import { Component } from "./Component.js";

export class BaseTable extends Component {
    constructor(data, title) {
        super();
        this.data = data;
        this.title = title;
    }

    renderWrapper(
        innerRowsHtml,
        headerHtml,
        headerButton = { text: "", action: "" }
    ) {
        const noDataMessage = `
            <div class="text-muted text-center py-3">
                Нет данных
            </div>
        `;
        return `
            ${this.renderHeader(headerButton)}
            <div class="table-responsive mb-4">
                <table class="table align-middle mb-0">
                <thead class="table-light">
                    <tr>${headerHtml}</tr>
                </thead>
                    <tbody>${innerRowsHtml || ""}</tbody>
                </table>
                ${innerRowsHtml ? "" : noDataMessage}
            </div>
        `;
    }

    renderHeader({ text, action }) {
        return `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2 class="h5 mb-0">${this.title}</h2>
                ${
                    text
                        ? `<button class="btn btn-create" data-action="${action}">${text}</a>`
                        : ""
                }
            </div>
        `;
    }

    addButtonHandler(
        container,
        action,
        handler,
        getIdAttr = "data-id",
        removeRowOnSuccess = false
    ) {
        container
            .querySelectorAll(`button[data-action="${action}"]`)
            .forEach((btn) => {
                btn.addEventListener("click", async () => {
                    const id = btn.getAttribute(getIdAttr);
                    try {
                        const result = await handler?.(id);
                        if (removeRowOnSuccess && result !== false) {
                            const row = btn.closest("tr");
                            if (row) row.remove();
                        }
                    } catch (err) {
                        console.error(
                            `Error handling ${action} for id=${id}`,
                            err
                        );
                    }
                });
            });
    }
}
