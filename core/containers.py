from dependency_injector import containers, providers
from application.services.auth.user_auth_service import (
    JWTTokenBlacklist,
    JWTTokenService,
    MockUserAuthService,
)
from application.services.user.admin_user_service import (
    MockAdminUserQueryService,
)
from core.providers import load_auth_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["presentation.controllers"],
    )

    # Auth
    auth_config = providers.Singleton(load_auth_config)
    token_black_list = providers.Singleton(JWTTokenBlacklist)
    token_service = providers.Singleton(
        JWTTokenService, black_list=token_black_list, config=auth_config
    )
    auth_service = providers.Singleton(MockUserAuthService)

    # UserQuery
    admin_user_query_service = providers.Singleton(MockAdminUserQueryService)
    contractor_user_query_service = providers.Singleton(MockUserAuthService)
    contractee_user_query_service = providers.Singleton(MockUserAuthService)
