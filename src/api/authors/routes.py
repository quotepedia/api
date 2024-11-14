from fastapi import APIRouter, HTTPException, status

from src.api.authors.deps import AuthorServiceDepends
from src.api.authors.schemas import AuthorCreateRequest, AuthorResponse
from src.api.deps import SearchParamsDepends
from src.api.tags import Tags
from src.api.users.me.deps import CurrentUser
from src.i18n import gettext as _

router = APIRouter(prefix="/authors", tags=[Tags.AUTHORS])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(args: AuthorCreateRequest, current_user: CurrentUser, service: AuthorServiceDepends):
    if service.exists(args.name):
        raise HTTPException(status.HTTP_409_CONFLICT, _("An author with the name '%s' already exists." % (args.name,)))

    return service.create_author(name=args.name, created_by_user_id=current_user.id)


@router.get("/{name}", response_model=AuthorResponse)
def get_author(name: str, service: AuthorServiceDepends):
    author = service.get_author_by_name(name)

    if not author:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No author found with the name '%s'." % (name,)))

    return author


@router.get("/", response_model=list[AuthorResponse])
def get_authors(search_params: SearchParamsDepends, service: AuthorServiceDepends):
    authors = service.get_authors(search_params)

    if not authors:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("No authors found matching the provided search parameters."))

    return authors
