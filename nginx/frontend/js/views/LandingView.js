import { View } from "./View.js";

export class LandingView extends View {
  constructor(root) {
    super(root);
  }

  render({ featuredOrders = [], metrics, onLogin, onRegister } = {}) {
    const renderOrderCard = ({ about, address }) => `
            <div class="col-12 col-md-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">${about}</h5>
                        <div class="text-muted mb-1">${address}</div>
                    </div>
                </div>
            </div>
        `;
    const renderMetricCard = ({ label, value, extra }) => `
            <div class="col-12 col-md-6${+value && !extra ? "" : " extra"}">
                <div class="stat-card">
                    <div class="stat-value">${value}</div>
                    <div class="stat-label">${label}</div>
                </div>
            </div>
        `;

    const ordersHtml = featuredOrders.map(renderOrderCard).join("");
    console.log(metrics);
    const metricsHtml = Object.values(metrics.toLabeledObject())
      .map(renderMetricCard)
      .join("");

    super.render(`
            <main class="container mb-3">
                <section class="hero-section mb-4">
                    <div class="row align-items-center g-4">
                        <div class="col-lg-6">
                            <div class="hero-title">Платформа для поиска и размещения заказов</div>
                            <div class="hero-desc">Современное решение для заказчиков и исполнителей. Находите заказы, управляйте откликами и работайте с лучшими.</div>
                            <button class="btn btn-primary" id="registerBtn">Зарегистрироваться</button>
                        </div>
                        <div class="col-lg-6">
                          <h2 class="h6 mb-3">Статистика платформы</h2>
                          <div class="row g-3" id="metrics-row">${metricsHtml}</div>
                      </div>
                    </div>
                </section>
                <section class="featured-orders mb-4">
                    <h2 class="h5 mb-3">Недавние заказы</h2>
                    <div class="row g-3">${ordersHtml}</div>
                </section>
                <section class="info-block">
                    <h2 class="h5 mb-3">О платформе</h2>
                    <p>Helper Hand — это современная платформа для поиска и размещения временных заказов. Мы объединяем заказчиков и исполнителей, делая процесс сотрудничества простым, безопасным и эффективным.</p>
                    <ul>
                        <li>Быстрый поиск заказов по фильтрам</li>
                        <li>Простая регистрация для обеих ролей</li>
                        <li>Безопасные сделки и поддержка</li>
                    </ul>
                </section>
            </main>
        `);

    this._bindEvents({ onLogin, onRegister });
  }

  _bindEvents({ onLogin, onRegister }) {
    if (onLogin) {
      this._bindClickHandlers("#loginBtn", onLogin);
    }
    if (onRegister) {
      this._bindClickHandlers("#registerBtn", onRegister);
    }
  }

  _bindClickHandlers(selector, handler) {
    this.root
      .querySelectorAll(selector)
      .forEach((btn) => (btn.onclick = handler));
  }
}
