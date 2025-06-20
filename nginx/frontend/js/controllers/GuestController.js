export class GuestController {
    constructor(
        orderService,
        authService,
        metricsService,
        landingView,
        loginView,
        registerView,
        navBarView,
        footerView,
        onLoginSuccess,
        onRegisterSuccess
    ) {
        this.orderService = orderService;
        this.authService = authService;
        this.metricsService = metricsService;
        this.landingView = landingView;
        this.loginView = loginView;
        this.registerView = registerView;
        this.navBarView = navBarView;
        this.footerView = footerView;
        this.onLoginSuccess = onLoginSuccess;
        this.onRegisterSuccess = onRegisterSuccess;
    }

    async showLanding() {
        const pageName = "";
        let metrics = {};
        let featuredOrders = [];
        try {
            metrics = await this.metricsService.getAppMetrics();
            featuredOrders = await this.orderService.listOrders({ size: 6 });
        } catch (e) {
            featuredOrders = [];
        }

        this.footerView.show();
        this._renderNavBar(pageName);
        this.landingView.render({
            featuredOrders,
            metrics,
            onLogin: () => this.showLoginView(),
            onRegister: () => this.showRegisterView(),
        });
    }

    showLoginView() {
        const pageName = "login";
        this.loginView.render({
            onRegister: () => this.showRegisterView(),
            onLogin: (username, password) =>
                this._loginHandler(username, password),
        });
        this.footerView.hide();
        this._renderNavBar(pageName);
    }

    showRegisterView() {
        const pageName = "register";
        this.registerView.render({
            onLogin: () => this.showLoginView(),
            onRegisterContractor: (user) =>
                this._registerContractorHandler(user),
            onRegisterContractee: (user) =>
                this._registerContracteeHandler(user),
        });
        this.footerView.hide();
        this._renderNavBar(pageName);
    }

    _renderNavBar(activeId) {
        const navLinks = [
            {
                label: "Войти",
                id: "login",
                callback: () => (location.hash = `#login`),
            },
            {
                label: "Регистрация",
                id: "register",
                callback: () => (location.hash = `#register`),
            },
        ];
        this.navBarView.render(navLinks, activeId);
    }

    async _loginHandler(username, password) {
        const data = await this.authService.login(username, password);
        this.onLoginSuccess(data.user_id);
        return data;
    }

    async _registerContractorHandler(user) {
        const data = await this.authService.registerContractor(user);
        this.onRegisterSuccess(data.user_id);
        return data;
    }

    async _registerContracteeHandler(user) {
        const data = await this.authService.registerContractee(user);
        this.onRegisterSuccess(data.user_id);
        return data;
    }
}
