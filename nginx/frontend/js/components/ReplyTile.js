import { calculateTimeUntil } from "../entities/Order.js";
import { Component } from "./Component.js";

export class ReplyTile extends Component {
    constructor(replies = [], title = "Отклики", onClick) {
        super();
        this.replies = replies;
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
            this.replies.length === 0
                ? noDataMessage
                : this.replies
                      .map(
                          ({ reply, detail, order }) => `
                <div class="col-12 col-md-4">
                    <div class="card-order card-hover" data-id="${
                        detail.order_id
                    }">
                        <div class="d-flex justify-content-between fw-semibold mb-1">
                            <div>${detail.position}</div>
                            <div>${calculateTimeUntil(detail)}</div>
                        </div>
                        <div class="text-muted mb-1">${order.address}</div>
                        <div class="fw-semibold">Ставка: ${reply.wager}₽</div>
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
            const replyId = parseInt(cardEl.dataset.id, 10);
            cardEl.addEventListener("click", () => {
                if (typeof this.onClick === "function") {
                    this.onClick(replyId);
                }
            });
        });
    }
}
