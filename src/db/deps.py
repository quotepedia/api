from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session as _Session

from src.db import ENGINE


def get_session() -> Generator[_Session, None, None]:
    session = _Session(ENGINE)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


Session = Annotated[_Session, Depends(get_session)]
