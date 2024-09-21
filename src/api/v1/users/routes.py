from fastapi import APIRouter

from src.api.v1.users.schemas import UserEmailRequest, UserExistenceResponse
from src.api.v1.users.service import is_email_registered
from src.db.deps import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/exists")
def user_exists(args: UserEmailRequest, session: Session) -> UserExistenceResponse:
    exists = is_email_registered(session, args.email)
    return UserExistenceResponse(exists=exists)
