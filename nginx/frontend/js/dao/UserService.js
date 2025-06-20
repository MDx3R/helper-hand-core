import {
    Methods,
    ADMIN_BASE,
    CONTRACTOR_BASE,
    CONTRACTEE_BASE,
} from "./HttpClient.js";
import { resolvePagination } from "../dto/Pagination.js";
import {
    User,
    Contractee,
    Contractor,
    Admin,
    CompleteContractee,
    CompleteContractor,
    CompleteAdmin,
} from "../entities/User.js";

const USERS_BASE = "users";

function mapRole(role, data) {
    if (role == "admin") {
        return new Admin(data);
    } else if (role == "contractor") {
        return new Contractor(data);
    } else if (role == "contractee") {
        return new Contractee(data);
    } else {
        throw Error;
    }
}

function mapCompleteRole(role, data) {
    if (role == "admin") {
        return new CompleteAdmin(data);
    } else if (role == "contractor") {
        return new CompleteContractor(data);
    } else if (role == "contractee") {
        return new CompleteContractee(data);
    } else {
        throw Error;
    }
}

export class UserService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = USERS_BASE;
    }

    async getMe() {
        const data = await this.httpClient.request(`/${this.base}/me`);
        return new User(data);
    }
}

class RoleUserService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = "";
    }

    async getMe() {
        const data = await this.httpClient.request(`/${this.base}/me`);
        return mapCompleteRole(data.user.role, data);
    }

    async updateProfile(userData) {
        const data = await this.httpClient.request(
            `/${this.base}/me`,
            Methods.PATCH,
            userData
        );
        return mapRole(data.role, data);
    }

    async getUser(userId) {
        const data = await this.httpClient.request(`/${this.base}/${userId}`);
        return mapCompleteRole(data.user.role, data);
    }
}

export class AdminUserService extends RoleUserService {
    constructor(httpClient) {
        super(httpClient);
        this.base = `${ADMIN_BASE}/${USERS_BASE}`;
    }

    async listPendingUsers(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/pending${query ? `?${query}` : ""}`
        );
        return data.map((u) => new User(u));
    }

    async approveUser(userId) {
        const data = await this.httpClient.request(
            `/${this.base}/${userId}/approve`
        );
        return new User(data);
    }

    async disapproveUser(userId) {
        const data = await this.httpClient.request(
            `/${this.base}/${userId}/disapprove`
        );
        return new User(data);
    }
}

export class ContractorUserService extends RoleUserService {
    constructor(httpClient) {
        super(httpClient);
        this.base = `${CONTRACTOR_BASE}/${USERS_BASE}`;
    }
}

export class ContracteeUserService extends RoleUserService {
    constructor(httpClient) {
        super(httpClient);
        this.base = `${CONTRACTEE_BASE}/${USERS_BASE}`;
    }
}
