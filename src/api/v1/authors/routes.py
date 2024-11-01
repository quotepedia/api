from fastapi import APIRouter, HTTPException, status

from src.api.deps import SearchParamsDepends
from src.api.v1.authors.deps import AuthorServiceDepends
from src.api.v1.authors.schemas import AuthorCreateRequest, AuthorResponse
from src.api.v1.users.me.deps import CurrentUser
from src.i18n import gettext as _

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/{name}", response_model=AuthorResponse)
def get_author(name: str, service: AuthorServiceDepends):
    author = service.get_author(name)

    if not author:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No author found with the name '%s'." % (name,)))

    return author


@router.get("/", response_model=list[AuthorResponse])
def get_authors(search_params: SearchParamsDepends, service: AuthorServiceDepends):
    authors = service.get_authors(search_params)

    if not authors:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No authors found matching the provided search parameters."))

    return authors


@router.post("/", response_model=AuthorResponse)
def create_author(current_user: CurrentUser, args: AuthorCreateRequest, service: AuthorServiceDepends):
    if service.exists(args.name):
        raise HTTPException(status.HTTP_409_CONFLICT, _("An author with the name '%s' already exists." % (args.name,)))
    if args.name == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, _("Author name cannot be an empty string."))

    return service.create_author(name=args.name, created_by_user_id=current_user.id)
