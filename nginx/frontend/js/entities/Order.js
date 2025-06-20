export class Order {
    constructor({ about, address, order_id, contractor_id, status, admin_id }) {
        this.about = about;
        this.address = address;
        this.order_id = order_id;
        this.contractor_id = contractor_id;
        this.status = status;
        this.admin_id = admin_id;
    }
}

export class OrderDetail {
    constructor({
        date,
        start_at,
        end_at,
        position,
        gender,
        count,
        wager,
        fee,
        detail_id,
        order_id,
    }) {
        this.date = date;
        this.start_at = start_at;
        this.end_at = end_at;
        this.position = position;
        this.gender = gender;
        this.count = count;
        this.wager = wager;
        this.fee = fee;
        this.detail_id = detail_id;
        this.order_id = order_id;
    }
}

export class OrderWithDetails {
    constructor({ order, details }) {
        this.order = order;
        this.details = details;
    }
}

export class CompleteOrder {
    constructor({ order, details, contractor, admin }) {
        this.order = order;
        this.details = details;
        this.contractor = contractor;
        this.admin = admin;
    }
}

export function calculateAverageWager(details = [], reduceWager = false) {
    return details.reduce(
        (sum, detail) =>
            reduceWager ? sum + detail.wager - detail.fee : sum + detail.wager,
        0
    );
}

export function calculateTimeUntil({ date, start_at }) {
    const now = new Date();
    const target = new Date(`${date}T${start_at}`);

    const diffMs = target - now;
    const diffMinutes = Math.floor(diffMs / 60000);

    if (diffMinutes <= 0) return "Скоро";

    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays >= 1) {
        return `Через ${diffDays} ${pluralize(
            diffDays,
            "день",
            "дня",
            "дней"
        )}`;
    }

    return `Через ${diffHours} ${pluralize(diffHours, "час", "часа", "часов")}`;
}
