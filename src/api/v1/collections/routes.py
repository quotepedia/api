from fastapi import APIRouter, HTTPException, status

from src.api.deps import SearchParamsDepends
from src.api.v1.collections.deps import CollectionServiceDepends
from src.api.v1.collections.models import Collection
from src.api.v1.collections.schemas import CollectionCreateRequest, CollectionResponse, CollectionUpdateRequest
from src.api.v1.users.me.deps import CurrentUser, CurrentUserOrNone
from src.i18n import gettext as _

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("/{id}", response_model=CollectionResponse)
def get_collection(id: int, service: CollectionServiceDepends, current_user: CurrentUserOrNone):
    collection = service.get_collection(id)

    if not collection:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No collection found with the ID %s." % (id,)))

    is_private = collection.visibility == Collection.Visibility.PRIVATE
    has_access = current_user and current_user.id == collection.created_by_user_id

    if is_private and not has_access:
        raise HTTPException(status.HTTP_403_FORBIDDEN, _("Access denied to this private collection."))

    return collection


@router.get("/", response_model=list[CollectionResponse])
def get_public_collections(search_params: SearchParamsDepends, service: CollectionServiceDepends):
    collections = service.get_public_collections(search_params)

    if not collections:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            _("No collections found matching the provided search parameters."),
        )

    return collections


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(args: CollectionCreateRequest, current_user: CurrentUser, service: CollectionServiceDepends):
    return service.create_collection(args, created_by_user_id=current_user.id)


@router.patch("/{id}", response_model=CollectionResponse)
def update_collection(
    id: int, args: CollectionUpdateRequest, current_user: CurrentUser, service: CollectionServiceDepends
):
    collection = service.get_collection(id)

    if not collection:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No collection found with the ID %s." % (id,)))
    if collection.created_by_user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, _("You do not have permission to modify this collection."))

    return service.update_collection(collection, args)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(id: int, current_user: CurrentUser, service: CollectionServiceDepends):
    collection = service.get_collection(id)

    if not collection:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No collection found with the ID %s." % (id,)))
    if collection.created_by_user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, _("You do not have permission to modify this collection."))

    service.delete_collection(collection)


# TODO:
# @router.get("/{collection_id}/quotes")
# @router.post("/{collection_id}/quotes")
# @router.delete("/{collection_id}/quotes/{quote_id}")
