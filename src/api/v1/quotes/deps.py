from typing import Annotated

from fastapi import Depends

from src.api.v1.quotes.service import QuoteService

QuoteServiceDepends = Annotated[QuoteService, Depends(QuoteService)]
