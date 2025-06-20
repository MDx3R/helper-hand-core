import { calculateAverageWager } from "../entities/Order.js";
import { Component } from "./Component.js";

export class OrderTile extends Component {
    constructor(compositeOrders = [], title = "Заказы", onClick) {
        super();
        this.compositeOrders = compositeOrders;
        this.title = title;
        this.onClick = onClick;
    }

    render() {
        const noDataMessage = `
            <div class="text-muted text-center py-3">
                Нет данных
            </div>
        `;

        const cardsHtml =
            this.compositeOrders.length === 0
                ? noDataMessage
                : this.compositeOrders
                      .map(
                          ({ order, details }) => `
                    <div class="col-12 col-md-4">
                        <div class="card-order card-hover" data-id="${
                            order.order_id
                        }">
                            <div class="fw-semibold mb-1">Заказ №${
                                order.order_id
                            }</div>
                            <div class="text-muted mb-1">${order.address}</div>
                            <div class="fw-semibold">Средняя ставка: ${calculateAverageWager(
                                details,
                                true
                            )}₽</div>
                        </div>
                    </div>
                `
                      )
                      .join("");

        return `
            <h2 class="h5 mb-3">${this.title}</h2>
            <div class="row g-3 mb-4">
                ${cardsHtml}
            </div>
        `;
    }

    attachEventHandlers(container) {
        const cardElements = container.querySelectorAll(".card-order");

        cardElements.forEach((cardEl) => {
            const orderId = parseInt(cardEl.dataset.id, 10);
            cardEl.addEventListener("click", () => this.onClick(orderId));
        });
    }
}
