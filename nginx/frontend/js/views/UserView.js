import { View } from "./View.js";

export class UserView extends View {
    constructor(root, baseURL) {
        super(root);
        this.baseURL = baseURL;
    }

    render(user, buttons = []) {
        if (!user || !user.role) {
            throw new Error("User and role must be provided");
        }

        // Вызов соответствующего рендера по роли
        let html;
        switch (user.role.toLowerCase()) {
            case "администратор":
            case "admin":
                html = this._renderAdmin(user, buttons);
                break;

            case "заказчик":
            case "contractor":
                html = this._renderContractor(user, buttons);
                break;

            case "исполнитель":
            case "contractee":
                html = this._renderContractee(user, buttons);
                break;

            default:
                throw new Error(`Unknown role: ${user.role}`);
        }
        super.render(html);
        this.bsModal = new bootstrap.Modal(this.root);
        this.bsModal.show();

        this._attachButtonHandlers(buttons, this.root);
    }

    // Общий рендер карусели фото
    _renderPhotoCarousel(photos, carouselId) {
        const photosExist = photos && photos.length > 0;
        const photosHtml = photosExist
            ? photos
                  .map(
                      (url, idx) => `
        <div class="carousel-item ${idx === 0 ? "active" : ""} photo-wrapper">
          <img src="${this.baseURL}/photos/${url}" alt="Фото ${
                          idx + 1
                      }" class="photo-background" />
          <img src="${this.baseURL}/photos/${url}" alt="Фото ${
                          idx + 1
                      }" class="photo-foreground" />
        </div>`
                  )
                  .join("")
            : `
      <div class="carousel-item active photo-wrapper">
        <img src="https://placehold.co/800x600" alt="Фото по умолчанию" class="photo-background" />
        <img src="https://placehold.co/600x600" alt="Фото по умолчанию" class="photo-foreground" />
      </div>`;

        const indicatorsHtml = photosExist
            ? photos
                  .map(
                      (_, i) => `
        <button type="button" data-bs-target="#${carouselId}" data-bs-slide-to="${i}" 
          class="${i === 0 ? "active" : ""}" aria-current="${
                          i === 0 ? "true" : "false"
                      }" aria-label="Slide ${i + 1}">
        </button>`
                  )
                  .join("")
            : `<button type="button" data-bs-target="#${carouselId}" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>`;

        return `
      <div id="${carouselId}" class="carousel slide mb-3" data-bs-ride="carousel">
        <div class="carousel-indicators">
          ${indicatorsHtml}
        </div>
        <div class="carousel-inner rounded">
          ${photosHtml}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Предыдущий</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Следующий</span>
        </button>
      </div>`;
    }

    _renderBaseModal(
        title,
        carouselHtml,
        fullName,
        role,
        phone,
        extraInfoHtml = "",
        buttons = []
    ) {
        const safeAbout =
            extraInfoHtml || '<p class="small text-secondary">Нет описания</p>';

        const buttonsHtml = buttons
            .map(
                (_, index) =>
                    `<button type="button" class="btn btn-action-${index}"></button>`
            )
            .join("");

        return `
              <div class="modal-dialog modal-dialog-centered modal-md">
                  <div class="modal-content shadow-lg rounded-4 border-0">
                      <div class="modal-header border-0 pb-0">
                          <h5 class="modal-title fw-bold mb-3">Информация о ${title}</h5>
                          <button type="button" class="btn-close btn-close-black" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                      </div>
                      <div class="modal-body pt-0">
                          <div class="d-flex flex-column align-items-center text-center">
                              ${carouselHtml}
                              <h4 class="fw-semibold mb-1">${fullName}</h4>
                              <p class="text-muted mb-3">Роль: ${role}</p>
                              <p>Телефон: ${phone}</p>
                              ${safeAbout}
                          </div>
                      </div>
                      <div class="modal-footer border-0 pt-0">
                          ${buttonsHtml}
                      </div>
                  </div>
              </div>
        `;
    }

    _attachButtonHandlers(buttons, modalElement) {
        buttons.forEach(({ text, onClick }, index) => {
            const btn = modalElement.querySelector(`.btn-action-${index}`);
            if (btn) {
                btn.textContent = text;
                btn.classList.add(
                    index === 0 ? "btn-outline-secondary" : "btn-primary"
                );
                btn.addEventListener("click", () => {
                    if (typeof onClick === "function") onClick();
                });
            }
        });
    }

    _renderAdmin(admin, buttons) {
        const {
            surname,
            name,
            patronymic,
            photos = [],
            role = "Администратор",
            phone_number,
            about,
        } = admin;

        const carouselHtml = this._renderPhotoCarousel(
            photos,
            "userPhotoCarousel"
        );
        const fullName = [surname, name, patronymic].filter(Boolean).join(" ");
        const aboutHtml = `<p class="small text-secondary">Описание: ${
            about || "Нет описания"
        }</p>`;

        return this._renderBaseModal(
            "Администраторе",
            carouselHtml,
            fullName,
            role,
            phone_number,
            aboutHtml,
            buttons
        );
    }

    _renderContractor(contractor, buttons) {
        const {
            surname,
            name,
            patronymic,
            phone_number,
            photos = [],
            about,
        } = contractor;

        const carouselHtml = this._renderPhotoCarousel(
            photos,
            "userPhotoCarousel"
        );
        const fullName = [surname, name, patronymic].filter(Boolean).join(" ");
        const role = "Заказчик";
        const aboutHtml = `<p class="small text-secondary">${
            about || "Нет описания"
        }</p>`;

        return this._renderBaseModal(
            "Заказчике",
            carouselHtml,
            fullName,
            role,
            phone_number,
            aboutHtml,
            buttons
        );
    }

    _renderContractee(contractee, buttons) {
        const {
            surname,
            name,
            patronymic,
            phone_number,
            photos = [],
            birthday,
            citizenship,
            height,
            positions = [],
        } = contractee;

        const carouselHtml = this._renderPhotoCarousel(
            photos,
            "userPhotoCarousel"
        );
        const fullName = [surname, name, patronymic].filter(Boolean).join(" ");
        const role = "Исполнитель";

        const positionsText = positions.length
            ? positions.join(", ")
            : "Нет позиций";

        const extraInfoHtml = `
      <p class="small text-secondary">
        Дата рождения: ${birthday || "не указано"}<br />
        Гражданство: ${citizenship || "не указано"}<br />
        Рост: ${height || "не указан"}<br />
        Позиции: ${positionsText}
      </p>`;

        return this._renderBaseModal(
            "Исполнителе",
            carouselHtml,
            fullName,
            role,
            phone_number,
            extraInfoHtml,
            buttons
        );
    }
}
