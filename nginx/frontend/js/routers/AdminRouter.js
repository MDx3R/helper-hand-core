import { Router } from "./Router.js";

export class AdminRouter extends Router {
    constructor(controller) {
        super(controller);
        this.controller = controller;
        this.registerDefaultRoute(controller.showDashboard.bind(controller));
        this.registerRoute("", controller.showDashboard.bind(controller));
        this.registerRoute(
            "dashboard",
            controller.showDashboard.bind(controller)
        );
        this.registerRoute("orders", controller.showOrders.bind(controller));
        this.registerRoute("profile", controller.showProfile.bind(controller));
        this.registerRoute("order", controller.showOrder.bind(controller));
    }
}
