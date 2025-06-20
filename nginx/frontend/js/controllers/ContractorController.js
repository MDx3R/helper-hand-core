import { MetricsBoard } from "../components/Metrics.js";
import { OrderBlock } from "../components/OrderBlock.js";
import { OrderDetailTable } from "../components/OrderDetailTable.js";
import { OrderFormComponent } from "../components/OrderFormComponent.js";
import { OrdersTable } from "../components/OrdersTable.js";
import {
    PendingRepliesTable,
    RepliesInlineTable,
    RepliesTable,
} from "../components/RepliesTable.js";
import { buildOrderButtons } from "../dao/OrderService.js";
import { wrapWithHandlers } from "../utils.js";
import { Section } from "../views/SectionView.js";

export class ContractorController {
    constructor(
        userService,
        orderService,
        replyService,
        metricsService,
        authService,
        dashboardView,
        ordersView,
        profileView,
        navBarView,
        userView,
        createOrderView,
        onLogout
    ) {
        this.userService = userService;
        this.orderService = orderService;
        this.replyService = replyService;
        this.metricsService = metricsService;
        this.authService = authService;
        this.dashboardView = dashboardView;
        this.ordersView = ordersView;
        this.profileView = profileView;
        this.navBarView = navBarView;
        this.userView = userView;
        this.createOrderView = createOrderView;
        this.onLogout = onLogout;
    }

    async showDashboard() {
        const pageName = "dashboard";
        let metrics = {};
        let orders = [];
        let pendingReplies = [];

        try {
            metrics = await this.metricsService.getContractorMetrics();
            orders = await this.orderService.listOrders();
            pendingReplies = await this.replyService.listPendingReplies();
        } catch (e) {
            error(e);
        }

        // Создание метрик
        const metricsBoard = new MetricsBoard(metrics);

        // Создание таблиц
        const pendingRepliesTable = wrapWithHandlers(
            new PendingRepliesTable(pendingReplies, "Ожидающие отклики"),
            {
                onView: (id) => this._viewUserHandler(id),
                onApprove: (id) => this._approveReplyHandler(id),
                onReject: (id) => this._disapproveReplyHandler(id),
            }
        );

        const ordersTable = wrapWithHandlers(
            new OrdersTable(orders, "Недавние заказы", true),
            {
                onView: (id) => this._viewOrderHandler(id),
                onCreate: () => {
                    this._viewCreateOrderHandler();
                },
            }
        );

        // Оборачиваем в секции
        const sections = [
            new Section("metrics", metricsBoard),
            new Section("pending-replies", pendingRepliesTable),
            new Section("orders", ordersTable),
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
        this.userView.render(composite.user, []);
    }
    async showOrder(orderId) {
        const pageName = "order";
        const composite = await this.orderService.getOrder(orderId);
        const replies = await this.replyService.listOrderReplies(orderId);

        const buttons = buildOrderButtons(composite.order, "contractor", {
            setCancelled: () => this._cancelOrderHandler(orderId),
            setActive: () => this._activateOrderHandler(orderId),
        });
        const orderBlock = new OrderBlock(composite, buttons);
        const detailsTable = wrapWithHandlers(
            new OrderDetailTable(composite.details),
            {}
        );
        const pendingRepliesTable = wrapWithHandlers(
            new PendingRepliesTable(replies),
            {
                onView: (id) => this._viewUserHandler(id),
                onApprove: (compositeId) =>
                    this._approveReplyHandler(...compositeId.split("-")),
                onReject: (compositeId) =>
                    this._disapproveReplyHandler(...compositeId.split("-")),
            }
        );
        const repliesTable = wrapWithHandlers(
            new RepliesInlineTable(replies),
            {}
        );

        const sections = [
            new Section("order", orderBlock),
            new Section("details", detailsTable),
            new Section("pending-replies", pendingRepliesTable),
            new Section("replies", repliesTable),
        ];
        this.renderNavbar(pageName);
        this.dashboardView.render(sections);
    }
    async showCreateOrder() {
        const pageName = "create-order";

        this.renderNavbar(pageName);
        this.createOrderView.render({
            onSubmit: async (orderData) => {
                this._createOrderHandler(orderData);
            },
        });
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

    async _viewCreateOrderHandler() {
        const pageName = "create-order";
        location.hash = `#${pageName}`;
    }

    async _viewUserHandler(userId) {
        // const pageName = "user";
        // location.hash = `#${pageName}-${userId}`;
        await this.showUser(userId);
    }

    async _viewOrderHandler(orderId) {
        const pageName = "order";
        location.hash = `#${pageName}/${orderId}`;
    }

    async _createOrderHandler(orderData) {
        const composite = await this.orderService.createOrder(orderData);
        location.hash = `#order/${composite.order.order_id}`;
    }

    async _updateProfileHandler(userData) {
        return await this.userService.updateProfile(userData);
    }

    async _cancelOrderHandler(orderId) {
        await this.orderService.cancelOrder(orderId);
    }

    async _activateOrderHandler(orderId) {
        await this.orderService.setActive(orderId);
    }

    async _approveReplyHandler(detailId, userId) {
        await this.replyService.approveReply(detailId, userId);
    }

    async _disapproveReplyHandler(detailId, userId) {
        await this.replyService.disapproveReply(detailId, userId);
    }
}
