import { NavbarView } from "./views/NavbarView.js";
import { GuestController } from "./controllers/GuestController.js";
import { AuthService } from "./dao/AuthService.js";
import { HttpClient } from "./dao/HttpClient.js";
import {
  AdminOrderService,
  ContracteeOrderService,
  ContractorOrderService,
  OrderService,
} from "./dao/OrderService.js";
import { TokenManager } from "./dao/TokenManager.js";
import {
  AdminUserService,
  ContracteeUserService,
  ContractorUserService,
  UserService,
} from "./dao/UserService.js";
import { GuestRouter } from "./routers/GuestRouter.js";
import { Router } from "./routers/Router.js";
import { LandingView } from "./views/LandingView.js";
import { LoginView } from "./views/LoginView.js";
import { RegisterView } from "./views/RegisterView.js";
import { AdminController } from "./controllers/AdminController.js";
import { AdminRouter } from "./routers/AdminRouter.js";
import { AdminDashboardView } from "./views/admin/AdminDashboardView.js";
import { FooterView } from "./views/FooterView.js";
import { MetricsService } from "./dao/MetricsService.js";
import { UserView } from "./views/UserView.js";
import { ContractorRouter } from "./routers/ContractorRouter.js";
import { ContractorController } from "./controllers/ContractorController.js";
import {
  ContracteeReplyService,
  ContractorReplyService,
} from "./dao/ReplyService.js";
import { ContractorDashboardView } from "./views/contractor/ContractorDashboardView.js";
import { ContracteeDashboardView } from "./views/contractee/ContracteeDashboardView.js";
import { ContracteeRouter } from "./routers/ContracteeRouter.js";
import { ContracteeController } from "./controllers/ContracteeController.js";
import { ProfileView } from "./views/ProfileView.js";
import { CreateOrderView } from "./views/CreateOrderView.js";
import { PhotoService } from "./dao/PhotoService.js";

// localStorage.removeItem("accessToken");
// localStorage.removeItem("refreshToken");

const baseURL = "http://127.0.0.1:80/api";
const accessToken = localStorage.getItem("accessToken");
const refreshToken = localStorage.getItem("refreshToken");
const tokenManager = new TokenManager({ accessToken, refreshToken });
const httpClient = new HttpClient({ baseURL, tokenManager });

// Shared DAO
const orderService = new OrderService(httpClient);
const authService = new AuthService(httpClient, tokenManager);
const metricsService = new MetricsService(httpClient);
const userService = new UserService(httpClient);
const photoService = new PhotoService(httpClient);

// Admin
const adminUserService = new AdminUserService(httpClient);
const adminOrderService = new AdminOrderService(httpClient);

// Contractor
const contractorUserService = new ContractorUserService(httpClient);
const contractorOrderService = new ContractorOrderService(httpClient);
const contractorReplyService = new ContractorReplyService(httpClient);

// Contractee
const contracteeUserService = new ContracteeUserService(httpClient);
const contracteeOrderService = new ContracteeOrderService(httpClient);
const contracteeReplyService = new ContracteeReplyService(httpClient);

const appElement = document.getElementById("app");
const navbarElement = document.getElementById("navbar");
const footerElement = document.querySelector("footer");
const userModal = document.getElementById("userModal");

// Shared
const navBarView = new NavbarView(navbarElement);
const footerView = new FooterView(footerElement);
const landingView = new LandingView(appElement, navBarView);
const loginView = new LoginView(appElement);
const registerView = new RegisterView(appElement);
const userView = new UserView(userModal, httpClient.baseURL);
const ordersView = null;
const profileView = new ProfileView(
  appElement,
  photoService,
  httpClient.baseURL
);

// Admin
const adminDashboardView = new AdminDashboardView(appElement);

// Contractor
const contractorDashboardView = new ContractorDashboardView(appElement);

// Contractee
const contracteeDashboardView = new ContracteeDashboardView(appElement);

// CreateOrder
const createOrderView = new CreateOrderView(appElement);

let controller;
let router = new Router();

let onAuth = async () => {
  let user = await userService.getMe();
  localStorage.setItem("role", user.role);
  routeTo = "#";
  startApp(user.role);
};

let onLogout = async () => {
  routeTo = "#";
  startApp("guest");
};

function createContractorController() {
  return new ContractorController(
    contractorUserService,
    contractorOrderService,
    contractorReplyService,
    metricsService,
    authService,
    contractorDashboardView,
    ordersView,
    profileView,
    navBarView,
    userView,
    createOrderView,
    onLogout
  );
}

function createContractorRouter(controller) {
  return new ContractorRouter(controller);
}

function createContracteeController() {
  return new ContracteeController(
    contracteeUserService,
    contracteeOrderService,
    contracteeReplyService,
    metricsService,
    authService,
    contracteeDashboardView,
    ordersView,
    profileView,
    navBarView,
    userView,
    onLogout
  );
}

function createContracteeRouter(controller) {
  return new ContracteeRouter(controller);
}

function createAdminController() {
  return new AdminController(
    adminUserService,
    adminOrderService,
    metricsService,
    authService,
    adminDashboardView,
    ordersView,
    profileView,
    navBarView,
    userView,
    onLogout
  );
}

function createAdminRouter(controller) {
  return new AdminRouter(controller);
}

let routeTo = null;

function startApp(role) {
  router.stop();

  switch (role) {
    case "contractor":
      controller = createContractorController();
      router = createContractorRouter(controller);
      break;
    case "contractee":
      controller = createContracteeController();
      router = createContracteeRouter(controller);
      break;
    case "admin":
      controller = createAdminController();
      router = createAdminRouter(controller);
      break;
    default:
      controller = new GuestController(
        orderService,
        authService,
        metricsService,
        landingView,
        loginView,
        registerView,
        navBarView,
        footerView,
        onAuth,
        onAuth
      );
      router = new GuestRouter(controller);
  }

  if (routeTo) {
    location.hash = routeTo;
  }
  router.start();
}

function getRole() {
  return localStorage.getItem("role") || "guest";
}

window.onload = () => {
  startApp(getRole());
};
