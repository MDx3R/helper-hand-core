import { View } from "./View.js";

export class RegisterView extends View {
    render({ onLogin, onRegisterContractor, onRegisterContractee } = {}) {
        let step = 1;
        let formData = {};

        const renderStep = () => {
            super.render(`
        <div class="auth-container">
          <ul class="nav nav-tabs mb-4" id="authTabs" role="tablist">
            <li class="nav-item">
              <button class="nav-link" id="login-tab" data-bs-toggle="tab" data-bs-target="#login" type="button" role="tab">Вход</button>
            </li>
            <li class="nav-item">
              <button class="nav-link active" id="register-tab" data-bs-toggle="tab" data-bs-target="#register" type="button" role="tab">Регистрация</button>
            </li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane fade show active" id="register" role="tabpanel">
              ${this.renderRegisterStep(step, formData)}
            </div>
          </div>
        </div>
      `);

            const loginTab = this.root.querySelector("#login-tab");
            if (onLogin) {
                loginTab.onclick = onLogin;
            }

            if (step === 1) {
                this.root.querySelector("#registerStep1").onsubmit = (e) => {
                    e.preventDefault();
                    formData.email = e.target.email.value;
                    formData.password = e.target.password.value;
                    step = 2;
                    renderStep();
                };
                this.root.querySelector("#toLogin").onclick = (e) => {
                    e.preventDefault();
                    if (onLogin) onLogin();
                };
            }
            if (step === 2) {
                this.root.querySelector("#registerStep2").onsubmit = (e) => {
                    e.preventDefault();
                    formData.surname = e.target.surname.value;
                    formData.name = e.target.name.value;
                    formData.patronymic = e.target.patronymic.value;
                    formData.phone = e.target.phone.value;
                    formData.role = e.target.role.value;
                    step = 3;
                    renderStep();
                };
                this.root.querySelector("#backStep2").onclick = () => {
                    step = 1;
                    renderStep();
                };
            }
            if (step === 3) {
                this.root.querySelector("#registerStep3").onsubmit = async (
                    e
                ) => {
                    e.preventDefault();
                    let credentials = {
                        web: {
                            email: formData.email,
                            password: formData.password,
                        },
                    };
                    let user = {};
                    if (formData.role === "contractor") {
                        user = {
                            surname: formData.surname,
                            name: formData.name,
                            patronymic: formData.patronymic,
                            phone_number: formData.phone,
                            company: e.target.company?.value || "",
                            inn: e.target.inn?.value || "",
                            about: e.target.about?.value || "",
                            photos: formData.photos || [],
                        };
                    } else if (formData.role === "contractee") {
                        user = {
                            surname: formData.surname,
                            name: formData.name,
                            patronymic: formData.patronymic,
                            phone_number: formData.phone,
                            birthday: e.target.birthday?.value || "",
                            height: e.target.height?.value || "",
                            gender: e.target.gender?.value || "",
                            citizenship: e.target.citizenship?.value || "",
                            positions: Array.from(e.target.positions || [])
                                .filter((input) => input.checked)
                                .map((input) => input.value),
                            about: e.target.about?.value || "",
                            photos: formData.photos || [],
                        };
                    }

                    const errorDiv = this.root.querySelector("#registerError");
                    errorDiv.classList.add("d-none");
                    try {
                        if (formData.role === "contractor") {
                            await onRegisterContractor({ credentials, user });
                        } else if (formData.role === "contractee") {
                            await onRegisterContractee({ credentials, user });
                        } else {
                            throw { msg: "Выберите роль" };
                        }
                    } catch (err) {
                        errorDiv.textContent =
                            "Ошибка регистрации: " +
                            (err?.msg || "Проверьте данные");
                        errorDiv.classList.remove("d-none");
                    }
                };
                this.root.querySelector("#backStep3").onclick = () => {
                    step = 2;
                    renderStep();
                };
            }
        };

        renderStep();
    }

