from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends

from backend.schemas.invitations_schema import InvitationRequestSchema
from backend.services.invitations_service import send_user_invitation, accept_user_invitation, \
    decline_user_invitation, get_pending_invitations
from backend.auth.jwt import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_async_session


router = APIRouter()


@router.get("/invitations")
async def view_invitations(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns all pending invitations for the current user"""
    return await get_pending_invitations(current_user["id"], session)



@router.post("/invitations")
async def send_invitation(
        data: InvitationRequestSchema,
        current_user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Creates and sends a new invitation to a user for a pet"""
    result, status_code = await send_user_invitation(data, current_user["id"], session)
    return JSONResponse(content=result, status_code=status_code)



@router.post("/invitations/{invitation_id}/accept")
async def accept_invitation(
        invitation_id: int,
        current_user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Accepts an invitation and assigns the user a role for the pet"""
    result, status_code = await accept_user_invitation(invitation_id, current_user["id"], session)
    return JSONResponse(content=result, status_code=status_code)



@router.post("/invitations/{invitation_id}/decline")
async def decline_invitation(
        invitation_id: int,
        current_user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    result, status_code = await decline_user_invitation(invitation_id, current_user["id"], session)
    return JSONResponse(content=result, status_code=status_code)


