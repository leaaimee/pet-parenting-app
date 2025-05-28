from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.models.pets_models import Pets
from backend.models.users_models import Roles
from backend.utils.permissions import user_has_access
from backend.utils.constants import Permission
from backend.models.invitations_models import Invitations
from backend.utils.constants import InvitationStatus


from backend.database import SessionLocal

import logging
logger = logging.getLogger(__name__)



def send_pet_invitation(
    db: Session,  # ✅ Accept db session from outside
    pet,
    inviter_id: int,
    invitee_id: int,
    role: str,
    access_level: str
):
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

        db.add(new_invite)         # ✅ SQLAlchemy-native add
        db.commit()                # ✅ Explicit commit
        db.refresh(new_invite)     # ✅ Optional: loads auto fields like ID
        return new_invite

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating invitation: {e}")
        return None



def send_user_invitation(data, inviter_id, db: Session):
    """Send a new invitation from one user to another"""
    new_invite = Invitations(
        pet_id=data.pet_id,
        inviter_id=inviter_id,
        invitee_id=data.invitee_id,
        role=data.role,
        access_level=data.access_level,
        status=InvitationStatus.PENDING
    )

    db.add(new_invite)
    db.commit()
    db.refresh(new_invite)

    return {"message": "Invitation sent!"}, 200



def get_pending_invitations(user_id: int, db: Session):
    """Return all pending invitations for a given user"""

    try:
        return db.query(Invitations).filter_by(
            invitee_id=user_id,
            status=InvitationStatus.PENDING
        ).all()
    except Exception as e:
        logger.error(f"Error fetching invitations: {e}")
        return []



def accept_user_invitation(invitation_id, user_id, db: Session):
    """Accept an invitation and assign the invited role"""

    invitation = db.query(Invitations).filter_by(id=invitation_id).first()

    if not invitation:
        return {"error": "Invitation not found"}, 404

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to accept this invitation"}, 403

    pet_id = invitation.pet_id
    role = invitation.role
    access_level = invitation.access_level

    new_role = set_role(pet_id, user_id, role, access_level, invitation, db)

    if not new_role:
        return {"error": "Failed to accept invitation."}, 500

    return {"message": "Invitation accepted!"}, 200



def decline_user_invitation(invitation_id, user_id, db: Session):
    """Decline an invitation and mark it as rejected"""

    invitation = db.query(Invitations).filter_by(id=invitation_id).first()

    if not invitation:
        return {"error": "Invitation not found"}, 404

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to decline this invitation"}, 403

    invitation.status = InvitationStatus.DECLINED
    db.commit()
    return {"message": "Invitation declined"}, 200



def set_role(user_id, pet_id, role, access_level, invitation, db: Session):
    """Assigns role & updates invitation status"""
    try:
        new_role = Roles(
            pet_id=pet_id,
            user_id=user_id,
            role=role,
            access_level=access_level,
        )

        db.add(new_role)
        invitation.status = InvitationStatus.ACCEPTED

        db.commit()
        db.refresh(new_role)  # Optional but safe
        return new_role

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        return None