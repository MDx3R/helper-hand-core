import { View } from "./View.js";

export class FooterView extends View {
    render() {
        super.render(`<div class="container pb-0">
            <a href="#" class="btn me-2">Контакты</a> | <a href="#" class="btn mx-2">Правила платформы</a> | <a href="#"
                class="btn ms-2">Поддержка</a>
            <div class="mt-2">&copy; 2025 Helper Hand</div>
        </div>`);
    }

    show() {
        this.render();
        this.root.classList.remove("d-none");
    }

    hide() {
        this.root.classList.add("d-none");
    }
}
