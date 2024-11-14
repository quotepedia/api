from PIL.ImageFile import ImageFile
from sqlalchemy.sql import exists

from src.api.v1.users.models import User
from src.api.v1.users.schemas import UserRegistrationRequest
from src.db.deps import SessionDepends
from src.security import get_password_hash
from src.storage import fs
from src.storage.images import crop_image_to_square


class UserService:
    def __init__(self, session: SessionDepends) -> None:
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def is_email_registered(self, email: str) -> bool:
        return self.session.query(exists().where(User.email == email)).scalar()

    def register_user(self, args: UserRegistrationRequest) -> User:
        user = User(
            email=args.email,
            password=get_password_hash(args.password.get_secret_value()),
            is_verified=True,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update_email(self, user: User, new_email: str):
        user.is_verified = True
        user.email = new_email

        self.session.commit()
        self.session.refresh(user)

    def update_password(self, user: User, new_password: str) -> None:
        hashed_password = get_password_hash(password=new_password)
        user.password = hashed_password

        self.session.commit()
        self.session.refresh(user)

    def delete_avatar(self, user: User) -> None:
        self.record_avatar(user)

    def update_avatar(self, user: User, image: ImageFile) -> None:
        cropped_image = crop_image_to_square(image)

        extension = cropped_image.format or "PNG"
        name = fs.generate_unique_file_name_from_extension(extension)
        path = fs.get_system_path(name)
        cropped_image.save(path, extension)

        self.record_avatar(user, name)

    def record_avatar(self, user: User, avatar_url: str | None = None) -> None:
        if user.avatar_url:
            fs.remove(user.avatar_url)

        user.avatar_url = avatar_url

        self.session.commit()
        self.session.refresh(user)
