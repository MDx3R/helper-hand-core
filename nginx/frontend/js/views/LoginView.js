import { View } from "./View.js";

export class LoginView extends View {
    render({ onRegister, onLogin } = {}) {
        super.render(`
      <div class="auth-container">
        <ul class="nav nav-tabs mb-4" id="authTabs" role="tablist">
          <li class="nav-item">
            <button class="nav-link active" id="login-tab" data-bs-toggle="tab" data-bs-target="#login" type="button" role="tab">Вход</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" id="register-tab" data-bs-toggle="tab" data-bs-target="#register" type="button" role="tab">Регистрация</button>
          </li>
        </ul>
        <div class="tab-content">
          <div class="tab-pane fade show active" id="login" role="tabpanel">
            <form id="loginForm">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" name="username" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input type="password" class="form-control" name="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Войти</button>
              <div class="switch-link"><a href="#">Забыли пароль?</a></div>
              <div class="switch-link">Нет аккаунта? <a href="#" id="toRegister">Зарегистрироваться</a></div>
              <div class="error d-none" id="loginError">Ошибка авторизации</div>
            </div>
          </div>
        </div>
      `);

        this.root.querySelector("#toRegister").onclick = (e) => {
            e.preventDefault();
            if (onRegister) onRegister();
        };

        this.root.querySelector("#register-tab").onclick = () => {
            if (onRegister) onRegister();
        };

        this.root.querySelector("#loginForm").onsubmit = async (e) => {
            e.preventDefault();
            const username = e.target.username.value;
            const password = e.target.password.value;
            const errorDiv = this.root.querySelector("#loginError");
            errorDiv.classList.add("d-none");
            try {
                await onLogin(username, password);
            } catch (err) {
                errorDiv.textContent =
                    "Ошибка авторизации: " + (err?.msg || "Проверьте данные");
                errorDiv.classList.remove("d-none");
            }
        };
    }
}
