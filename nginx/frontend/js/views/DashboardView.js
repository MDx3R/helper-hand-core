import { View } from "./View.js";

export async function showDashboardView() {
    let user = null;
    try {
        user = await UserService.getMe();
    } catch (e) {
        document.getElementById(
            "app"
        ).innerHTML = `<div class="alert alert-danger">Ошибка загрузки профиля. Попробуйте войти снова.</div>`;
        return;
    }
    document.getElementById("app").innerHTML = `
    <div class="col-md-8 mx-auto">
      <div class="card mb-4">
        <div class="card-body">
          <h3 class="card-title mb-3">Добро пожаловать, ${user.name} ${user.surname}!</h3>
          <p class="card-text"><b>Роль:</b> ${user.role}</p>
          <p class="card-text"><b>Статус:</b> ${user.status}</p>
          <a href="#profile" class="btn btn-outline-primary me-2">Профиль</a>
          <a href="#orders" class="btn btn-outline-secondary">Мои заказы</a>
        </div>
      </div>
      <div class="alert alert-info">Это ваша главная страница. Здесь будет отображаться актуальная информация и быстрые действия.</div>
    </div>
  `;
}

// Contractor Dashboard View (example)
export class ContractorDashboardView extends View {
    render({ metrics, lastOrders, pendingReplies }) {
        const navbar = new NavbarView(
            [
                { label: "Дашборд", href: "#dashboard" },
                { label: "Мои заказы", href: "#orders" },
                { label: "Отклики", href: "#replies" },
                { label: "Профиль", href: "#profile" },
            ],
            "#dashboard"
        ).render();
        const metricsBlock = new MetricsView(metrics).render();
        const lastOrdersBlock = `
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h5 mb-0">Последние заказы</h2>
        <a href="#create-order" class="btn btn-create">Создать заказ</a>
      </div>
      <div class="table-responsive mb-4">
        <table class="table align-middle mb-0">
          <thead class="table-light">
            <tr><th>Название</th><th>Статус</th><th>Дата</th></tr>
          </thead>
          <tbody>
            ${lastOrders
                .map(
                    (o) => `
                  <tr>
                    <td>${o.title}</td>
                    <td><span class="badge bg-success">${o.status}</span></td>
                    <td>${o.date}</td>
                  </tr>
                `
                )
                .join("")}
          </tbody>
        </table>
      </div>
    `;
        const pendingRepliesBlock = `
      <h2 class="h5 mb-3">Ожидающие отклики</h2>
      <div class="table-responsive">
        <table class="table align-middle mb-0">
          <thead class="table-light">
            <tr><th>Имя Исполнителя</th><th>Позиция</th><th>Статус</th></tr>
          </thead>
          <tbody>
            ${pendingReplies
                .map(
                    (r) => `
                  <tr>
                    <td>${r.name}</td>
                    <td>${r.position}</td>
                    <td><span class="badge bg-warning text-dark">Ожидает</span></td>
                  </tr>
                `
                )
                .join("")}
          </tbody>
        </table>
      </div>
    `;
        this.render(
            navbar +
                '<main class="container mb-5">' +
                metricsBlock +
                lastOrdersBlock +
                pendingRepliesBlock +
                "</main>"
        );
    }
}

// Contractee Dashboard View
export class ContracteeDashboardView extends View {
    render({ metrics, recommendedOrders, upcomingShifts, lastReplies }) {
        const navbar = new NavbarView(
            [
                { label: "Дашборд", href: "#dashboard" },
                { label: "Поиск заказов", href: "#search-orders" },
                { label: "Мои отклики", href: "#replies" },
                { label: "Профиль", href: "#profile" },
            ],
            "#dashboard"
        ).render();
        const metricsBlock = new MetricsView(metrics).render();
        const recommendedOrdersBlock = `
      <h2 class="h5 mb-3">Рекомендованные заказы</h2>
      <div class="row g-3 mb-4">
        ${recommendedOrders
            .map(
                (o) => `
              <div class="col-12 col-md-4">
                <div class="card-order">
                  <div class="fw-semibold mb-1">${o.title}</div>
                  <div class="text-muted mb-1">${o.location}</div>
                  <div class="fw-semibold">Ставка: ${o.wager}₽</div>
                </div>
              </div>
            `
            )
            .join("")}
      </div>
    `;
        const upcomingShiftsBlock = `
      <h2 class="h5 mb-3">Ближайшие выходы</h2>
      <div class="row g-3 mb-4">
        ${upcomingShifts
            .map(
                (s) => `
              <div class="col-12 col-md-4">
                <div class="card-order">
                  <div class="d-flex justify-content-between fw-semibold mb-1">
                    <div>${s.position}</div>
                    <div>${s.timeLeft}</div>
                  </div>
                  <div class="text-muted mb-1">${s.location}</div>
                  <div class="fw-semibold">Ставка: ${s.wager}₽</div>
                </div>
              </div>
            `
            )
            .join("")}
      </div>
    `;
        const lastRepliesBlock = `
      <h2 class="h5 mb-3">Последние отклики</h2>
      <div class="table-responsive">
        <table class="table align-middle mb-0">
          <thead class="table-light">
            <tr><th>Заказ</th><th>Статус</th><th>Дата подачи</th></tr>
          </thead>
          <tbody>
            ${lastReplies
                .map(
                    (r) => `
                  <tr>
                    <td>${r.orderTitle}</td>
                    <td><span class="badge ${
                        r.status === "Принят"
                            ? "bg-success"
                            : "bg-warning text-dark"
                    }">${r.status}</span></td>
                    <td>${r.date}</td>
                  </tr>
                `
                )
                .join("")}
          </tbody>
        </table>
      </div>
    `;
        this.render(
            navbar +
                '<main class="container mb-5">' +
                metricsBlock +
                recommendedOrdersBlock +
                upcomingShiftsBlock +
                lastRepliesBlock +
                "</main>"
        );
    }
}

// Аналогично реализовать ContracteeDashboardView и AdminDashboardView, используя компоненты выше
