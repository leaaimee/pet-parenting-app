from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.models.users_models import Roles

from backend.models.invitations_models import Invitations
from backend.utils.constants import InvitationStatus





import logging
logger = logging.getLogger(__name__)



async def send_pet_invitation_service(
    session: AsyncSession,
    pet,
    inviter_id: int,
    invitee_id: int,
    role: str,
    access_level: str
) -> Invitations | None:
    """Create and store a pending pet invitation in the database"""
    try:
        new_invite = Invitations(
            pet_id=pet.id,
            inviter_id=inviter_id,
            invitee_id=invitee_id,
            role=role,
            access_level=access_level,
            status=InvitationStatus.PENDING
        )

        session.add(new_invite)
        await session.commit()
        await session.refresh(new_invite)
        return new_invite

    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating invitation: {e}")
        return None




async def send_user_invitation(data, inviter_id: int, session: AsyncSession):
    """Send a new invitation from one user to another"""
    new_invite = Invitations(
        pet_id=data.pet_id,
        inviter_id=inviter_id,
        invitee_id=data.invitee_id,
        role=data.role,
        access_level=data.access_level,
        status=InvitationStatus.PENDING
    )

    session.add(new_invite)
    await session.commit()
    await session.refresh(new_invite)

    return {"message": "Invitation sent!"}, 200



async def get_pending_invitations(user_id: int, session: AsyncSession):
    """Return all pending invitations for a given user"""
    try:
        result = await session.execute(
            select(Invitations).where(
                Invitations.invitee_id == user_id,
                Invitations.status == InvitationStatus.PENDING
            )
        )
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Error fetching invitations: {e}")
        return []




async def accept_user_invitation(invitation_id: int, user_id: int, session: AsyncSession):
    """Accept an invitation and assign the invited role"""

    result = await session.execute(
        select(Invitations).where(Invitations.id == invitation_id)
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        return {"error": "Invitation not found"}, 404

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to accept this invitation"}, 403

    pet_id = invitation.pet_id
    role = invitation.role
    access_level = invitation.access_level

    new_role = await set_role(pet_id, user_id, role, access_level, invitation, session)

    if not new_role:
        return {"error": "Failed to accept invitation."}, 500

    return {"message": "Invitation accepted!"}, 200




async def decline_user_invitation(invitation_id: int, user_id: int, session: AsyncSession):
    """Decline an invitation and mark it as rejected"""

    result = await session.execute(
        select(Invitations).where(Invitations.id == invitation_id)
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        return {"error": "Invitation not found"}, 404

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to decline this invitation"}, 403

    invitation.status = InvitationStatus.DECLINED
    await session.commit()
    return {"message": "Invitation declined"}, 200




async def set_role(
    user_id: int,
    pet_id: int,
    role: str,
    access_level: str,
    invitation: Invitations,
    session: AsyncSession
):
    """Assigns role & updates invitation status"""
    try:
        new_role = Roles(
            pet_id=pet_id,
            user_id=user_id,
            role=role,
            access_level=access_level,
        )

        session.add(new_role)
        invitation.status = InvitationStatus.ACCEPTED

        await session.commit()
        await session.refresh(new_role)
        return new_role

    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Database error: {e}")
        return None
