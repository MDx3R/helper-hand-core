export function wrapWithHandlers(component, handlers) {
    const origAttach = component.attachEventHandlers.bind(component);
    component.attachEventHandlers = (container) =>
        origAttach(container, handlers);
    return component;
}

export function pluralize(n, one, few, many) {
    const mod10 = n % 10;
    const mod100 = n % 100;

    if (mod10 === 1 && mod100 !== 11) return one;
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return few;
    return many;
}

export function showError(message) {
    const errorContainer = document.getElementById("error-message");

    errorContainer.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>
        </div>
    `;
}
