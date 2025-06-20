import { BaseTable } from "./Table.js";

export class OrdersTable extends BaseTable {
    constructor(orders, title = "Заказы", addCreateButton = false) {
        super(orders, title);
        this.addCreateButton = addCreateButton;
    }

    render() {
        const createButton = { text: "Создать заказ", action: "create-order" };
        const headerHtml = `
      <th>Название</th>
      <th>Локация</th>
      <th>Статус</th>
      <th>Действия</th>
    `;

        const rowsHtml = this.data
            .map(
                (order) => `
      <tr>
        <td>${order.about}</td>
        <td>${order.address}</td>
        <td><span class="badge bg-warning text-dark">${order.status}</span></td>
        <td>
          <button class="btn btn-primary btn-sm" data-id="${order.order_id}" data-action="order-view">
            Посмотреть
          </button>
        </td>
      </tr>
    `
            )
            .join("");
        return this.renderWrapper(
            rowsHtml,
            headerHtml,
            this.addCreateButton ? createButton : {}
        );
    }

    attachEventHandlers(container, { onView, onCreate } = {}) {
        this.addButtonHandler(container, "order-view", onView, "data-id");
        if (onCreate && this.addCreateButton) {
            this.addButtonHandler(container, "create-order", onCreate);
        }
    }
}

export class PendingOrdersTable extends BaseTable {
    constructor(orders, title = "Ожидающие заказы") {
        super(orders, title);
    }

    render() {
        const headerHtml = `
      <th>Название</th>
      <th>Локация</th>
      <th>Действия</th>
    `;

        const rowsHtml = this.data
            .map(
                (order) => `
      <tr>
        <td>${order.about}</td>
        <td>${order.address}</td>
        <td>
          <button class="btn btn-primary btn-sm" data-id="${order.order_id}" data-action="order-view">
            Посмотреть
          </button>
          <button class="btn btn-success btn-sm" data-id="${order.order_id}" data-action="order-approve">
            Одобрить
          </button>
          <button class="btn btn-danger btn-sm" data-id="${order.order_id}" data-action="order-reject">
            Отклонить
          </button>
        </td>
      </tr>
    `
            )
            .join("");

        return this.renderWrapper(rowsHtml, headerHtml);
    }

    attachEventHandlers(container, { onView, onApprove, onReject } = {}) {
        this.addButtonHandler(container, "order-view", onView, "data-id");
        this.addButtonHandler(
            container,
            "order-approve",
            onApprove,
            "data-id",
            true
        );
        this.addButtonHandler(
            container,
            "order-reject",
            onReject,
            "data-id",
            true
        );
    }
}
