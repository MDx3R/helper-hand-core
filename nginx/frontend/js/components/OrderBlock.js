import { concatFullname } from "../entities/User.js";
import { Component } from "./Component.js";

export class OrderBlock extends Component {
    constructor(compositeOrder, buttons = []) {
        super();
        this.compositeOrder = compositeOrder;
        this.buttons = buttons;
    }

    render() {
        const { admin, contractor, order } = this.compositeOrder;
        const { about, address, order_id, status } = order;
        const contractorFullname = concatFullname(contractor);
        const adminFullname = admin ? concatFullname(admin) : "Не назначен";

        const buttonsHtml = this.buttons
            .map(
                (btn, index) => `
                <button class="btn btn-sm ${
                    btn.danger ? "btn-primary" : "btn-secondary"
                }" data-action="action-${index}">
                    ${btn.text}
                </button>`
            )
            .join("");

        return `
            <div class="order-block">
                <div class="order-header">Заказ №${order_id}</div>
                <div class="order-meta">
                    Адрес: ${address} | Статус: 
                    <span class="badge ${
                        status == "open" ? "bg-success" : "bg-secondary"
                    } badge-status">${status}</span>
                </div>
                <div class="order-meta">
                    Заказчик: ${contractorFullname} | Администратор: ${adminFullname}
                </div>
                <div class="mb-2">Описание: ${about}</div>
                <div class="d-flex gap-2 mb-2">
                    ${buttonsHtml}
                </div>
            </div>
        `;
    }

    attachEventHandlers(container) {
        this.buttons.forEach((btn, index) => {
            if (typeof btn.onClick === "function") {
                const button = container.querySelector(
                    `[data-action="action-${index}"]`
                );
                if (button) {
                    button.addEventListener("click", btn.onClick);
                }
            }
        });
    }
}
