from alembic.util import status

from backend import InvitationStatus
from backend.database import db
from flask_login import login_required, current_user
from backend.models.pets_models import Pets
from backend.routes.invitations_routes import send_invite, accept_invite
from backend.models.users_models import Roles
from backend.models.invitations_models import db, Invitations
from backend.utils.constants import InvitationStatus
from sqlalchemy.exc import SQLAlchemyError


def sent_pet_invitation(pet, inviter_id, invitee_id, role, access_level):
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