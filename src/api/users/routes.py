from fastapi import APIRouter

from src.api.tags import Tags
from src.api.users.deps import UserServiceDepends
from src.api.users.schemas import UserEmailRequest, UserExistenceResponse

router = APIRouter(prefix="/users", tags=[Tags.USERS])


@router.post("/exists")
def user_exists(args: UserEmailRequest, service: UserServiceDepends) -> UserExistenceResponse:
    exists = service.is_email_registered(args.email)
    return UserExistenceResponse(exists=exists)
