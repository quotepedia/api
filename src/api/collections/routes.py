from fastapi import APIRouter, HTTPException, status

from src.api.collections.deps import CollectionServiceDepends
from src.api.collections.models import Collection
from src.api.collections.schemas import CollectionCreateRequest, CollectionResponse, CollectionUpdateRequest
from src.api.deps import SearchParamsDepends
from src.api.quotes.deps import QuoteServiceDepends
from src.api.quotes.schemas import QuoteCollectionsResponse, QuoteResponse
from src.api.tags import Tags
from src.api.users.me.deps import CurrentUser, CurrentUserOrNone
from src.i18n.deps import Translator

router = APIRouter(prefix="/collections", tags=[Tags.COLLECTIONS])


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(args: CollectionCreateRequest, current_user: CurrentUser, service: CollectionServiceDepends):
    return service.create_collection(args, created_by_user_id=current_user.id)


@router.patch("/{collection_id}", response_model=CollectionResponse)
def update_collection(
    collection_id: int,
    args: CollectionUpdateRequest,
    current_user: CurrentUser,
    service: CollectionServiceDepends,
    translator: Translator,
):
    collection = service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )
    if collection.created_by_user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, translator.gettext("You do not have permission to modify this collection.")
        )

    return service.update_collection(collection, args)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: int, current_user: CurrentUser, service: CollectionServiceDepends, translator: Translator
):
    collection = service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )
    if collection.created_by_user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, translator.gettext("You do not have permission to modify this collection.")
        )

    service.delete_collection(collection)


@router.get("/{collection_id}", response_model=CollectionResponse)
def get_collection(
    collection_id: int, service: CollectionServiceDepends, current_user: CurrentUserOrNone, translator: Translator
):
    collection = service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )

    is_private = collection.visibility == Collection.Visibility.PRIVATE
    has_access = current_user and current_user.id == collection.created_by_user_id

    if is_private and not has_access:
        raise HTTPException(status.HTTP_403_FORBIDDEN, translator.gettext("Access denied to this private collection."))

    return collection


@router.get("/{collection_id}/quotes", response_model=list[QuoteResponse])
def get_collection_quotes(
    collection_id: int,
    search_params: SearchParamsDepends,
    current_user: CurrentUserOrNone,
    collection_service: CollectionServiceDepends,
    quote_service: QuoteServiceDepends,
    translator: Translator,
):
    collection = collection_service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )

    is_private = collection.visibility == Collection.Visibility.PRIVATE
    has_access = current_user and current_user.id == collection.created_by_user_id

    if is_private and not has_access:
        raise HTTPException(status.HTTP_403_FORBIDDEN, translator.gettext("Access denied to this private collection."))

    return quote_service.get_collection_quotes(collection_id, search_params)


@router.get("/", response_model=list[CollectionResponse])
def get_public_collections(
    search_params: SearchParamsDepends, service: CollectionServiceDepends, translator: Translator
):
    collections = service.get_public_collections(search_params)

    if not collections:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            translator.gettext("No collections found matching the provided search parameters."),
        )

    return collections


@router.post("/{collection_id}/quotes", response_model=QuoteCollectionsResponse, status_code=status.HTTP_201_CREATED)
def add_quote_to_collection(
    collection_id: int,
    quote_id: int,
    current_user: CurrentUser,
    collection_service: CollectionServiceDepends,
    quote_service: QuoteServiceDepends,
    translator: Translator,
):
    quote = quote_service.get_quote_by_id(quote_id)

    if not quote:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No quote found with the ID %s." % (quote_id,))
        )

    collection = collection_service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )
    if quote.id in (quote.id for quote in collection.quotes):
        raise HTTPException(
            status.HTTP_409_CONFLICT, translator.gettext("Quote with the ID %s is in collection." % (quote_id,))
        )

    if current_user.id != collection.created_by_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, translator.gettext("Access denied to this private collection."))

    return collection_service.add_quote_to_collection(quote, collection)


@router.delete("/{collection_id}/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_quote_from_collection(
    collection_id: int,
    quote_id: int,
    current_user: CurrentUser,
    collection_service: CollectionServiceDepends,
    quote_service: QuoteServiceDepends,
    translator: Translator,
):
    quote = quote_service.get_quote_by_id(quote_id)

    if not quote:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No quote found with the ID %s." % (quote_id,))
        )

    collection = collection_service.get_collection(collection_id)

    if not collection:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, translator.gettext("No collection found with the ID %s." % (collection_id,))
        )
    if quote.id not in (quote.id for quote in collection.quotes):
        raise HTTPException(
            status.HTTP_409_CONFLICT, translator.gettext("Quote with the ID %s is not in collection." % (quote_id,))
        )

    if current_user.id != collection.created_by_user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, translator.gettext("Access denied to this private collection."))

    collection_service.remove_quote_from_collection(quote, collection)
