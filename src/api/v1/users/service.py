from PIL.ImageFile import ImageFile
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

from src.api.v1.users.models import User
from src.api.v1.users.schemas import UserCreate
from src.security import get_password_hash
from src.storage import fs
from src.storage.images import crop_image_to_square


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def is_email_registered(session: Session, email: str) -> bool:
    return session.query(exists().where(User.email == email)).scalar()


def create_user(session: Session, schema: UserCreate) -> User:
    user = User(
        email=schema.email,
        password=get_password_hash(schema.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def verify_user(session: Session, user: User) -> None:
    user.is_verified = True
    session.commit()
    session.refresh(user)


def update_email(session: Session, user: User, new_email: str):
    user.is_verified = False
    user.email = new_email
    session.commit()
    session.refresh(user)


def update_password(session: Session, user: User, new_password: str) -> None:
    hashed_password = get_password_hash(password=new_password)
    user.password = hashed_password
    session.commit()
    session.refresh(user)


def record_avatar(session: Session, user: User, avatar_url: str | None = None) -> None:
    if user.avatar_url:
        fs.remove(user.avatar_url)

    user.avatar_url = avatar_url
    session.commit()
    session.refresh(user)


def update_avatar(session: Session, user: User, image: ImageFile) -> None:
    cropped_image = crop_image_to_square(image)

    extension = cropped_image.format or "PNG"
    name = fs.generate_unique_file_name_from_extension(extension)
    path = fs.get_system_path(name)
    cropped_image.save(path, extension)

    record_avatar(session, user, name)


def delete_avatar(session: Session, user: User) -> None:
    record_avatar(session, user)
