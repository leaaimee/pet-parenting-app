from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user, AnonymousUserMixin

from backend.models.invitations_models import db, Invitations, InvitationStatus
from backend.services.invitations_service import set_role, send_user_invitation, accept_user_invitation, \
    decline_user_invitation

invitations_bp = Blueprint("invitations", __name__)


@invitations_bp.route("/invitations/send", methods=["POST"])
# @login_required
def send_invitation():
    result, status_code = send_user_invitation(request.form, current_user.id)
    return jsonify(result), status_code


@invitations_bp.route("/invitations/view", methods=["GET"])
def view_invitations():
    if isinstance(current_user, AnonymousUserMixin):
        # Fake dev user ID (just for now)
        fake_user_id = 1  # Replace with a real ID from your DB
    else:
        fake_user_id = current_user.id

    invitations = Invitations.query.filter_by(
        invitee_id=fake_user_id,
        status=InvitationStatus.PENDING
    ).all()
    return render_template("invites.html", invitations=invitations)


@invitations_bp.route("/invitations/<int:invite_id>/accept", methods=["POST"])
# @login_required
def accept_invitation(invitation_id):
    result, status_code = accept_user_invitation(invitation_id, current_user.id)
    return jsonify(result), status_code


@invitations_bp.route("/invitations/<int:invite_id>/decline", methods=["POST"])
# @login_required
def decline_invitation(invitation_id):
    result, status_code = decline_user_invitation(invitation_id, current_user.id)
    return jsonify(result), status_code


