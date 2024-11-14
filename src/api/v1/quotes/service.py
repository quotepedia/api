from src.api.params import SearchParams
from src.api.v1.quotes.enums import UserQuotesType
from src.api.v1.quotes.models import Quote
from src.api.v1.quotes.schemas import QuoteCreateRequest, QuoteUpdateRequest
from src.api.v1.quotes.session import QuoteSessionDepends


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

    def get_quotes(self, search_params: SearchParams) -> list[Quote]:
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
