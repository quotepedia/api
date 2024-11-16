from typing import Self

from sqlalchemy import or_
from sqlalchemy.orm import Query

from src.api.authors.models import Author
from src.api.collections.models import Collection
from src.api.params import SearchParams
from src.api.quotes.enums import UserQuotesType
from src.api.quotes.models import Quote


class QuoteQuery(Query[Quote]):
    def filter_by_search_params(self, search_params: SearchParams) -> Self:
        if search_params.q:
            self = self.filter(
                or_(
                    Quote.content.icontains(search_params.q) |
                    Quote.author.has(Author.name.icontains(search_params.q)),
                )
            )

        return self.offset(search_params.offset).limit(search_params.limit)

    def filter_by_collection_id(self, collection_id: int) -> Self:
        return self.filter(Quote.collections.any(Collection.id == collection_id))

    def filter_by_user_quotes_type(self, user_id: int, type: UserQuotesType) -> Self:
        match type:
            case UserQuotesType.ALL:
                return self.filter_by_user_id_all(user_id)
            case UserQuotesType.SAVED:
                return self.filter_by_user_id_saved(user_id)
            case UserQuotesType.CREATED:
                return self.filter_by_user_id_created(user_id)

    def filter_by_user_id_all(self, user_id: int) -> Self:
        return self.outerjoin(Quote.collections).filter(
            or_(
                Quote.collections.any((Collection.created_by_user_id == user_id)),
                Quote.created_by_user_id == user_id,
            )
        )

    def filter_by_user_id_saved(self, user_id: int) -> Self:
        return self.join(Quote.collections).filter(
            Quote.collections.any((Collection.created_by_user_id == user_id)),
            Quote.created_by_user_id != user_id,
        )

    def filter_by_user_id_created(self, user_id: int) -> Self:
        return self.filter(Quote.created_by_user_id == user_id)
