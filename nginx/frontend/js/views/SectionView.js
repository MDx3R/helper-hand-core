import { View } from "./View.js";

export class Section {
    constructor(id, component) {
        this.containerId = `section-${id}`;
        this.component = component;
    }

    render() {
        return `<div id="${this.containerId}">${this.component.render()}</div>`;
    }

    attach(container) {
        this.component.attachEventHandlers(container);
    }
}

export class SectionView extends View {
    render(sections = []) {
        const sectionsHtml = sections
            .map((section) => section.render())
            .join("");
        super.render(`<main class="container mb-5">${sectionsHtml}</main>`);

        // Привязка обработчиков
        const main = document.querySelector("main.container");
        if (!main) return;

        sections.forEach((section) => {
            const container = main.querySelector(`#${section.containerId}`);
            if (container) section.attach(container);
        });
    }
}
