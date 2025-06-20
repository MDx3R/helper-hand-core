import {
    AdminMetrics,
    AppMetrics,
    ContracteeMetrics,
    ContractorMetrics,
} from "../entities/Metrics.js";
import { ADMIN_BASE, CONTRACTEE_BASE, CONTRACTOR_BASE } from "./HttpClient.js";

const METRICS_APP_BASE = "metrics";
export const METRICS_BASE = {
    app: METRICS_APP_BASE,
    admin: `${ADMIN_BASE}/${METRICS_APP_BASE}`,
    contractee: `${CONTRACTEE_BASE}/${METRICS_APP_BASE}`,
    contractor: `${CONTRACTOR_BASE}/${METRICS_APP_BASE}`,
};

export class MetricsService {
    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async getAppMetrics() {
        const data = await this.httpClient.request(`/${METRICS_BASE.app}`);
        return new AppMetrics(data);
    }

    async getAdminMetrics() {
        const data = await this.httpClient.request(`/${METRICS_BASE.admin}`);
        return new AdminMetrics(data);
    }

    async getContracteeMetrics() {
        const data = await this.httpClient.request(
            `/${METRICS_BASE.contractee}`
        );
        return new ContracteeMetrics(data);
    }

    async getContractorMetrics() {
        const data = await this.httpClient.request(
            `/${METRICS_BASE.contractor}`
        );
        return new ContractorMetrics(data);
    }
}