    renderRegisterStep(step, data = {}) {
        if (step === 1) {
            return `
        <form id="registerStep1">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" name="email" value="${
                data.email || ""
            }" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Пароль</label>
            <input type="password" class="form-control" name="password" required>
          </div>
          <button type="submit" class="btn btn-primary w-100">Далее</button>
          <div class="switch-link">Уже есть аккаунт? <a href="#" id="toLogin">Войти</a></div>
          <div class="error d-none" id="registerError">Ошибка регистрации</div>
        </form>`;
        }
        if (step === 2) {
            return `
        <form id="registerStep2">
          <div class="mb-3">
            <label class="form-label">Фамилия</label>
            <input type="text" class="form-control" name="surname" value="${
                data.surname || ""
            }" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Имя</label>
            <input type="text" class="form-control" name="name" value="${
                data.name || ""
            }" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Отчество (опционально)</label>
            <input type="text" class="form-control" name="patronymic" value="${
                data.patronymic || ""
            }">
          </div>
          <div class="mb-3">
            <label class="form-label">Телефон</label>
            <input type="tel" class="form-control" name="phone" value="${
                data.phone || ""
            }" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Роль</label>
            <select class="form-select" name="role" required>
              <option value="">Выберите роль</option>
              <option value="contractor" ${
                  data.role === "contractor" ? "selected" : ""
              }>Заказчик</option>
              <option value="contractee" ${
                  data.role === "contractee" ? "selected" : ""
              }>Исполнитель</option>
            </select>
          </div>
          <button type="button" class="btn btn-secondary me-2" id="backStep2">Назад</button>
          <button type="submit" class="btn btn-primary">Далее</button>
          <div class="error d-none" id="registerError">Ошибка регистрации</div>
        </form>`;
        }
        if (step === 3) {
            if (data.role === "contractor") {
                return `
          <form id="registerStep3">
            <div class="mb-3">
              <label class="form-label">Компания (опционально)</label>
              <input type="text" class="form-control" name="company" value="${
                  data.company || ""
              }">
            </div>
            <div class="mb-3">
              <label class="form-label">ИНН (опционально)</label>
              <input type="text" class="form-control" name="inn" value="${
                  data.inn || ""
              }">
            </div>
            <div class="mb-3">
              <label class="form-label">О себе</label>
              <textarea class="form-control" name="about">${
                  data.about || ""
              }</textarea>
            </div>
            <button type="button" class="btn btn-secondary me-2 mb-3" id="backStep3">Назад</button>
            <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
            <div class="error d-none" id="registerError">Ошибка регистрации</div>
          </form>`;
            } else if (data.role === "contractee") {
                return `
          <form id="registerStep3">
            <div class="mb-3">
              <label class="form-label">Дата рождения</label>
              <input type="date" class="form-control" name="birthday" value="${
                  data.birthday || ""
              }" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Рост (в см)</label>
              <input type="number" class="form-control" name="height" value="${
                  data.height || ""
              }" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Пол</label>
              <select class="form-select" name="gender" required>
                <option value="" disabled selected>Выберите пол</option>
                <option value="Мужской">Мужской</option>
                <option value="Женский">Женский</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Гражданство</label>
              <select class="form-select" name="citizenship" required>
                <option value="" disabled selected>Выберите гражданство</option>
                <option value="Российское">Россия</option>
                <option value="Другое">Другое</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">Желаемые позиции</label>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="positions" value="Хелпер" id="positionHelper">
                <label class="form-check-label" for="positionHelper">Хелпер</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="positions" value="Хостес" id="positionHostess">
                <label class="form-check-label" for="positionHostess">Хостес</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="positions" value="Монтажник" id="positionInstaller">
                <label class="form-check-label" for="positionInstaller">Монтажник</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="positions" value="Парковщик" id="positionValet">
                <label class="form-check-label" for="positionValet">Парковщик</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="positions" value="Другая" id="positionOther">
                <label class="form-check-label" for="positionOther">Другая</label>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">О себе</label>
              <textarea class="form-control" name="about">${
                  data.about || ""
              }</textarea>
            </div>
            <button type="button" class="btn btn-secondary me-2 mb-3" id="backStep3">Назад</button>
            <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
            <div class="error d-none" id="registerError">Ошибка регистрации</div>
          </form>`;
            } else {
                return '<div class="error">Не выбрана роль</div>';
            }
        }
    }
}
