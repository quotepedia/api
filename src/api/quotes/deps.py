from typing import Annotated

from fastapi import Depends

from src.api.quotes.service import QuoteService

QuoteServiceDepends = Annotated[QuoteService, Depends(QuoteService)]
