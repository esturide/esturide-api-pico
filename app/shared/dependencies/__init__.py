from typing import Annotated, Optional

from fastapi import Depends, File
from fastapi.security import OAuth2PasswordRequestForm
from geopy import Nominatim

from app.application.usecase.auth import AuthUseCase, get_auth_case
from app.application.usecase.user import UserUseCase, get_user_use_case
from app.core.oauth2 import oauth2_scheme
from app.shared.credentials import user_credentials, get_user_is_authenticated, validate_admin_role, \
    validate_permission_role
from app.shared.dependencies.depends import get_locator_agent
from app.shared.models.user import User
from app.shared.types import Token

OAuth2Scheme = Annotated[Token, Depends(oauth2_scheme)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
UserCredentials = Annotated[Optional[User], Depends(user_credentials)]
AuthUserCodeCredentials = Annotated[User, Depends(get_user_is_authenticated)]
AdminAuthenticated = Annotated[bool, Depends(validate_admin_role)]
ManagerAuthenticated = Annotated[bool, Depends(validate_permission_role)]

FileRequest = Annotated[bytes | None, File()]
NominatimDepend = Annotated[Nominatim, Depends(get_locator_agent)]

UserDependency = Annotated[UserUseCase, Depends(get_user_use_case)]

AuthDependency = Annotated[AuthUseCase, Depends(get_auth_case)]
