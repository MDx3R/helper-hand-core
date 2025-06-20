import { Component } from "./Component.js";

export class OrderFormComponent extends Component {
    constructor(onSubmit) {
        super();
        this.onSubmit = onSubmit;
    }

    render() {
        return `
            <div class="create-order-block">
                <h2 class="mb-4">Создание заказа</h2>
                <form id="orderForm">
                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <label class="form-label">Описание заказа</label>
                            <textarea class="form-control" name="description" rows="1" required></textarea>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Адрес</label>
                            <input type="text" class="form-control" name="address" required>
                        </div>
                    </div>
                    <hr class="my-4">
                    <h5 class="mb-3">Позиции</h5>
                    <div id="detailsList" class="row row-cols-1 g-3">
                        ${this.renderDetailBlock()}
                    </div>
                    <button type="button" class="btn btn-outline-dark btn-sm mb-3 mt-3" id="addDetailBtn">Добавить позицию</button>
                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark">Создать заказ</button>
                    </div>
                    <div class="error d-none" id="orderError">Ошибка создания заказа</div>
                </form>
            </div>
        `;
    }

    renderDetailBlock() {
        return `
            <div class="col">
                <div class="card p-3 position-relative order-detail-row">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Дата</label>
                            <input type="date" class="form-control" name="date[]" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Начало</label>
                            <input type="time" class="form-control" name="startTime[]" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Окончание</label>
                            <input type="time" class="form-control" name="endTime[]" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Позиция</label>
                            <select class="form-select" name="position[]" required>
                                <option value="">Выберите...</option>
                                <option value="Хелпер">Хелпер</option>
                                <option value="Хостес">Хостес</option>
                                <option value="Монтажник">Монтажник</option>
                                <option value="Парковщик">Парковщик</option>
                                <option value="Другая">Другая</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Пол</label>
                            <select class="form-select" name="gender[]">
                                <option value="">Любой</option>
                                <option value="Мужской">Мужской</option>
                                <option value="Женский">Женский</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Кол-во</label>
                            <input type="number" class="form-control" name="count[]" required min="1">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Ставка, ₽</label>
                            <input type="number" class="form-control" name="rate[]" required min="0">
                        </div>
                    </div>
                    <button type="button" class="btn-close position-absolute top-0 end-0 m-2 remove-detail" aria-label="Удалить"></button>
                </div>
            </div>
        `;
    }

    attachEventHandlers(container) {
        const form = container.querySelector("#orderForm");
        const errorBlock = container.querySelector("#orderError");

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            errorBlock.classList.add("d-none");

            try {
                const data = this.extractFormData(form);
                await this.onSubmit(data);
            } catch (err) {
                errorBlock.textContent =
                    err?.message || "Ошибка создания заказа";
                errorBlock.classList.remove("d-none");
            }
        });

        container
            .querySelector("#addDetailBtn")
            .addEventListener("click", () => {
                const list = container.querySelector("#detailsList");
                const temp = document.createElement("div");
                temp.innerHTML = this.renderDetailBlock();
                list.appendChild(temp.firstElementChild);
            });

        container
            .querySelector("#detailsList")
            .addEventListener("click", (e) => {
                if (e.target.classList.contains("remove-detail")) {
                    const block = e.target.closest(".col");
                    if (block) block.remove();
                }
            });
    }

    extractFormData(form) {
        const formData = new FormData(form);
        const about = formData.get("description");
        const address = formData.get("address");

        const positions = [];
        const count = formData.getAll("count[]").length;

        for (let i = 0; i < count; i++) {
            const gender = formData.getAll("gender[]")[i];
            positions.push({
                date: formData.getAll("date[]")[i],
                start_at: formData.getAll("startTime[]")[i],
                end_at: formData.getAll("endTime[]")[i],
                position: formData.getAll("position[]")[i],
                gender: gender ? gender : null,
                count: Number(formData.getAll("count[]")[i]),
                wager: Number(formData.getAll("rate[]")[i]),
            });
        }

        return { order: { about, address }, details: positions };
    }
}
