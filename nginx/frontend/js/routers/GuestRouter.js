import { Router } from "./Router.js";

export class GuestRouter extends Router {
    constructor(controller) {
        super();
        this.registerDefaultRoute(controller.showLanding.bind(controller));
        this.registerRoute("", controller.showLanding.bind(controller));
        this.registerRoute("login", controller.showLoginView.bind(controller));
        this.registerRoute("register", controller.showRegisterView.bind(controller));
    }
}