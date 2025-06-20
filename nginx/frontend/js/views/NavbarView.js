import { View } from "./View.js";

export class NavbarView extends View {
    render(links, active) {
        let navbar = `
        <div class="container">
          <a class="navbar-brand fw-bold" href="#">Helper Hand</a>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            ${links
                .map(
                    (l) =>
                        `<li id="${
                            l.id
                        }NavButton" class="nav-item"><a class="nav-link${
                            l.id === active ? " active" : ""
                        }" href="#${l.id}">${l.label}</a></li>`
                )
                .join("")}
          </ul>
        </div>
    `;
        super.render(navbar);
        links.forEach((l) => {
            const btn = this.root.querySelector(`#${l.id}NavButton`);
            if (btn) {
                btn.onclick = (e) => {
                    e.preventDefault();
                    l.callback(e);
                };
            }
        });
    }
}
