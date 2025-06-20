import { BaseTable } from "./Table.js";

export class OrderDetailTable extends BaseTable {
    constructor(orderDetails, reduceWager = false, title = "Позиции заказа") {
        super(orderDetails, title);
        this.reduceWager = reduceWager;
    }

    render() {
        return this.renderWrapper(this._renderRows(), this._renderHeader());
    }

    _renderHeader() {
        return `<th>Дата</th>
                <th>Время</th>
                <th>Позиция</th>
                <th>Пол</th>
                <th>Кол-во</th>
                <th>Ставка (Комиссия ${
                    this.reduceWager ? "учтена" : "не учтена"
                })</th>`;
    }

    _renderRows() {
        return this.data
            .map(
                (item) => `
                        <tr>
                            <td>${item.date}</td>
                            <td>${item.start_at}-${item.start_at}</td>
                            <td>${item.position}</td>
                            <td>${item.gender ? item.gender : "Любой"}</td>
                            <td>${item.count}</td>
                            <td>${
                                this.reduceWager
                                    ? item.wager - item.fee
                                    : item.wager
                            }₽</td>
                        </tr>
                    `
            )
            .join("");
    }

    attachEventHandlers(container, handlers = {}) {
        // Здесь можно добавить обработчики на строки или кнопки, если нужно.
        // Пример:
        // this.addRowClickHandler(container, "order-detail-row", handlers.onRowClick);
    }
}

export class SuitableOrderDetailTable extends BaseTable {
    constructor(orderDetails, title = "Позиции заказа") {
        super(orderDetails, title);
        this.reduceWager = true;
    }

    render() {
        return this.renderWrapper(this._renderRows(), this._renderHeader());
    }

    _renderHeader() {
        return `<th>Дата</th>
                <th>Время</th>
                <th>Позиция</th>
                <th>Пол</th>
                <th>Кол-во</th>
                <th>Ставка (Комиссия ${
                    this.reduceWager ? "учтена" : "не учтена"
                })</th>
                <th>Действия</th>`;
    }

    _renderRows() {
        return this.data
            .map(
                (item) => `
                        <tr>
                            <td>${item.date}</td>
                            <td>${item.start_at}-${item.start_at}</td>
                            <td>${item.position}</td>
                            <td>${item.gender ? item.gender : "Любой"}</td>
                            <td>${item.count}</td>
                            <td>${
                                this.reduceWager
                                    ? item.wager - item.fee
                                    : item.wager
                            }₽</td>
                            <td>
                                <button class="btn btn-primary btn-sm" data-id="${
                                    item.detail_id
                                }" data-action="submit-reply">
                                    Откликнуться
                                </button>
                            </td>
                        </tr>
                    `
            )
            .join("");
    }

    attachEventHandlers(container, handlers = {}) {
        this.addButtonHandler(
            container,
            "submit-reply",
            handlers.onSubmit,
            "data-id",
            true
        );
    }
}
