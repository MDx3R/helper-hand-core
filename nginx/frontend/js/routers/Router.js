// Показывает preloader
export function showPreloader() {
    const preloader = document.getElementById("preloader");
    if (preloader) {
        preloader.classList.remove("hidden");
    }
}
// Скрывает preloader
export function hidePreloader() {
    const preloader = document.getElementById("preloader");
    if (preloader) {
        preloader.classList.add("hidden");
    }
}

export class Router {
    constructor() {
        this.routes = {};
        this.defaultRoute = () => {};
        this._boundHandleRoute = this.handleRoute.bind(this);
        this.suppressNextHashChange = false;
    }

    registerDefaultRoute(handler) {
        this.defaultRoute = () => {
            showPreloader();
            try {
                handler();
            } finally {
                hidePreloader();
            }
        };
    }

    registerRoute(route, handler) {
        this.routes[route] = (...values) => {
            showPreloader();
            try {
                handler(...values);
            } finally {
                hidePreloader();
            }
        };
    }

    handleRoute() {
        if (this.suppressNextHashChange) {
            this.suppressNextHashChange = false;
            return;
        }

        const fullHash = location.hash.slice(1) || ""; // default
        const split = fullHash.split("/");
        const hash = split[0];
        const handler = this.routes[hash];
        if (handler && typeof handler === "function") {
            handler(...split.slice(1).map((value) => +value));
        } else {
            this.defaultRoute();
        }
    }

    start() {
        window.addEventListener("hashchange", this._boundHandleRoute);
        this.handleRoute();
    }

    stop() {
        window.removeEventListener("hashchange", this._boundHandleRoute);
    }

    suppressNext() {
        this.suppressNextHashChange = true;
    }
}
