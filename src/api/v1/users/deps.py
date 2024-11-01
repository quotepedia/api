from typing import Annotated

from fastapi import Depends

from src.api.v1.users.service import UserService

UserServiceDepends = Annotated[UserService, Depends(UserService)]
