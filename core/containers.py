from dependency_injector import containers, providers
from application.external.metrics.metrics_repository import MetricsRepository
from application.external.password_hasher import BcryptPasswordHasher
from application.services.auth.user_auth_service import (
    JWTTokenBlacklist,
    JWTTokenService,
    UserAuthServiceImpl,
)
from application.services.metrics.metrics_service import MetricsServiceImpl
from application.services.order.admin_order_service import (
    AdminOrderManagementServiceImpl,
    AdminOrderQueryServiceImpl,
)
from application.services.order.contractee_order_service import (
    ContracteeOrderQueryServiceImpl,
)
from application.services.order.contractor_order_service import (
    ContractorOrderManagementServiceImpl,
    ContractorOrderQueryServiceImpl,
)
from application.services.order.order_query_service import (
    OrderQueryServiceImpl,
)
from application.services.reply.contractee_reply_service import (
    ContracteeReplyManagmentServiceImpl,
    ContracteeReplyQueryServiceImpl,
)
from application.services.reply.contractor_reply_service import (
    ContractorReplyManagmentServiceImpl,
    ContractorReplyQueryServiceImpl,
)
from application.services.user.admin_user_service import (
    AdminUserManagementServiceImpl,
    AdminUserQueryServiceImpl,
)
from application.services.user.contractee_user_service import (
    ContracteeUserQueryServiceImpl,
)
from application.services.user.contractor_user_service import (
    ContractorUserQueryServiceImpl,
)
from application.services.user_photo_service import PhotoServiceImpl
from application.usecases.auth.login_use_case import (
    LoginUseCase,
    LogoutUseCase,
)
from application.usecases.auth.create_user_use_case import (
    CreateContracteeUseCase,
    CreateContractorUseCase,
    CreateCredentialsUseCase,
)
from application.usecases.auth.register_user_use_case import (
    RegisterContracteeUseCase,
    RegisterContractorUseCase,
)
from application.usecases.metrics.get_admin_metrics_use_case import (
    GetAdminMetricsUseCase,
)
from application.usecases.metrics.get_app_metrics_use_case import (
    GetAppMetricsUseCase,
)
from application.usecases.metrics.get_contractee_metrics_use_case import (
    GetContracteeMetricsUseCase,
)
from application.usecases.metrics.get_contractor_metrics_use_case import (
    GetContractorMetricsUseCase,
)
from application.usecases.order.admin.create_order_use_case import (
    CreateOrderForAdminUseCase,
)
from application.usecases.order.admin.get_order_use_case import (
    GetOrderForAdminUseCase,
)
from application.usecases.order.admin.get_unassigned_order_use_case import (
    GetUnassignedOrderUseCase,
    ListUnassignedOrdersUseCase,
)
from application.usecases.order.admin.list_supervised_orders_use_case import (
    ListSupervisedOrdersUseCase,
)
from application.usecases.order.admin.take_order_use_case import (
    TakeOrderUseCase,
)
from application.usecases.order.change_order_status_use_case import (
    ApproveOrderUseCase,
    CancelOrderUseCase,
    CloseOrderUseCase,
    DisapproveOrderUseCase,
    FulfillOrderUseCase,
    OpenOrderUseCase,
    SetActiveOrderUseCase,
)
from application.usecases.order.contractee.get_suitable_order_use_case import (
    GetSuitableDetailsFromOrderUseCase,
    GetSuitableDetailsForOrderUseCase,
    GetSuitableOrderUseCase,
    GetUnavailableDetailsForContracteeUseCase,
    ListSuitableOrdersUseCase,
)
from application.usecases.order.contractor.create_order_use_case import (
    CreateOrderForContractorUseCase,
)
from application.usecases.order.contractor.get_order_use_case import (
    GetOrderForContractorUseCase,
)
from application.usecases.order.contractor.list_owned_orders_use_case import (
    ListOwnedOrdersUseCase,
)
from application.usecases.order.order_query_use_case import (
    ListRecentOrdersUseCase,
)
from application.usecases.reply.contractee.create_reply_use_case import (
    CreateReplyUseCase,
)
from application.usecases.reply.contractee.get_reply_use_case import (
    GetReplyForContracteeUseCase,
)
from application.usecases.reply.contractee.list_future_replies_use_case import (
    ListFutureRepliesForContracteeUseCase,
)
from application.usecases.reply.contractee.list_submitted_replies_use_case import (
    ListSubmittedRepliesForContracteeUseCase,
    ListSubmittedRepliesForOrderAndContracteeUseCase,
)
from application.usecases.reply.contractor.change_reply_status_use_case import (
    ApproveReplyUseCase,
    DisapproveReplyUseCase,
)
from application.usecases.reply.contractor.get_pending_reply_use_case import (
    GetPendingReplyForOrderUseCase,
    GetPendingReplyUseCase,
    ListPendingRepliesForOrderUseCase,
    ListPendingRepliesUseCase,
)
from application.usecases.reply.contractor.get_reply_use_case import (
    GetReplyForContractorUseCase,
)
from application.usecases.reply.contractor.list_order_replies_use_case import (
    ListDetailRepliesForContractorUseCase,
    ListOrderRepliesForContractorUseCase,
)
from application.usecases.user.admin.chage_user_status_use_case import (
    ApproveUserUseCase,
    BanUserUseCase,
    ChangeUserStatusUseCase,
    DisapproveUserUseCase,
    DropUserUseCase,
)
from application.usecases.user.admin.get_pending_user_use_case import (
    ListPendingUsersUseCase,
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
from application.usecases.user.update_user_use_case import (
    UpdateAdminUseCase,
    UpdateContracteeUseCase,
    UpdateContractorUseCase,
)
from application.usecases.user.user_photo_use_case import (
    GetPhotoUseCase,
    RemovePhotoUseCase,
    UploadPhotoUseCase,
)
from application.usecases.user.user_query_use_case import (
    GetProfileForUserUseCase,
)
from core.config import Config
from domain.services.user.admin_user_service import AdminUserManagementService
from infrastructure.database.database import (
    Database,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.metrics.metrics_service import (
    MetricsRepositoryImpl,
)
from infrastructure.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepositoryImpl,
)
from infrastructure.repositories.order.detail.order_detail_command_repository import (
    OrderDetailCommandRepositoryImpl,
)
from infrastructure.repositories.order.detail.order_detail_query_repository import (
    OrderDetailQueryRepositoryImpl,
)
from infrastructure.repositories.order.order_command_repository import (
    OrderCommandRepositoryImpl,
)
from infrastructure.repositories.order.order_query_repository import (
    OrderQueryRepositoryImpl,
)
from infrastructure.repositories.photos.local_photo_storage import (
    LocalPhotoStorage,
)
from infrastructure.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepositoryImpl,
)
from infrastructure.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepositoryImpl,
)
from infrastructure.repositories.reply.reply_command_repository import (
    ReplyCommandRepositoryImpl,
)
from infrastructure.repositories.reply.reply_query_repository import (
    ReplyQueryRepositoryImpl,
)
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

    # TODO: Resources

    # ---------------------- Config ----------------------
    config = providers.Singleton(Config.load)
    auth_config = config.provided.auth
    db_config = config.provided.db

    # ---------------------- Database ----------------------
    database = providers.Singleton(Database, config=db_config)
    session_factory = providers.Singleton(
        lambda db: db.get_session_factory(), database
    )
    transaction_manager = providers.Singleton(
        SQLAlchemyTransactionManager, session_factory=session_factory
    )
    query_executor = providers.Singleton(QueryExecutor, transaction_manager)

    # ---------------------- Repositories ----------------------

    # --- User Repositories ---
    user_query_repository = providers.Singleton(
        UserQueryRepositoryImpl, query_executor
    )
    user_role_query_repository = providers.Singleton(
        UserRoleQueryRepositoryImpl, query_executor
    )
    admin_query_repository = providers.Singleton(
        AdminQueryRepositoryImpl, query_executor
    )
    contractor_query_repository = providers.Singleton(
        ContractorQueryRepositoryImpl, query_executor
    )
    contractee_query_repository = providers.Singleton(
        ContracteeQueryRepositoryImpl, query_executor
    )

    user_command_repository = providers.Singleton(
        UserCommandRepositoryImpl, query_executor
    )
    admin_command_repository = providers.Singleton(
        AdminCommandRepositoryImpl, query_executor
    )
    contractor_command_repository = providers.Singleton(
        ContractorCommandRepositoryImpl, query_executor
    )
    contractee_command_repository = providers.Singleton(
        ContracteeCommandRepositoryImpl, query_executor
    )

    # --- Order Repositories ---
    order_query_repository = providers.Singleton(
        OrderQueryRepositoryImpl, query_executor
    )
    composite_order_query_repository = providers.Singleton(
        CompositeOrderQueryRepositoryImpl, query_executor
    )
    order_command_repository = providers.Singleton(
        OrderCommandRepositoryImpl, query_executor
    )
    order_detail_query_repository = providers.Singleton(
        OrderDetailQueryRepositoryImpl, query_executor
    )
    order_detail_command_repository = providers.Singleton(
        OrderDetailCommandRepositoryImpl, query_executor
    )

    # --- Reply Repositories ---
    reply_query_repository = providers.Singleton(
        ReplyQueryRepositoryImpl, query_executor
    )
    reply_command_repository = providers.Singleton(
        ReplyCommandRepositoryImpl, query_executor
    )
    composite_reply_query_repository = providers.Singleton(
        CompositeReplyQueryRepositoryImpl, query_executor
    )
    contractee_reply_query_repository = providers.Singleton(
        ContracteeReplyQueryRepositoryImpl, query_executor
    )

    # --- Token Repositories ---
    token_query_repository = providers.Singleton(
        TokenQueryRepositoryImpl, query_executor
    )
    token_command_repository = providers.Singleton(
        TokenCommandRepositoryImpl, query_executor
    )

    # --- Metrics Repositories ---
    metrics_repository = providers.Singleton(
        MetricsRepositoryImpl, query_executor
    )
    # --- Photo Storage ---
    photo_storage = providers.Singleton(LocalPhotoStorage)

    # ---------------------- Auth ----------------------
    token_black_list = providers.Singleton(JWTTokenBlacklist)
    password_hasher = providers.Singleton(BcryptPasswordHasher)
    token_service = providers.Singleton(
        JWTTokenService,
        query_repository=token_query_repository,
        command_repository=token_command_repository,
        black_list=token_black_list,
        config=auth_config,
    )

    # ---------------------- UseCases ----------------------

    # --- Create Users ---
    create_credentials_use_case = providers.Singleton(
        CreateCredentialsUseCase, user_command_repository, password_hasher
    )
    create_contractee_use_case = providers.Singleton(
        CreateContracteeUseCase,
        create_credentials_use_case,
        contractee_command_repository,
    )
    create_contractor_use_case = providers.Singleton(
        CreateContractorUseCase,
        create_credentials_use_case,
        contractor_command_repository,
    )

    register_contractee_use_case = providers.Singleton(
        RegisterContracteeUseCase, token_service, create_contractee_use_case
    )
    register_contractor_use_case = providers.Singleton(
        RegisterContractorUseCase, token_service, create_contractor_use_case
    )

    login_use_case = providers.Singleton(
        LoginUseCase, token_service, password_hasher, user_query_repository
    )
    logout_use_case = providers.Singleton(
        LogoutUseCase,
        token_query_repository=token_query_repository,
        token_command_repository=token_command_repository,
        token_blacklist=token_black_list,
        token_service=token_service,
    )

    # --- Profile & Role UseCases ---
    get_profile_for_user_use_case = providers.Singleton(
        GetProfileForUserUseCase, user_query_repository
    )

    get_user_for_admin_use_case = providers.Singleton(
        GetUserForAdminUseCase, user_role_query_repository
    )
    get_profile_for_admin_use_case = providers.Singleton(
        GetProfileForAdminUseCase, admin_query_repository
    )

    get_user_for_contractor_use_case = providers.Singleton(
        GetUserForContractorUseCase, user_role_query_repository
    )
    get_profile_for_contractor_use_case = providers.Singleton(
        GetProfileForContractorUseCase, contractor_query_repository
    )

    get_user_for_contractee_use_case = providers.Singleton(
        GetUserForContracteeUseCase, user_role_query_repository
    )
    get_profile_for_contractee_use_case = providers.Singleton(
        GetProfileForContracteeUseCase, contractee_query_repository
    )

    list_pending_users_use_case = providers.Singleton(
        ListPendingUsersUseCase, user_query_repository
    )
    change_user_status_use_case = providers.Singleton(
        ChangeUserStatusUseCase, user_query_repository, user_command_repository
    )
    approve_user_use_case = providers.Singleton(
        ApproveUserUseCase, change_user_status_use_case
    )
    disapprove_user_use_case = providers.Singleton(
        DisapproveUserUseCase, change_user_status_use_case
    )
    drop_user_use_case = providers.Singleton(
        DropUserUseCase, change_user_status_use_case
    )
    ban_user_use_case = providers.Singleton(
        BanUserUseCase, change_user_status_use_case
    )

    update_contractor_use_case = providers.Singleton(
        UpdateContractorUseCase,
        contractor_query_repository=contractor_query_repository,
        contractor_command_repository=contractor_command_repository,
    )
    update_contractee_use_case = providers.Singleton(
        UpdateContracteeUseCase,
        contractee_query_repository=contractee_query_repository,
        contractee_command_repository=contractee_command_repository,
    )
    update_admin_use_case = providers.Singleton(
        UpdateAdminUseCase,
        admin_query_repository=admin_query_repository,
        admin_command_repository=admin_command_repository,
    )

    # --- Orders ---
    get_order_for_admin_use_case = providers.Singleton(
        GetOrderForAdminUseCase, composite_order_query_repository
    )
    get_order_for_contracor_use_case = providers.Singleton(
        GetOrderForContractorUseCase, composite_order_query_repository
    )
    get_suitable_details_from_order_use_case = providers.Singleton(
        GetSuitableDetailsFromOrderUseCase
    )
    get_unavailable_details_for_contractee_use_case = providers.Singleton(
        GetUnavailableDetailsForContracteeUseCase,
        composite_reply_query_repository,
    )
    get_suitable_details_use_case = providers.Singleton(
        GetSuitableDetailsForOrderUseCase,
        order_repository=composite_order_query_repository,
        reply_repository=composite_reply_query_repository,
        contractee_repository=contractee_query_repository,
        unavailable_details_use_case=get_unavailable_details_for_contractee_use_case,
        filtering_use_case=get_suitable_details_from_order_use_case,
    )

    list_recent_orders_use_case = providers.Singleton(
        ListRecentOrdersUseCase, order_query_repository
    )
    list_unassigned_orders_use_case = providers.Singleton(
        ListUnassignedOrdersUseCase, order_query_repository
    )
    list_supervised_orders_use_case = providers.Singleton(
        ListSupervisedOrdersUseCase, order_query_repository
    )
    list_owned_orders_use_case = providers.Singleton(
        ListOwnedOrdersUseCase, order_query_repository
    )
    list_suitable_orders_use_case = providers.Singleton(
        ListSuitableOrdersUseCase,
        order_repository=composite_order_query_repository,
        contractee_repository=contractee_query_repository,
        filtering_use_case=get_suitable_details_from_order_use_case,
        unavailable_details_use_case=get_unavailable_details_for_contractee_use_case,
    )
    get_suitable_order_use_case = providers.Singleton(
        GetSuitableOrderUseCase,
        list_suitable_orders_use_case=list_suitable_orders_use_case,
        order_repository=composite_order_query_repository,
    )
    create_order_for_admin_use_case = providers.Singleton(
        CreateOrderForAdminUseCase,
        order_command_repository,
        order_detail_command_repository,
    )
    create_order_for_contractor_use_case = providers.Singleton(
        CreateOrderForContractorUseCase,
        order_command_repository,
        order_detail_command_repository,
    )
    take_order_use_case = providers.Singleton(
        TakeOrderUseCase, order_query_repository, order_command_repository
    )
    approve_order_use_case = providers.Singleton(
        ApproveOrderUseCase, order_query_repository, order_command_repository
    )
    disapprove_order_use_case = providers.Singleton(
        DisapproveOrderUseCase,
        order_query_repository,
        order_command_repository,
    )
    cancel_order_use_case = providers.Singleton(
        CancelOrderUseCase, order_query_repository, order_command_repository
    )
    close_order_use_case = providers.Singleton(
        CloseOrderUseCase, order_query_repository, order_command_repository
    )
    open_order_use_case = providers.Singleton(
        OpenOrderUseCase, order_query_repository, order_command_repository
    )
    set_order_active_use_case = providers.Singleton(
        SetActiveOrderUseCase, order_query_repository, order_command_repository
    )
    fulfill_order_use_case = providers.Singleton(
        FulfillOrderUseCase, order_query_repository, order_command_repository
    )

    # --- Reply ---
    create_reply_use_case = providers.Singleton(
        CreateReplyUseCase,
        contractee_repository=contractee_query_repository,
        order_repository=order_query_repository,
        detail_repository=order_detail_query_repository,
        reply_query_repository=reply_query_repository,
        reply_command_repository=reply_command_repository,
        contractee_reply_repository=contractee_reply_query_repository,
    )
    get_reply_for_contractee_use_case = providers.Singleton(
        GetReplyForContracteeUseCase,
        composite_reply_query_repository,
    )
    get_reply_for_contractor_use_case = providers.Singleton(
        GetReplyForContractorUseCase,
        order_repository=order_query_repository,
        reply_repository=composite_reply_query_repository,
    )
    list_pending_replies_use_case = providers.Singleton(
        ListPendingRepliesUseCase,
        order_repository=order_query_repository,
        reply_repository=composite_reply_query_repository,
    )
    list_pending_replies_for_order_use_case = providers.Singleton(
        ListPendingRepliesForOrderUseCase,
        order_repository=order_query_repository,
        reply_repository=composite_reply_query_repository,
    )
    get_pending_reply_use_case = providers.Singleton(
        GetPendingReplyUseCase, list_pending_replies_use_case
    )
    get_pending_reply_for_order_use_case = providers.Singleton(
        GetPendingReplyForOrderUseCase, list_pending_replies_for_order_use_case
    )
    list_order_replies_for_contractor_use_case = providers.Singleton(
        ListOrderRepliesForContractorUseCase,
        composite_reply_query_repository,
    )
    list_detail_replies_for_contractor_use_case = providers.Singleton(
        ListDetailRepliesForContractorUseCase,
        composite_reply_query_repository,
    )
    list_submitted_replies_use_case = providers.Singleton(
        ListSubmittedRepliesForContracteeUseCase,
        composite_reply_query_repository,
    )
    list_submitted_replies_for_order_use_case = providers.Singleton(
        ListSubmittedRepliesForOrderAndContracteeUseCase,
        composite_reply_query_repository,
    )
    list_future_replies_for_contractee_use_case = providers.Singleton(
        ListFutureRepliesForContracteeUseCase,
        composite_reply_query_repository,
    )
    approve_reply_use_case = providers.Singleton(
        ApproveReplyUseCase,
        reply_query_repository=reply_query_repository,
        reply_command_repository=reply_command_repository,
        composite_reply_query_repository=composite_reply_query_repository,
        order_repository=order_command_repository,
    )
    disapprove_reply_use_case = providers.Singleton(
        DisapproveReplyUseCase,
        reply_command_repository=reply_command_repository,
        composite_reply_query_repository=composite_reply_query_repository,
    )

    # --- Metrics ---
    get_app_metrics_use_case = providers.Singleton(
        GetAppMetricsUseCase, metrics_repository
    )
    get_admin_metrics_use_case = providers.Singleton(
        GetAdminMetricsUseCase, metrics_repository
    )
    get_contractee_metrics_use_case = providers.Singleton(
        GetContracteeMetricsUseCase, metrics_repository
    )
    get_contractor_metrics_use_case = providers.Singleton(
        GetContractorMetricsUseCase, metrics_repository
    )

    # --- Photo ---
    get_photo_use_case = providers.Singleton(
        GetPhotoUseCase,
        photo_storage=photo_storage,
        user_query_repository=user_query_repository,
    )
    upload_photo_use_case = providers.Singleton(
        UploadPhotoUseCase,
        photo_storage=photo_storage,
        user_query_repository=user_query_repository,
        user_command_repository=user_command_repository,
    )
    remove_photo_use_case = providers.Singleton(
        RemovePhotoUseCase,
        photo_storage=photo_storage,
        user_query_repository=user_query_repository,
        user_command_repository=user_command_repository,
    )

    # ---------------------- Services (Facades) ----------------------

    # --- Auth ---
    auth_service = providers.Singleton(
        UserAuthServiceImpl,
        login_use_case=login_use_case,
        logout_use_case=logout_use_case,
        register_contractor_use_case=register_contractor_use_case,
        register_contractee_use_case=register_contractee_use_case,
    )

    # --- Users ---
    admin_user_query_service = providers.Singleton(
        AdminUserQueryServiceImpl,
        get_user_use_case=get_user_for_admin_use_case,
        list_pending_users_use_case=list_pending_users_use_case,
        get_profile_use_case=get_profile_for_admin_use_case,
        update_admin_use_case=update_admin_use_case,
    )
    admin_user_managment_service = providers.Singleton(
        AdminUserManagementServiceImpl,
        approve_user_use_case=approve_user_use_case,
        disapprove_user_use_case=disapprove_user_use_case,
        drop_user_use_case=drop_user_use_case,
        ban_user_use_case=ban_user_use_case,
        notification_service=None,  # TODO: inject service
    )
    contractor_user_query_service = providers.Singleton(
        ContractorUserQueryServiceImpl,
        get_user_use_case=get_user_for_contractor_use_case,
        get_profile_use_case=get_profile_for_contractor_use_case,
        update_contractor_use_case=update_contractor_use_case,
    )
    contractee_user_query_service = providers.Singleton(
        ContracteeUserQueryServiceImpl,
        get_user_use_case=get_user_for_contractee_use_case,
        get_profile_use_case=get_profile_for_contractee_use_case,
        update_contractee_use_case=update_contractee_use_case,
    )

    # --- Orders ---
    order_query_service = providers.Singleton(
        OrderQueryServiceImpl,
        list_recent_orders_use_case=list_recent_orders_use_case,
    )

    admin_order_query_service = providers.Singleton(
        AdminOrderQueryServiceImpl,
        get_order_use_case=get_order_for_admin_use_case,
        get_orders_use_case=list_supervised_orders_use_case,
        list_unassigned_orders_use_case=list_unassigned_orders_use_case,
    )
    admin_order_managment_service = providers.Singleton(
        AdminOrderManagementServiceImpl,
        create_order_use_case=create_order_for_admin_use_case,
        take_order_use_case=take_order_use_case,
        approve_order_use_case=approve_order_use_case,
        disapprove_order_use_case=disapprove_order_use_case,
        cancel_order_use_case=cancel_order_use_case,
        close_order_use_case=close_order_use_case,
        open_order_use_case=open_order_use_case,
        set_order_active_use_case=set_order_active_use_case,
        fulfill_order_use_case=fulfill_order_use_case,
        contractee_notification_service=None,  # TODO: inject service
        contractor_notification_service=None,  # TODO: inject service
    )

    contractor_order_query_service = providers.Singleton(
        ContractorOrderQueryServiceImpl,
        get_order_use_case=get_order_for_contracor_use_case,
        get_orders_use_case=list_owned_orders_use_case,
    )
    contractor_order_managment_service = providers.Singleton(
        ContractorOrderManagementServiceImpl,
        create_order_use_case=create_order_for_contractor_use_case,
        cancel_order_use_case=cancel_order_use_case,
        set_order_active_use_case=set_order_active_use_case,
        admin_notification_service=None,  # TODO: inject service
        contractee_notification_service=None,  # TODO: inject service
    )

    contractee_order_query_service = providers.Singleton(
        ContracteeOrderQueryServiceImpl,
        get_order_use_case=get_order_for_contracor_use_case,
        get_orders_use_case=list_owned_orders_use_case,
        list_suitable_orders_use_case=list_suitable_orders_use_case,
        get_suitable_details_use_case=get_suitable_details_use_case,
    )

    # --- Reply ---

    contractor_reply_query_service = providers.Singleton(
        ContractorReplyQueryServiceImpl,
        get_reply_use_case=get_reply_for_contractor_use_case,
        list_pending_replies_use_case=list_pending_replies_use_case,
        list_pending_replies_for_order_use_case=list_pending_replies_for_order_use_case,
        get_order_replies_use_case=list_order_replies_for_contractor_use_case,
        get_detail_replies_use_case=list_detail_replies_for_contractor_use_case,
    )
    contractor_reply_managment_service = providers.Singleton(
        ContractorReplyManagmentServiceImpl,
        approve_reply_use_case=approve_reply_use_case,
        disapprove_reply_use_case=disapprove_reply_use_case,
        contractee_notification_service=None,  # TODO: inject service
    )

    contractee_reply_query_service = providers.Singleton(
        ContracteeReplyQueryServiceImpl,
        get_reply_use_case=get_reply_for_contractee_use_case,
        get_replies_use_case=list_submitted_replies_use_case,
        get_order_replies_use_case=list_submitted_replies_for_order_use_case,
        get_future_replies_use_case=list_future_replies_for_contractee_use_case,
    )
    contractee_reply_managment_service = providers.Singleton(
        ContracteeReplyManagmentServiceImpl,
        create_reply_use_case=create_reply_use_case,
        contractor_notification_service=None,  # TODO: inject service
    )

    # --- Metrics ---
    metrics_service = providers.Singleton(
        MetricsServiceImpl,
        get_app_metrics_use_case=get_app_metrics_use_case,
        get_admin_metrics_use_case=get_admin_metrics_use_case,
        get_contractee_metrics_use_case=get_contractee_metrics_use_case,
        get_contractor_metrics_use_case=get_contractor_metrics_use_case,
    )

    photo_service = providers.Singleton(
        PhotoServiceImpl,
        get_photo_use_case=get_photo_use_case,
        upload_photo_use_case=upload_photo_use_case,
        remove_photo_use_case=remove_photo_use_case,
    )
