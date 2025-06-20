import { BaseTable } from "./Table.js";

export class RepliesTable extends BaseTable {
    constructor(replies, title = "Отклики") {
        super(replies, title);
    }

    render() {
        const headerHtml = `
      <th>Адрес</th>
      <th>Позиция</th>
      <th>Дата</th>
      <th>Время</th>
      <th>Ставка</th>
      <th>Статус</th>
      <th>Действия</th>
    `;

        const rowsHtml = this.data
            .map((completeReply) => {
                const { contractee, detail, reply, order } = completeReply;
                return `
      <tr>
        <td>${order ? order.address : ""}</td>
        <td>${detail ? detail.position : ""}</td>
        <td>${detail ? detail.date : ""}</td>
        <td>${detail ? `${detail.start_at}-${detail.end_at}` : ""}</td>
        <td>${reply.wager}</td>
        <td><span class="badge bg-warning text-dark">${
            reply.dropped ? "dropped" : reply.status
        }</span></td>
        <td>
          <button class="btn btn-primary btn-sm" data-id="${
              detail.order_id
          }" data-action="reply-view">
            Посмотреть
          </button>
        </td>
      </tr>
    `;
            })
            .join("");

        return this.renderWrapper(rowsHtml, headerHtml);
    }

    attachEventHandlers(container, { onView } = {}) {
        this.addButtonHandler(container, "reply-view", onView, "data-id");
    }
}

export class RepliesInlineTable extends BaseTable {
    constructor(replies, title = "Отклики") {
        super(replies, title);
    }

    render() {
        const headerHtml = `
      <th>Имя Исполнителя</th>
      <th>Позиция</th>
      <th>Дата</th>
      <th>Время</th>
      <th>Статус</th>
    `;

        const rowsHtml = this.data
            .map((completeReply) => {
                const { contractee, detail, reply } = completeReply;
                return `
      <tr>
        <td>${contractee ? `${contractee.surname} ${contractee.name}` : ""}</td>
        <td>${detail ? detail.position : ""}</td>
        <td>${detail ? detail.date : ""}</td>
        <td>${detail ? `${detail.start_at}-${detail.end_at}` : ""}</td>
        <td><span class="badge bg-warning text-dark">${
            reply.dropped ? "dropped" : reply.status
        }</span></td>
      </tr>
    `;
            })
            .join("");

        return this.renderWrapper(rowsHtml, headerHtml);
    }

    attachEventHandlers(container, { onView } = {}) {
        this.addButtonHandler(container, "reply-view", onView, "data-id");
    }
}

export class PendingRepliesTable extends BaseTable {
    constructor(replies, title = "Отклики") {
        super(replies, title);
    }

    render() {
        const headerHtml = `
      <th>Имя Исполнителя</th>
      <th>Позиция</th>
      <th>Дата</th>
      <th>Время</th>
      <th>Статус</th>
      <th>Действия</th>
    `;

        const rowsHtml = this.data
            .map((completeReply) => {
                const { contractee, detail, reply } = completeReply;
                return `
      <tr>
        <td>${contractee ? `${contractee.surname} ${contractee.name}` : ""}</td>
        <td>${detail ? detail.position : ""}</td>
        <td>${detail ? detail.date : ""}</td>
        <td>${detail ? `${detail.start_at}-${detail.end_at}` : ""}</td>
        <td><span class="badge bg-warning text-dark">${
            reply.dropped ? "dropped" : reply.status
        }</span></td>
        <td>
          <button class="btn btn-primary btn-sm" data-id="${
              reply.contractee_id
          }" data-action="reply-view">
            Посмотреть
          </button>
          <button class="btn btn-success btn-sm" data-id="${reply.detail_id}-${
                    reply.contractee_id
                }" data-action="reply-approve">
            Одобрить
          </button>
          <button class="btn btn-danger btn-sm" data-id="${reply.detail_id}-${
                    reply.contractee_id
                }" data-action="reply-reject">
            Отклонить
          </button>
        </td>
      </tr>
    `;
            })
            .join("");

        return this.renderWrapper(rowsHtml, headerHtml);
    }

    attachEventHandlers(container, { onView, onApprove, onReject } = {}) {
        this.addButtonHandler(container, "reply-view", onView, "data-id");
        this.addButtonHandler(
            container,
            "reply-approve",
            onApprove,
            "data-id",
            true
        );
        this.addButtonHandler(
            container,
            "reply-reject",
            onReject,
            "data-id",
            true
        );
    }
}
