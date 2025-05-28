from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.invitations_schema import InvitationRequestSchema
from backend.services.invitations_service import send_user_invitation, accept_user_invitation, \
    decline_user_invitation, get_pending_invitations
from backend.auth.jwt import get_current_user


router = APIRouter()


@router.get("/invitations")
def view_invitations(current_user: dict = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    """Returns all pending invitations for the current user"""
    return get_pending_invitations(current_user["id"], db)



@router.post("/invitations/send")
def send_invitation(
        data: InvitationRequestSchema,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Creates and sends a new invitation to a user for a pet"""
    result, status_code = send_user_invitation(data, current_user["id"], db)
    return JSONResponse(content=result, status_code=status_code)



@router.post("/invitations/{invite_id}/accept")
def accept_invitation(
        invitation_id: int,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Accepts an invitation and assigns the user a role for the pet"""
    result, status_code = accept_user_invitation(invitation_id, current_user["id"], db)
    return JSONResponse(content=result, status_code=status_code)



@router.post("/invitations/{invite_id}/decline")
def decline_invitation(
        invitation_id: int,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    result, status_code = decline_user_invitation(invitation_id, current_user["id"], db)
    return JSONResponse(content=result, status_code=status_code)


