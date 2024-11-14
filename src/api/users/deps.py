from typing import Annotated

from fastapi import Depends

from src.api.users.service import UserService

UserServiceDepends = Annotated[UserService, Depends(UserService)]
