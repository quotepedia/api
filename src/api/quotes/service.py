from sqlalchemy.sql.expression import func, text

from src.api.collections.models import Collection, QuoteCollection
from src.api.params import SearchParams
from src.api.quotes.enums import UserQuotesType
from src.api.quotes.models import Quote
from src.api.quotes.schemas import QuoteCreateRequest, QuoteUpdateRequest
from src.api.quotes.session import QuoteSessionDepends


class QuoteService:
    def __init__(self, session: QuoteSessionDepends) -> None:
        self.session = session

    def create_quote(self, args: QuoteCreateRequest, *, created_by_user_id: int) -> Quote:
        quote = Quote(**args.model_dump(), created_by_user_id=created_by_user_id)

        self.session.add(quote)
        self.session.commit()
        self.session.refresh(quote)

        return quote

    def update_quote(self, quote: Quote, args: QuoteUpdateRequest) -> Quote:
        quote.update_from_schema(args)

        self.session.add(quote)
        self.session.commit()
        self.session.refresh(quote)

        return quote

    def delete_quote(self, quote: Quote) -> None:
        self.session.delete(quote)
        self.session.commit()

    def get_quote_by_id(self, quote_id: int) -> Quote | None:
        return self.session.query(Quote).get(quote_id)

    def get_quote_collection_ids(self, quote_id: int) -> list[int]:
        query = (
            self.session.query(QuoteCollection.collection_id).filter(QuoteCollection.quote_id == quote_id).distinct()
        )

        collection_ids = [collection_id for (collection_id,) in query.all()]  # type: ignore

        return collection_ids

    def bulk_modify_quote_collections(self, quote_id: int, new_collection_ids: list[int]) -> None:
        current_collection_ids = self.get_quote_collection_ids(quote_id)

        collections_to_remove = set(current_collection_ids) - set(new_collection_ids)

        if collections_to_remove:
            self.session.query(QuoteCollection).filter(
                QuoteCollection.quote_id == quote_id, QuoteCollection.collection_id.in_(collections_to_remove)
            ).delete(synchronize_session=False)

        for collection_id in new_collection_ids:
            collection_exists = (
                self.session.query(Collection).filter(Collection.id == collection_id).first() is not None
            )

            if collection_exists:
                quote_collection_exists = (
                    self.session.query(QuoteCollection)
                    .filter(QuoteCollection.quote_id == quote_id, QuoteCollection.collection_id == collection_id)
                    .first()
                    is None
                )

                if quote_collection_exists:
                    new_collection = QuoteCollection(quote_id=quote_id, collection_id=collection_id)
                    self.session.add(new_collection)

        self.session.commit()

    def get_quotes(self, search_params: SearchParams) -> list[Quote]:
        if not search_params.q:
            self.session.execute(text(f"SELECT setseed({search_params.seed})"))
            return self.session.query(Quote).order_by(func.random()).filter_by_search_params(search_params).all()
        return self.session.query(Quote).filter_by_search_params(search_params).all()

    def get_user_quotes(self, user_id: int, search_params: SearchParams, type: UserQuotesType) -> list[Quote]:
        return (
            self.session.query(Quote)
            .filter_by_user_quotes_type(user_id, type)
            .filter_by_search_params(search_params)
            .all()
        )

    def get_collection_quotes(self, collection_id: int, search_params: SearchParams) -> list[Quote]:
        return (
            self.session.query(Quote)
            .filter_by_collection_id(collection_id)
            .filter_by_search_params(search_params)
            .all()
        )

    def get_random_quote(self) -> Quote | None:
        return self.session.query(Quote).order_by(func.random()).limit(1).first()
