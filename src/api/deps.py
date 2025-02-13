from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.api.params import SearchParams
from src.config import settings
from src.i18n.deps import Translator


def get_search_params(translator: Translator, params: SearchParams = Depends(SearchParams)) -> SearchParams:
    if params.limit > settings.api.max_search_params_limit:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            translator.gettext("The requested search limit of %s exceeds the maximum allowed limit of %s.")
            % (params.limit, settings.api.max_search_params_limit),
        )
    return params


SearchParamsDepends = Annotated[SearchParams, Depends(get_search_params)]
