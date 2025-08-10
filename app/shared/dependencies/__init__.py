from typing import Annotated

from fastapi import Depends, File
from fastapi.security import OAuth2PasswordRequestForm
from geopy import Nominatim

from app.application.usecase.auth import AuthSessionUseCase, get_auth_session_case
from app.application.usecase.ride import ger_ride_use_case
from app.application.usecase.schedule import ScheduleTravelUseCase, get_schedule_use_case
from app.application.usecase.user import UserUseCase, get_user_use_case
from app.core.oauth2 import oauth2_scheme
from app.shared.credentials import get_user_code_from_credentials, is_user_authenticated, \
    get_user_code_and_role_code_from_credentials
from app.shared.dependencies.depends import get_locator_agent
from app.shared.types import Token
from app.shared.types.enum import RoleUser

OAuth2Scheme = Annotated[Token, Depends(oauth2_scheme)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
AuthUserCodeCredentials = Annotated[int, Depends(get_user_code_from_credentials)]
AuthUserCodeAndRoleCredentials = Annotated[tuple[int, RoleUser], Depends(get_user_code_and_role_code_from_credentials)]
UserIsAuthenticated = Annotated[bool, Depends(is_user_authenticated)]

FileRequest = Annotated[bytes | None, File()]
NominatimDepend = Annotated[Nominatim, Depends(get_locator_agent)]

UserDependency = Annotated[UserUseCase, Depends(get_user_use_case)]
ScheduleDependency = Annotated[ScheduleTravelUseCase, Depends(get_schedule_use_case)]
RideDependency = Annotated[ScheduleTravelUseCase, Depends(ger_ride_use_case)]

AuthDependency = Annotated[AuthSessionUseCase, Depends(get_auth_session_case)]
