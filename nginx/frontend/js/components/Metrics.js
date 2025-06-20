import { Component } from "./Component.js";

export class MetricsBoard extends Component {
    constructor(metrics, showMore = false) {
        super();
        this.metrics = metrics;
        this.showMore = showMore;
    }
    render() {
        const rows = Object.values(this.metrics.toLabeledObject())
            .sort((a, b) => a.extra - b.extra)
            .map(
                (m) => `
                <div class="col-12 col-md-4${m.extra ? " extra" : ""}">
                    <div class="stat-card">
                        <div class="stat-value">${m.value}</div>
                        <div class="stat-label">${m.label}</div>
                    </div>
                </div>
              `
            )
            .join("");

        return `
        <div class="row g-4 mb-3" id="metrics-row">${rows}</div>
        <div class="d-flex justify-content-end align-items-center mb-3">
          <button class="btn" id="showMoreBtn">
            ${this.showMore ? "Показать меньше" : "Показать больше"}
          </button>
        </div>
      `;
    }
    attachEventHandlers(container, {} = {}) {
        const btn = container.querySelector("#showMoreBtn");
        const extras = container.querySelectorAll(".extra");

        btn.addEventListener("click", () => {
            const isHidden =
                extras[0].style.display === "none" ||
                extras[0].style.display === "";
            extras.forEach((card) => {
                card.style.display = isHidden ? "block" : "none";
            });
            btn.textContent = isHidden ? "Показать меньше" : "Показать больше";
        });
    }
}
