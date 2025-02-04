from fastapi import APIRouter, HTTPException, status

from src.api.authors import AuthorServiceDepends
from src.api.deps import SearchParamsDepends
from src.api.quotes.deps import QuoteServiceDepends
from src.api.quotes.schemas import QuoteCollectionsResponse, QuoteCreateRequest, QuoteResponse, QuoteUpdateRequest
from src.api.tags import Tags
from src.api.users.me.deps import CurrentUser
from src.i18n.deps import Translator

router = APIRouter(prefix="/quotes", tags=[Tags.QUOTES])


@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
def create_quote(
    args: QuoteCreateRequest,
    current_user: CurrentUser,
    quote_service: QuoteServiceDepends,
    author_service: AuthorServiceDepends,
    translator: Translator,
):
    if args.author_id is not None and not author_service.get_author_by_id(args.author_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No author found with the ID '%s'." % (args.author_id,))
        )
    return quote_service.create_quote(args, created_by_user_id=current_user.id)


@router.patch("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    quote_id: int,
    args: QuoteUpdateRequest,
    current_user: CurrentUser,
    service: QuoteServiceDepends,
    translator: Translator,
):
    quote = service.get_quote_by_id(quote_id)

    if not quote:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No quote found with the ID %s." % (quote_id,))
        )
    if quote.created_by_user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, translator.gettext("You do not have permission to modify this quote.")
        )

    return service.update_quote(quote, args)


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quote(quote_id: int, current_user: CurrentUser, service: QuoteServiceDepends, translator: Translator):
    quote = service.get_quote_by_id(quote_id)

    if not quote:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No quote found with the ID %s." % (quote_id,))
        )
    if quote.created_by_user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, translator.gettext("You do not have permission to modify this quote.")
        )

    service.delete_quote(quote)


@router.get("/{quote_id}", response_model=QuoteCollectionsResponse)
def get_quote(quote_id: int, service: QuoteServiceDepends, translator: Translator):
    quote = service.get_quote_by_id(quote_id)

    if not quote:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No quote found with the ID %s." % (quote_id,))
        )

    return quote


@router.get("/", response_model=list[QuoteResponse])
def get_quotes(search_params: SearchParamsDepends, service: QuoteServiceDepends, translator: Translator):
    quotes = service.get_quotes(search_params)

    if not quotes:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            translator.gettext("No quotes found matching the provided search parameters."),
        )

    return quotes
