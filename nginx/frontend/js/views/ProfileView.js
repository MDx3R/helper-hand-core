import { View } from "./View.js";

export class ProfileView extends View {
    constructor(root, photoService, baseURL) {
        super(root);
        this.photoService = photoService;
        this.baseURL = baseURL;
        this._currentUser = null;
        this.onPhotoUpload = async (file) =>
            await this.photoService.uploadPhoto(file);
        this._selectedPhotos = [];
    }

    render(user, { onSubmit }) {
        if (!user || !user.role) {
            throw new Error("User and role must be provided");
        }

        this._currentUser = user;
        const photos = user.photos || [];

        let html;
        switch (user.role.toLowerCase()) {
            case "admin":
            case "администратор":
                html = this._renderProfile(
                    user,
                    "Администратор",
                    this._renderAdminFields(user),
                    photos
                );
                break;
            case "contractor":
            case "заказчик":
                html = this._renderProfile(
                    user,
                    "Заказчик",
                    this._renderContractorFields(user),
                    photos
                );
                break;
            case "contractee":
            case "исполнитель":
                html = this._renderProfile(
                    user,
                    "Исполнитель",
                    this._renderContracteeFields(user),
                    photos
                );
                break;
            default:
                throw new Error(`Unknown role: ${user.role}`);
        }

        super.render(html);

        this._setupPhotoInputHandler(photos.length);
        this._setupSubmitHandler(onSubmit);
    }

    _renderProfile(user, roleLabel, fieldsHtml, photoIds = []) {
        const fullName = [user.surname, user.name, user.patronymic]
            .filter(Boolean)
            .join(" ");
        const firstPhotoUrl = photoIds.length
            ? `${this.baseURL}/photos/${photoIds[0]}`
            : "https://placehold.co/800x600";

        return `
            <div class="profile-block">
                <div class="d-flex align-items-center gap-4 mb-4">
                    <img 
                        src="${firstPhotoUrl}" 
                        alt="Фото профиля" 
                        class="profile-photo"
                    />
                    <div>
                        <div class="fs-4 fw-semibold">${fullName}</div>
                        <div class="profile-label">${roleLabel}</div>
                    </div>
                </div>
                <form>
                    ${fieldsHtml}
                    <div class="mb-3">
                        <label class="form-label">Фотография профиля (до 3)</label>
                        <input type="file" id="photo-input" accept="image/*" multiple class="form-control mt-2" />
                        <div class="photo-preview d-flex gap-2 mt-2" id="photo-preview"></div>
                    </div>
                    <button type="submit" class="btn btn-dark">Сохранить</button>
                    <div class="error d-none">Ошибка сохранения</div>
                </form>
            </div>
        `;
    }

    _renderCommonFields(user) {
        return `
            <div class="mb-3">
                <label class="form-label">Фамилия</label>
                <input type="text" class="form-control" name="surname" value="${
                    user.surname || ""
                }">
            </div>
            <div class="mb-3">
                <label class="form-label">Имя</label>
                <input type="text" class="form-control" name="name" value="${
                    user.name || ""
                }">
            </div>
            <div class="mb-3">
                <label class="form-label">Телефон</label>
                <input type="tel" class="form-control" name="phone_number" value="${
                    user.phone_number || ""
                }">
            </div>
        `;
    }

    _renderAdminFields(admin) {
        return `
            ${this._renderCommonFields(admin)}
            <div class="mb-3">
                <label class="form-label">О себе</label>
                <textarea class="form-control" name="about" rows="3">${
                    admin.about || ""
                }</textarea>
            </div>
        `;
    }

    _renderContractorFields(contractor) {
        return `
            ${this._renderCommonFields(contractor)}
            <div class="mb-3">
                <label class="form-label">О себе</label>
                <textarea class="form-control" name="about" rows="3">${
                    contractor.about || ""
                }</textarea>
            </div>
        `;
    }

    _renderContracteeFields(contractee) {
        return `
            ${this._renderCommonFields(contractee)}
            <div class="mb-3">
                <label class="form-label">Дата рождения</label>
                <input type="date" class="form-control" name="birthday" value="${
                    contractee.birthday || ""
                }">
            </div>
            <div class="mb-3">
                <label class="form-label">Гражданство</label>
                <input type="text" class="form-control" name="citizenship" value="${
                    contractee.citizenship || ""
                }">
            </div>
            <div class="mb-3">
                <label class="form-label">Рост (см)</label>
                <input type="number" class="form-control" name="height" value="${
                    contractee.height || ""
                }">
            </div>
            <div class="mb-3">
                <label class="form-label">Позиции</label>
                <input type="text" class="form-control" name="positions" value="${contractee.positions.join(
                    ", "
                )}">
            </div>
        `;
    }

    _setupPhotoInputHandler(initialPhotoCount = 0) {
        const input = document.getElementById("photo-input");
        const previewContainer = document.getElementById("photo-preview");
        this._selectedPhotos = [];

        const updateInputVisibility = () => {
            const total = initialPhotoCount + this._selectedPhotos.length;
            input.disabled = total >= 3;
            input.classList.toggle("d-none", total >= 3);
        };

        const renderPreview = (src) => {
            const img = document.createElement("img");
            img.src = src;
            img.className = "rounded border border-light";
            img.style.width = "100px";
            img.style.height = "100px";
            previewContainer.appendChild(img);
        };

        for (let photoId of this._currentUser.photos) {
            renderPreview(`${this.baseURL}/photos/${photoId}`);
        }

        input.addEventListener("change", (event) => {
            const files = Array.from(event.target.files);
            let currentTotal = initialPhotoCount + this._selectedPhotos.length;

            for (const file of files) {
                if (currentTotal >= 3) {
                    alert("Нельзя загрузить больше 3 фотографий.");
                    break;
                }

                const alreadyAdded = this._selectedPhotos.some(
                    (f) => f.name === file.name && f.size === file.size
                );
                if (!alreadyAdded) {
                    this._selectedPhotos.push(file);
                    currentTotal++;

                    renderPreview(URL.createObjectURL(file));
                }
            }

            input.value = "";
            updateInputVisibility();
        });

        updateInputVisibility();
    }

    _setupSubmitHandler(onSubmit) {
        const form = document.querySelector("form");
        const errorEl = form.querySelector(".error");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            try {
                // Загружаем новые фотографии
                for (const file of this._selectedPhotos) {
                    const user = await this.onPhotoUpload(file);
                    this._currentUser.photos = user.photos;
                }

                // Собираем данные формы
                const formData = {};
                const inputs = form.querySelectorAll(
                    "input[name], textarea[name]"
                );
                inputs.forEach((input) => {
                    if (input.name === "positions") {
                        formData.positions = input.value
                            .split(",")
                            .map((s) => s.trim())
                            .filter(Boolean);
                    } else if (input.name === "height") {
                        formData.height = parseInt(input.value, 10) || null;
                    } else {
                        formData[input.name] = input.value.trim();
                    }
                });
                formData.photos = this._currentUser.photos;
                if (this._currentUser.role == "contractee") {
                    formData.gender = this._currentUser.gender;
                }
                // Вызов onSubmit с собранными данными
                this._currentUser = await onSubmit(formData);
                console.log(this._currentUser);
                // Перерисовываем форму с обновленными данными
                this.render(this._currentUser, { onSubmit });
            } catch (err) {
                console.error("Ошибка при сохранении:", err);
                errorEl.classList.remove("d-none");
            }
        });
    }
}
