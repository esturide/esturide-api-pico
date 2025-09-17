from typing import Annotated

from fastapi import Depends, File
from fastapi.security import OAuth2PasswordRequestForm

from geopy.geocoders.base import Geocoder

from app.application.usecase.admin import AdminManagerUseCase, get_admin_manager_use_case
from app.application.usecase.auth import AuthSessionUseCase, get_auth_session_case
from app.application.usecase.notify import NotifyUseCase, get_notify_user_case
from app.application.usecase.ride import get_ride_use_case, RideUseCase
from app.application.usecase.schedule import ScheduleTravelUseCase, get_schedule_use_case
from app.application.usecase.tracking import TrackingUseCase, get_tracking_use_case
from app.application.usecase.user import UserUseCase, get_user_use_case
from app.core.oauth2 import oauth2_scheme
from app.shared.credentials import get_user_code_from_credentials, is_user_authenticated, \
    get_user_code_and_role_code_from_credentials
from app.shared.dependencies.depends import get_nominatim_locator_agent, get_google_locator_agent
from app.shared.types import Token
from app.shared.types.enum import RoleUser

OAuth2Scheme = Annotated[Token, Depends(oauth2_scheme)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
AuthUserCodeCredentials = Annotated[int, Depends(get_user_code_from_credentials)]
AuthUserCodeAndRoleCredentials = Annotated[tuple[int, RoleUser], Depends(get_user_code_and_role_code_from_credentials)]
UserIsAuthenticated = Annotated[bool, Depends(is_user_authenticated)]

FileRequest = Annotated[bytes | None, File()]
NominatimDepend = Annotated[Geocoder, Depends(get_nominatim_locator_agent)]
GoogleGeolocationDepend = Annotated[Geocoder, Depends(get_google_locator_agent)]

UserDependency = Annotated[UserUseCase, Depends(get_user_use_case)]
ScheduleDependency = Annotated[ScheduleTravelUseCase, Depends(get_schedule_use_case)]
RideDependency = Annotated[RideUseCase, Depends(get_ride_use_case)]
AdminManagerDependency = Annotated[AdminManagerUseCase, Depends(get_admin_manager_use_case)]
NotifyDependency = Annotated[NotifyUseCase, Depends(get_notify_user_case)]
TrackingDependency = Annotated[TrackingUseCase, Depends(get_tracking_use_case)]

AuthDependency = Annotated[AuthSessionUseCase, Depends(get_auth_session_case)]
