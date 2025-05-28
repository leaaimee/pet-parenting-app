from pydantic import BaseModel

class InvitationRequestSchema(BaseModel):
    pet_id: int
    invitee_id: int
    role: str
    access_level: str


class InvitationResponseSchema(BaseModel):
    id: int
    pet_id: int
    role: str
    access_level: str
    status: str

    class Config:
        orm_mode = True