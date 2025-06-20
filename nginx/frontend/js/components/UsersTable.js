import { BaseTable } from "./Table.js";

export class PendingUsersTable extends BaseTable {
    constructor(users, title = "Ожидающие пользователи") {
        super(users, title);
    }

    render() {
        const headerHtml = `
      <th>Имя</th>
      <th>Роль</th>
      <th>Действия</th>
    `;

        const rowsHtml = this.data
            .map(
                (user) => `
      <tr>
        <td>${user.surname} ${user.name} ${user.patronymic || ""}</td>
        <td>${user.role}</td>
        <td>
          <button class="btn btn-primary btn-sm" data-id="${
              user.user_id
          }" data-action="user-view">Посмотреть</button>
          <button class="btn btn-success btn-sm" data-id="${
              user.user_id
          }" data-action="user-approve">Одобрить</button>
          <button class="btn btn-danger btn-sm" data-id="${
              user.user_id
          }" data-action="user-reject">Отклонить</button>
        </td>
      </tr>
    `
            )
            .join("");

        return this.renderWrapper(rowsHtml, headerHtml);
    }

    attachEventHandlers(container, { onView, onApprove, onReject } = {}) {
        this.addButtonHandler(container, "user-view", onView, "data-id");
        this.addButtonHandler(
            container,
            "user-approve",
            onApprove,
            "data-id",
            true
        );
        this.addButtonHandler(
            container,
            "user-reject",
            onReject,
            "data-id",
            true
        );
    }
}
