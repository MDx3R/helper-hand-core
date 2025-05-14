from dependency_injector import containers, providers
from application.services.auth.user_auth_service import (
    JWTTokenBlacklist,
    JWTTokenService,
    MockUserAuthService,
)
from application.services.user.admin_user_service import (
    AdminUserQueryServiceImpl,
)
from application.usecases.user.admin.get_pending_user_use_case import (
    GetPendingUserUseCase,
)
from application.usecases.user.admin.get_user_use_case import (
    GetProfileForAdminUseCase,
    GetUserForAdminUseCase,
)
from core.config import Config
from infrastructure.database.database import (
    Database,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.user.admin.admin_command_repository import (
    AdminCommandRepositoryImpl,
)
from infrastructure.repositories.user.admin.admin_query_repository import (
    AdminQueryRepositoryImpl,
)
from infrastructure.repositories.user.user_query_repository import (
    UserQueryRepositoryImpl,
)
from infrastructure.repositories.user.user_role_query_repository import (
    UserRoleQueryRepositoryImpl,
)
from infrastructure.transactions.transaction_manager import (
    SQLAlchemyTransactionManager,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["presentation.controllers", "run"],
    )

    # Config
    config = providers.Singleton(Config.load)
    auth_config = config.provided.auth
    db_config = config.provided.db

    # Database
    database = providers.Singleton(Database, config=db_config)

    session_factory = providers.Singleton(
        lambda database: database.get_session_factory(), database=database
    )
    transaction_manager = providers.Singleton(
        SQLAlchemyTransactionManager, session_factory=session_factory
    )
    query_executor = providers.Singleton(
        QueryExecutor, transaction_manager=transaction_manager
    )

    # Auth
    token_black_list = providers.Singleton(JWTTokenBlacklist)
    token_service = providers.Singleton(
        JWTTokenService, black_list=token_black_list, config=auth_config
    )
    auth_service = providers.Singleton(
        MockUserAuthService, token_service=token_service
    )

    # User Query Repositories
    user_query_repository = providers.Singleton(
        UserQueryRepositoryImpl, executor=query_executor
    )
    user_role_query_repository = providers.Singleton(
        UserRoleQueryRepositoryImpl, executor=query_executor
    )
    admin_query_repository = providers.Singleton(
        AdminQueryRepositoryImpl, executor=query_executor
    )

    # User Command Repositories
    admin_command_repository = providers.Singleton(
        AdminCommandRepositoryImpl, executor=query_executor
    )

    # User Query UseCases
    get_user_for_admin_use_case = providers.Singleton(
        GetUserForAdminUseCase, repository=user_role_query_repository
    )
    get_pending_user_use_case = providers.Singleton(
        GetPendingUserUseCase, repository=user_role_query_repository
    )
    get_profile_for_admin_use_case = providers.Singleton(
        GetProfileForAdminUseCase, repository=admin_query_repository
    )

    # UserQuery
    # UseCases
    admin_user_query_service = providers.Singleton(
        AdminUserQueryServiceImpl,
        get_user_use_case=get_user_for_admin_use_case,
        get_pending_user_use_case=get_pending_user_use_case,
        get_profile_use_case=get_profile_for_admin_use_case,
    )
    contractor_user_query_service = providers.Singleton(MockUserAuthService)
    contractee_user_query_service = providers.Singleton(MockUserAuthService)
