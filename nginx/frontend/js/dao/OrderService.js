import { resolvePagination } from "../dto/Pagination.js";
import {
    ADMIN_BASE,
    CONTRACTOR_BASE,
    CONTRACTEE_BASE,
    Methods,
} from "./HttpClient.js";
import {
    Order,
    CompleteOrder,
    OrderDetail,
    OrderWithDetails,
} from "../entities/Order.js";

const ORDERS_BASE = "orders";

export class OrderService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = ORDERS_BASE;
    }

    async listOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}${query ? `?${query}` : ""}`,
            Methods.GET,
            {},
            {},
            false
        );
        return data.map((o) => new Order(o));
    }
}

export class AdminOrderService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = `${ADMIN_BASE}/${ORDERS_BASE}`;
    }

    async createOrder(orderData) {
        const data = await this.httpClient.request(
            `/${this.base}`,
            Methods.POST,
            orderData
        );
        return new OrderWithDetails(data);
    }

    async listOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}${query ? `?${query}` : ""}`
        );
        return data.map((o) => new Order(o));
    }

    async listPendingOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/pending${query ? `?${query}` : ""}`
        );
        return data.map((o) => new Order(o));
    }

    async getOrder(orderId) {
        const data = await this.httpClient.request(`/${this.base}/${orderId}`);
        return new CompleteOrder(data);
    }

    async takeOrder(orderId) {
        return await this.performAction(orderId, "take");
    }

    async approveOrder(orderId) {
        return await this.performAction(orderId, "approve");
    }

    async disapproveOrder(orderId) {
        return await this.performAction(orderId, "disapprove");
    }

    async cancelOrder(orderId) {
        return await this.performAction(orderId, "cancel");
    }

    async closeOrder(orderId) {
        return await this.performAction(orderId, "close");
    }

    async openOrder(orderId) {
        return await this.performAction(orderId, "open");
    }

    async setActiveOrder(orderId) {
        return await this.performAction(orderId, "set-active");
    }

    async fulfillOrder(orderId) {
        return await this.performAction(orderId, "fulfill");
    }

    async performAction(orderId, action) {
        const data = await this.httpClient.request(
            `/${this.base}/${orderId}/${action}`,
            Methods.POST
        );
        return new Order(data);
    }
}

export class ContractorOrderService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = `${CONTRACTOR_BASE}/${ORDERS_BASE}`;
    }

    async createOrder(orderData) {
        const data = await this.httpClient.request(
            `/${this.base}`,
            Methods.POST,
            orderData
        );
        return new OrderWithDetails(data);
    }

    async listOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}${query ? `?${query}` : ""}`
        );
        return data.map((o) => new Order(o));
    }

    async getOrder(orderId) {
        const data = await this.httpClient.request(`/${this.base}/${orderId}`);
        return new CompleteOrder(data);
    }

    async cancelOrder(orderId) {
        return await this.performAction(orderId, "cancel");
    }

    async setActive(orderId) {
        return await this.performAction(orderId, "set-active");
    }

    async performAction(orderId, action) {
        const data = await this.httpClient.request(
            `/${this.base}/${orderId}/${action}`,
            Methods.POST
        );
        return new Order(data);
    }
}

export class ContracteeOrderService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = `${CONTRACTEE_BASE}/${ORDERS_BASE}`;
    }

    async listOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}${query ? `?${query}` : ""}`
        );
        return data.map((o) => new Order(o));
    }

    async listSuitableOrders(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/suitable${query ? `?${query}` : ""}`
        );
        return data.map((o) => new OrderWithDetails(o));
    }

    async getSuitableDetailsForOrder(orderId) {
        const data = await this.httpClient.request(
            `/${this.base}/suitable/${orderId}`
        );
        return data.map((d) => new OrderDetail(d));
    }

    async getOrder(orderId) {
        const data = await this.httpClient.request(`/${this.base}/${orderId}`);
        return new CompleteOrder(data);
    }
}

export const buildOrderButtons = (order, role, handlers) => {
    const buttons = [];

    const status = order.status;
    const isAdmin = role === "admin";
    const isContractor = role === "contarctor";

    const isCreated = status === "created";
    const isOpen = status === "open";
    const isClosed = status === "closed";
    const isActive = status === "active";
    const isCancelled = status === "cancelled";
    const isFulfilled = status === "fulfilled";

    // Admin-only actions
    if (isAdmin) {
        if (isCreated) {
            buttons.push({
                text: "Подтвердить",
                onClick: () => handlers.approve(order.id),
            });
            buttons.push({
                text: "Отклонить",
                danger: true,
                onClick: () => handlers.disapprove(order.id),
            });
        }

        if (isClosed) {
            buttons.push({
                text: "Открыть",
                onClick: () => handlers.setOpen(order.id),
            });
        }

        if (isOpen) {
            buttons.push({
                text: "Закрыть",
                onClick: () => handlers.setClosed(order.id),
            });
        }

        if (isActive) {
            buttons.push({
                text: "Выполнен",
                onClick: () => handlers.setFulfilled(order.id),
            });
        }
    }

    // Customer + Admin
    if (!isCancelled && !isFulfilled) {
        buttons.push({
            text: "Отменить",
            danger: true,
            onClick: () => handlers.setCancelled(order.id),
        });
    }

    // Customer-only
    if (isContractor && (isOpen || isClosed)) {
        buttons.push({
            text: "Сделать активным",
            onClick: () => handlers.setActive(order.id),
        });
    }

    return buttons;
};
