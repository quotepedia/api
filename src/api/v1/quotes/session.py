from typing import Annotated

from fastapi import Depends

from src.api.v1.quotes.query import QuoteQuery
from src.db.deps import GenericSession, GenericSessionFactory

QuoteSessionDepends = Annotated[GenericSession[QuoteQuery], Depends(GenericSessionFactory(query_cls=QuoteQuery))]
