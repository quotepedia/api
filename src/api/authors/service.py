from sqlalchemy import exists

from src.api.authors.models import Author
from src.api.params import SearchParams
from src.db.deps import SessionDepends


class AuthorService:
    def __init__(self, session: SessionDepends) -> None:
        self.session = session

    def create_author(self, *, name: str, created_by_user_id: int) -> Author:
        author = Author(name=name, created_by_user_id=created_by_user_id)

        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)

        return author

    def get_author_by_id(self, author_id: int) -> Author | None:
        return self.session.get(Author, author_id)

    def get_author_by_name(self, name: str) -> Author | None:
        return self.session.query(Author).filter(Author.name == name).first()

    def get_authors(self, search_params: SearchParams) -> list[Author]:
        query = self.session.query(Author)

        if search_params.q:
            query = query.filter(Author.name.icontains(search_params.q))

        return query.order_by(Author.name).offset(search_params.offset).limit(search_params.limit).all()

    def exists(self, name: str) -> bool:
        return self.session.query(exists().where(Author.name == name)).scalar()
