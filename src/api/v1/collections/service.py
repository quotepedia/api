from sqlalchemy.orm import Query

from src.api.params import SearchParams
from src.api.v1.collections.models import Collection
from src.api.v1.collections.schemas import CollectionCreateRequest, CollectionUpdateRequest
from src.db.deps import Session


class CollectionService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_collection(self, id: int) -> Collection | None:
        return self.session.get(Collection, id)

    def get_public_collections(self, search_params: SearchParams) -> list[Collection]:
        query = self.session.query(Collection).filter(Collection.visibility == Collection.Visibility.PUBLIC)
        query = self._filter_collections_query(query, search_params)

        return query.all()

    def get_user_collections(self, user_id: int, search_params: SearchParams) -> list[Collection]:
        query = self.session.query(Collection).filter(Collection.created_by_user_id == user_id)
        query = self._filter_collections_query(query, search_params)

        return query.all()

    def _filter_collections_query(self, query: Query[Collection], search_params: SearchParams) -> Query[Collection]:
        if search_params.q:
            query = query.filter(
                Collection.name.ilike(f"%{search_params.q}%") | Collection.description.ilike(f"%{search_params.q}%")
            )

        return query.offset(search_params.offset).limit(search_params.limit)

    def create_collection(self, args: CollectionCreateRequest, *, created_by_user_id: int) -> Collection:
        collection = Collection(**args.model_dump(), created_by_user_id=created_by_user_id)

        self.session.add(collection)
        self.session.commit()
        self.session.refresh(collection)

        return collection

    def update_collection(self, collection: Collection, args: CollectionUpdateRequest) -> Collection:
        collection.update_from_schema(args)

        self.session.add(collection)
        self.session.commit()
        self.session.refresh(collection)

        return collection

    def delete_collection(self, collection: Collection) -> None:
        self.session.delete(collection)
        self.session.commit()
