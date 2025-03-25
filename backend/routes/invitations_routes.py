from flask import Blueprint, request, jsonify
from backend.models.invitations_models import db, Invitations, InvitationStatus
from backend.services.invitations_service import set_role
from flask_login import login_required, current_user
from backend.models.pets_models import Pets
from backend.models.users_models import Roles
from backend.services.invitations_service import sent_pet_invitation
from backend.utils.permissions import user_has_access
from backend.utils.constants import Permission

invitations_bp = Blueprint("invitations")

@invitations_bp.route("/invite", methods=["POST"])
@login_required
def send_invite():
    data = request.json
    pet_id = data.get("pet_id")
    invitee_id = data.get("invitee_id")
    role = data.get("role")
    access_level = data.get("access_level")

    pet = Pets.query.get(pet_id)
    if not pet:
        return jsonify({"error: Pet not found"}), 404

    if pet.parent_id != current_user.id and not user_has_access(current_user.id, pet.id, Permission.ASSIGN_ROLES):
        return jsonify({"error": "You do not have permission to invite others to this pet."}), 403

    new_invite = sent_pet_invitation(pet_id, invitee_id, role, access_level, current_user.id)

    if not new_invite:
        return jsonify({"error": "Failed to send invitation"}), 500

    return jsonify({"message": "Invitation sent!"}), 201



@invitations_bp.route("/invite/accept/<int:invite_id>", methods=["POST"])
@login_required
def accept_invite(invite_id):
    invitation = Invitations.query.get_or_404(invite_id)

    pet_id = invitation.pet_id
    role = invitation.role
    access_level = invitation.access_level

    if invitation.invitee_id != current_user.id:
        return jsonify({"error": "You are not authorized to accept this invitation"}), 403

    new_role = set_role(pet_id, current_user.id, role, access_level, invitation)

    if not new_role:
        return jsonify({"error": "Failed to accept invitation."}), 500

    return jsonify({"message": "Invitation accepted!"}), 200



@invitations_bp.route("invite/decline/<int:invite_id>", methods=["POST"])
@login_required
def decline_invitation(invite_id):
    invitation = Invitations.query.get_or_404(invite_id)

    if invitation.invitee_id != current_user.id:
        return jsonify({"error": "You are not authorized to decline this invitation"}), 403

    invitation.status = InvitationStatus.DECLINED
    db.session.commit()

    return jsonify({"message": "Invitation declined."}), 200


