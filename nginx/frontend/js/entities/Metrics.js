function mapFields(instance, labels, extraFields = []) {
    const result = {};
    for (const key in labels) {
        result[key] = {
            label: labels[key],
            value: instance[key],
            extra: extraFields.includes(key),
        };
    }
    return result;
}
export class ContracteeMetrics {
    constructor({
        replies,
        accepted_replies,
        orders_with_accepted_replies,
        earned,
        hours_worked,
        average_wager,
    }) {
        this.replies = replies;
        this.accepted_replies = accepted_replies;
        this.orders_with_accepted_replies = orders_with_accepted_replies;
        this.earned = earned;
        this.hours_worked = hours_worked;
        this.average_wager = average_wager;
    }

    toLabeledObject() {
        const labels = {
            replies: "Отклики",
            accepted_replies: "Принятые отклики",
            orders_with_accepted_replies: "Заказы с принятыми откликами",
            earned: "Заработано",
            hours_worked: "Отработано часов",
            average_wager: "Средняя ставка",
        };

        const extraFields = [
            "orders_with_accepted_replies",
            "average_wager",
            "accepted_replies",
        ];
        return mapFields(this, labels, extraFields);
    }
}
export class AdminMetrics {
    constructor({
        orders,
        open_orders,
        active_orders,
        completed_orders,
        amount,
        hours_worked,
    }) {
        this.orders = orders;
        this.open_orders = open_orders;
        this.active_orders = active_orders;
        this.completed_orders = completed_orders;
        this.amount = amount;
        this.hours_worked = hours_worked;
    }

    toLabeledObject() {
        const labels = {
            orders: "Всего заказов",
            open_orders: "Открытые заказы",
            active_orders: "Активные заказы",
            completed_orders: "Завершённые заказы",
            amount: "Общая сумма",
            hours_worked: "Отработано часов",
        };

        const extraFields = ["amount", "hours_worked", "completed_orders"];
        return mapFields(this, labels, extraFields);
    }
}

export class ContractorMetrics {
    constructor({
        orders,
        open_orders,
        active_orders,
        completed_orders,
        replies,
        pending_replies,
        spent,
        hours_worked,
    }) {
        this.orders = orders;
        this.open_orders = open_orders;
        this.active_orders = active_orders;
        this.completed_orders = completed_orders;
        this.replies = replies;
        this.pending_replies = pending_replies;
        this.spent = spent;
        this.hours_worked = hours_worked;
    }

    toLabeledObject() {
        const labels = {
            orders: "Всего заказов",
            open_orders: "Открытые заказы",
            active_orders: "Активные заказы",
            completed_orders: "Завершённые заказы",
            replies: "Отклики",
            pending_replies: "Ожидающие отклики",
            spent: "Потрачено",
            hours_worked: "Отработано часов",
        };

        const extraFields = [
            "active_orders",
            "completed_orders",
            "replies",
            "spent",
            "hours_worked",
        ];
        return mapFields(this, labels, extraFields);
    }
}
export class AppMetrics {
    constructor({ users, orders, replies, total_amount, average_wager }) {
        this.users = users;
        this.orders = orders;
        this.replies = replies;
        this.total_amount = total_amount;
        this.average_wager = average_wager;
    }

    toLabeledObject() {
        const labels = {
            users: "Пользователи",
            orders: "Заказы",
            replies: "Отклики",
            total_amount: "Общая сумма",
            average_wager: "Средняя ставка",
        };

        const extraFields = ["total_amount"];
        return mapFields(this, labels, extraFields);
    }
}
