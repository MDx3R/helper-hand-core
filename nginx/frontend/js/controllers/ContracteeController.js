import { MetricsBoard } from "../components/Metrics.js";
import { OrderBlock } from "../components/OrderBlock.js";
import {
    OrderDetailTable,
    SuitableOrderDetailTable,
} from "../components/OrderDetailTable.js";
import { OrdersTable } from "../components/OrdersTable.js";
import { OrderTile } from "../components/OrderTile.js";
import {
    PendingRepliesTable,
    RepliesInlineTable,
    RepliesTable,
} from "../components/RepliesTable.js";
import { ReplyTile } from "../components/ReplyTile.js";
import { wrapWithHandlers } from "../utils.js";
import { Section } from "../views/SectionView.js";

export class ContracteeController {
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
        this.onLogout = onLogout;
    }

    async showDashboard() {
        const pageName = "dashboard";
        let metrics = {};
        let suitableOrders = [];
        let futureReplies = [];
        let replies = [];

        try {
            metrics = await this.metricsService.getContracteeMetrics();
            suitableOrders = await this.orderService.listSuitableOrders();
            futureReplies = await this.replyService.listFutureReplies();
            replies = await this.replyService.listReplies();
        } catch (e) {
            console.error(e);
        }

        // Создание метрик
        const metricsBoard = new MetricsBoard(metrics);

        // Создание таблиц
        // TODO:
        const suitableOrdersTile = new OrderTile(
            suitableOrders,
            "Рекомендованные заказы",
            (id) => this._viewOrderHandler(id)
        );

        const futureRepliesTile = new ReplyTile(
            futureReplies,
            "Ближайшие выходы",
            (id) => this._viewOrderHandler(id)
        );

        const repliesTable = wrapWithHandlers(new RepliesTable(replies), {
            onView: (id) => this._viewOrderHandler(id),
        });

        // Оборачиваем в секции
        const sections = [
            new Section("metrics", metricsBoard),
            new Section("suitable-orders", suitableOrdersTile),
            new Section("future-replies", futureRepliesTile),
            new Section("replies", repliesTable),
        ];

        this.renderNavbar(pageName);
        this.dashboardView.render(sections);
    }

    async showReplies() {}
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
        const suitableDetails =
            await this.orderService.getSuitableDetailsForOrder(orderId);
        const replies = await this.replyService.listOrderReplies(orderId);
        const orderBlock = new OrderBlock(composite, []);
        const detailsTable = wrapWithHandlers(
            new OrderDetailTable(composite.details, true),
            {}
        );
        const suitableDetailsTable = wrapWithHandlers(
            new SuitableOrderDetailTable(suitableDetails, "Подходящие позиции"),
            { onSubmit: (id) => this._submitReplyHandler(id) }
        );
        const repliesTable = wrapWithHandlers(
            new RepliesTable(replies, "Мои отклики"),
            {}
        );

        const sections = [
            new Section("order", orderBlock),
            new Section("details", detailsTable),
            new Section("suitable-details", suitableDetailsTable),
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

    async _viewOrderHandler(orderId) {
        const pageName = "order";
        location.hash = `#${pageName}/${orderId}`;
    }

    async _updateProfileHandler(userData) {
        return await this.userService.updateProfile(userData);
    }

    async _submitReplyHandler(detailId) {
        await this.replyService.submitReply(detailId);
    }
}
