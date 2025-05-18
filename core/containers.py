from dependency_injector import containers, providers
from application.external.password_hasher import BcryptPasswordHasher
from application.services.auth.user_auth_service import (
    JWTTokenBlacklist,
    JWTTokenService,
    MockUserAuthService,
    UserAuthServiceImpl,
)
from application.services.user.admin_user_service import (
    AdminUserQueryServiceImpl,
)
from application.services.user.contractee_user_service import (
    ContracteeUserQueryServiceImpl,
)
from application.services.user.contractor_user_service import (
    ContractorUserQueryServiceImpl,
)
from application.usecases.auth.login_use_case import LoginUseCase
from application.usecases.auth.create_user_use_case import (
    CreateContracteeUseCase,
    CreateContractorUseCase,
    CreateCredentialsUseCase,
)
from application.usecases.auth.register_user_use_case import (
    RegisterContracteeUseCase,
    RegisterContractorUseCase,
)
from application.usecases.user.admin.get_pending_user_use_case import (
    GetPendingUserUseCase,
)
from application.usecases.user.admin.get_user_use_case import (
    GetProfileForAdminUseCase,
    GetUserForAdminUseCase,
)
from application.usecases.user.contractee.get_user_use_case import (
    GetProfileForContracteeUseCase,
    GetUserForContracteeUseCase,
)
from application.usecases.user.contractor.get_user_use_case import (
    GetProfileForContractorUseCase,
    GetUserForContractorUseCase,
)
from application.usecases.user.user_query_use_case import (
    GetProfileForUserUseCase,
)
from core.config import Config
from domain.entities import user
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from infrastructure.database.database import (
    Database,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.token.token_command_repository import (
    TokenCommandRepositoryImpl,
)
from infrastructure.repositories.token.token_query_repository import (
    TokenQueryRepositoryImpl,
)
from infrastructure.repositories.user.admin.admin_command_repository import (
    AdminCommandRepositoryImpl,
)
from infrastructure.repositories.user.admin.admin_query_repository import (
    AdminQueryRepositoryImpl,
)
from infrastructure.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepositoryImpl,
)
from infrastructure.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepositoryImpl,
)
from infrastructure.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepositoryImpl,
)
from infrastructure.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepositoryImpl,
)
from infrastructure.repositories.user.user_command_repository import (
    UserCommandRepositoryImpl,
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
    contractor_query_repository = providers.Singleton(
        ContractorQueryRepositoryImpl, executor=query_executor
    )
    contractee_query_repository = providers.Singleton(
        ContracteeQueryRepositoryImpl, executor=query_executor
    )

    # User Command Repositories
    user_command_repository = providers.Singleton(
        UserCommandRepositoryImpl, executor=query_executor
    )
    admin_command_repository = providers.Singleton(
        AdminCommandRepositoryImpl, executor=query_executor
    )
    contractee_command_repository = providers.Singleton(
        ContracteeCommandRepositoryImpl, executor=query_executor
    )
    contractor_command_repository = providers.Singleton(
        ContractorCommandRepositoryImpl, executor=query_executor
    )

    # Token Repositories
    token_query_repository = providers.Singleton(
        TokenQueryRepositoryImpl, executor=query_executor
    )
    token_command_repository = providers.Singleton(
        TokenCommandRepositoryImpl, executor=query_executor
    )

    # Auth
    token_black_list = providers.Singleton(JWTTokenBlacklist)
    password_hasher = providers.Singleton(BcryptPasswordHasher)
    token_service = providers.Singleton(
        JWTTokenService,
        query_repository=token_query_repository,
        command_repository=token_command_repository,
        black_list=token_black_list,
        config=auth_config,
    )

    # Create Users UseCase
    create_credentials_use_case = providers.Singleton(
        CreateCredentialsUseCase,
        user_command_repository=user_command_repository,
        password_hasher=password_hasher,
    )
    create_contractee_use_case = providers.Singleton(
        CreateContracteeUseCase,
        create_credentials_use_case=create_credentials_use_case,
        contractee_command_repository=contractee_command_repository,
    )
    create_contractor_use_case = providers.Singleton(
        CreateContractorUseCase,
        create_credentials_use_case=create_credentials_use_case,
        contractor_command_repository=contractor_command_repository,
    )

    register_contractee_use_case = providers.Singleton(
        RegisterContracteeUseCase,
        token_service=token_service,
        create_contractee_use_case=create_contractee_use_case,
    )
    register_contractor_use_case = providers.Singleton(
        RegisterContractorUseCase,
        token_service=token_service,
        create_contractor_use_case=create_contractor_use_case,
    )

    login_use_case = providers.Singleton(
        LoginUseCase,
        token_service=token_service,
        password_hasher=password_hasher,
        user_query_repository=user_query_repository,
    )
    auth_service = providers.Singleton(
        UserAuthServiceImpl,
        login_use_case=login_use_case,
        register_contractee_use_case=register_contractee_use_case,
        register_contractor_use_case=register_contractor_use_case,
    )

    # User Query UseCases
    get_profile_for_user_use_case = providers.Singleton(
        GetProfileForUserUseCase, repository=user_query_repository
    )

    # Admin
    get_user_for_admin_use_case = providers.Singleton(
        GetUserForAdminUseCase, repository=user_role_query_repository
    )
    get_pending_user_use_case = providers.Singleton(
        GetPendingUserUseCase, repository=user_role_query_repository
    )
    get_profile_for_admin_use_case = providers.Singleton(
        GetProfileForAdminUseCase, repository=admin_query_repository
    )

    # Contractor
    get_user_for_contractor_use_case = providers.Singleton(
        GetUserForContractorUseCase, repository=user_role_query_repository
    )
    get_profile_for_contractor_use_case = providers.Singleton(
        GetProfileForContractorUseCase, repository=contractor_query_repository
    )

    # Contractor
    get_user_for_contractee_use_case = providers.Singleton(
        GetUserForContracteeUseCase, repository=user_role_query_repository
    )
    get_profile_for_contractee_use_case = providers.Singleton(
        GetProfileForContracteeUseCase, repository=contractee_query_repository
    )

    # UserQuery
    # UseCases
    admin_user_query_service = providers.Singleton(
        AdminUserQueryServiceImpl,
        get_user_use_case=get_user_for_admin_use_case,
        get_pending_user_use_case=get_pending_user_use_case,
        get_profile_use_case=get_profile_for_admin_use_case,
    )
    contractor_user_query_service = providers.Singleton(
        ContractorUserQueryServiceImpl,
        get_user_use_case=get_user_for_contractor_use_case,
        get_profile_use_case=get_profile_for_contractor_use_case,
    )
    contractee_user_query_service = providers.Singleton(
        ContracteeUserQueryServiceImpl,
        get_user_use_case=get_user_for_contractee_use_case,
        get_profile_use_case=get_profile_for_contractee_use_case,
    )
