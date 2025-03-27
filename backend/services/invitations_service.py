from flask_login import login_required, current_user
from flask import jsonify, request
from backend.models.pets_models import Pets
from backend.models.users_models import Roles
from backend.utils.permissions import user_has_access
from backend.utils.constants import Permission
from backend.models.invitations_models import Invitations
from backend.database import db
from backend.utils.constants import InvitationStatus
from sqlalchemy.exc import SQLAlchemyError


def send_pet_invitation(pet, inviter_id, invitee_id, role, access_level):
    try:

        new_invite = Invitations(
            pet_id=pet.id,
            inviter_id=inviter_id,
            invitee_id=invitee_id,
            role=role,
            access_level=access_level,
            status=InvitationStatus.PENDING
        )

        db.session.add(new_invite)
        db.session.commit()
        return new_invite

    except Exception as e:
        db.session.rollback()
        print(f"Error creating invitation: {e}")  # TODO: Replace with proper logging
        return None



def send_user_invitation(data, user_id):

    pet_id = data.get("pet_id")
    invitee_id = data.get("invitee_id")
    role = data.get("role")
    access_level = data.get("access_level")

    pet = Pets.query.get(pet_id)
    if not pet:
        return {"error": "Pet not found"}, 404

    if pet.parent_id != user_id and not user_has_access(user_id, pet.id, Permission.ASSIGN_ROLES):
        return {"error": "You do not have permission to invite others to this pet."}, 403

    new_invite = send_pet_invitation(pet_id, invitee_id, role, access_level, user_id)

    if not new_invite:
        return {"error": "Failed to send invitation"}, 500

    return {"message": "Invitation sent!"}, 201


def accept_user_invitation(invitation_id, user_id):
    invitation = Invitations.query.get_or_404(invitation_id)

    if not invitation:
        return {"error": "Invitation not found"}, 404

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to accept this invitation"}, 403

    pet_id = invitation.pet_id
    role = invitation.role
    access_level = invitation.access_level

    new_role = set_role(pet_id, user_id, role, access_level, invitation)

    if not new_role:
        return {"error": "Failed to accept invitation."}, 500

    return {"message": "Invitation accepted!"}, 200


def decline_user_invitation(invitation_id, user_id):
    invitation = Invitations.query.get_or_404(invitation_id)

    if invitation.invitee_id != user_id:
        return {"error": "You are not authorized to decline this invitation"}, 403

    invitation.status = InvitationStatus.DECLINED
    db.session.commit()

    return {"message": "Invitation declined!"}, 200



def set_role(user_id, pet_id, role, access_level, invitation):
    """ Assigns role & invitation status """
    try:
        new_role = Roles(
            pet_id=pet_id,
            user_id=user_id,
            role=role,
            access_level=access_level,
        )

        db.session.add(new_role)
        invitation.status = InvitationStatus.ACCEPTED

        db.session.commit()
        return new_role

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {e}")  # Maybe replace with logging later
        return None