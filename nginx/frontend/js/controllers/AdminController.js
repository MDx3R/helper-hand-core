import { MetricsBoard } from "../components/Metrics.js";
import { OrderBlock } from "../components/OrderBlock.js";
import { OrderDetailTable } from "../components/OrderDetailTable.js";
import { OrdersTable, PendingOrdersTable } from "../components/OrdersTable.js";
import { RepliesTable } from "../components/RepliesTable.js";
import { PendingUsersTable } from "../components/UsersTable.js";
import { buildOrderButtons } from "../dao/OrderService.js";
import { wrapWithHandlers } from "../utils.js";
import { Section } from "../views/SectionView.js";

export class AdminController {
    constructor(
        userService,
        orderService,
        metricsService,
        authService,
        dashboardView,
        ordersView,
        profileView,
        navBarView,
        userView,
        onLogout
    ) {
        this.userService = userService;
        this.orderService = orderService;
        this.metricsService = metricsService;
        this.authService = authService;
        this.dashboardView = dashboardView;
        this.ordersView = ordersView;
        this.profileView = profileView;
        this.navBarView = navBarView;
        this.userView = userView;
        this.onLogout = onLogout;
    }

    async showDashboard() {
        ("once");
        const pageName = "dashboard";
        let metrics = {};
        let pendingUsers = [];
        let pendingOrders = [];
        let curatedOrders = [];

        try {
            metrics = await this.metricsService.getAdminMetrics();
            pendingUsers = await this.userService.listPendingUsers();
            pendingOrders = await this.orderService.listPendingOrders();
            curatedOrders = await this.orderService.listOrders();
        } catch (e) {
            console.error(e);
        }

        // Создание метрик
        const metricsBoard = new MetricsBoard(metrics);

        // Создание таблиц
        const usersTable = wrapWithHandlers(
            new PendingUsersTable(pendingUsers),
            {
                onView: (id) => this._viewUserHandler(id),
                onApprove: (id) => this._approveUserHandler(id),
                onReject: (id) => this._disapproveUserHandler(id),
            }
        );

        const pendingOrdersTable = wrapWithHandlers(
            new PendingOrdersTable(pendingOrders, "Ожидающие заказы"),
            {
                onView: (id) => this._viewOrderHandler(id),
                onApprove: (id) => this._approveOrderHandler(id),
                onReject: (id) => this._disapproveOrderHandler(id),
            }
        );

        const curatedOrdersTable = wrapWithHandlers(
            new OrdersTable(curatedOrders, "Курируемые заказы"),
            {
                onView: (id) => this._viewOrderHandler(id),
            }
        );

        // Оборачиваем в секции
        const sections = [
            new Section("metrics", metricsBoard),
            new Section("pending-users", usersTable),
            new Section("pending-orders", pendingOrdersTable),
            new Section("curated-orders", curatedOrdersTable),
        ];

        this.renderNavbar(pageName);
        this.dashboardView.render(sections);
    }

    async showOrders() {}
    async showProfile() {
        const pageName = "profle";
        const composite = await this.userService.getMe();

        this.renderNavbar(pageName);
        this.profileView.render(composite.user, {
            onSubmit: async (userData) =>
                await this._updateProfileHandler(userData),
        });
    }

    async showUser(userId) {
        const pageName = "user";
        const composite = await this.userService.getUser(userId);

        this.renderNavbar(pageName);
        this.userView.render(composite.user, [
            {
                text: "Подтвердить",
                onClick: () => this._approveUserHandler(composite.user.user_id),
            },
            {
                text: "Отклонить",
                onClick: () =>
                    this._disapproveUserHandler(composite.user.user_id),
            },
        ]);
    }
    async showOrder(orderId) {
        const pageName = "order";
        const composite = await this.orderService.getOrder(orderId);
        const replies = [];

        const buttons = buildOrderButtons(composite.order, "admin", {
            approve: () => this._approveOrderHandler(orderId),
            disapprove: () => this._disapproveOrderHandler(orderId),
            setOpen: () => this._openOrderHandler(orderId),
            setClosed: () => this._closeOrderHandler(orderId),
            setCancelled: () => this._cancelOrderHandler(orderId),
            setFulfilled: () => this._fulfillOrderHandler(orderId),
        });
        const orderBlock = new OrderBlock(composite, buttons);
        const detailsTable = wrapWithHandlers(
            new OrderDetailTable(composite.details),
            {}
        );
        const repliesTable = wrapWithHandlers(new RepliesTable(replies), {});

        const sections = [
            new Section("order", orderBlock),
            new Section("details", detailsTable),
            new Section("replies", repliesTable),
        ];
        this.renderNavbar(pageName);
        this.dashboardView.render(sections);
    }

    renderNavbar(active) {
        const navLinks = [
            {
                label: "Дашборд",
                id: "dashboard",
                callback: () => (location.hash = "#dashboard"),
            },
            {
                label: "Профиль",
                id: "profile",
                callback: () => (location.hash = "#profile"),
            },
            {
                label: "Выйти",
                id: "logout",
                callback: async () => {
                    await this._logoutHandler();
                    await this.onLogout();
                },
            },
        ];
        this.navBarView.render(navLinks, active);
    }

    async _logoutHandler() {
        await this.authService.logout();
    }

    async _viewUserHandler(userId) {
        // const pageName = "user";
        // location.hash = `#${pageName}-${userId}`;
        await this.showUser(userId);
    }

    async _updateProfileHandler(userData) {
        return await this.userService.updateProfile(userData);
    }

    async _approveUserHandler(userId) {
        await this.userService.approveUser(userId);
    }

    async _disapproveUserHandler(userId) {
        await this.userService.disapproveUser(userId);
    }

    async _viewOrderHandler(orderId) {
        const pageName = "order";
        location.hash = `#${pageName}/${orderId}`;
    }

    async _approveOrderHandler(orderId) {
        await this.orderService.approveOrder(orderId);
    }

    async _disapproveOrderHandler(orderId) {
        await this.orderService.disapproveOrder(orderId);
    }

    async _openOrderHandler(orderId) {
        await this.orderService.openOrder(orderId);
    }

    async _closeOrderHandler(orderId) {
        await this.orderService.closeOrder(orderId);
    }

    async _cancelOrderHandler(orderId) {
        await this.orderService.cancelOrder(orderId);
    }

    async _fulfillOrderHandler(orderId) {
        await this.orderService.fulfillOrder(orderId);
    }
}
