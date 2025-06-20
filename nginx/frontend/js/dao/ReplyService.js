import { Reply, CompleteReply } from "../entities/Reply.js";
import { resolvePagination } from "../dto/Pagination.js";
import { CONTRACTEE_BASE, CONTRACTOR_BASE, Methods } from "./HttpClient.js";

const REPLIES_BASE = "replies";

export class ContracteeReplyService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = `${CONTRACTEE_BASE}/${REPLIES_BASE}`;
    }

    async listReplies(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async listOrderReplies(orderId, paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/order/${orderId}${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async listFutureReplies(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/future${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async getReply(detailId) {
        const data = await this.httpClient.request(`/${this.base}/${detailId}`);
        return new CompleteReply(data);
    }

    async submitReply(detailId) {
        const data = await this.httpClient.request(
            `/${this.base}/${detailId}`,
            Methods.POST
        );
        return new Reply(data);
    }
}

export class ContractorReplyService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = `${CONTRACTOR_BASE}/${REPLIES_BASE}`;
    }

    async listOrderReplies(orderId, paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/order/${orderId}${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async listDetailReplies(detailId, paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/detail/${detailId}${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async listPendingReplies(paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/pending${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async listPendingRepliesForOrder(orderId, paginationDTO) {
        const query = resolvePagination(paginationDTO).toQueryString();
        const data = await this.httpClient.request(
            `/${this.base}/pending/${orderId}${query ? `?${query}` : ""}`
        );
        return data.map((r) => new CompleteReply(r));
    }

    async getReply(detailId, contracteeId) {
        const data = await this.httpClient.request(
            `/${this.base}/${detailId}/${contracteeId}`
        );
        return new CompleteReply(data);
    }

    async approveReply(detailId, contracteeId) {
        return await this.performAction(detailId, contracteeId, "approve");
    }

    async disapproveReply(detailId, contracteeId) {
        return await this.performAction(detailId, contracteeId, "disapprove");
    }

    async performAction(detailId, contracteeId, action) {
        const data = await this.httpClient.request(
            `/${this.base}/${detailId}/${contracteeId}/${action}`,
            Methods.POST
        );
        return new Reply(data);
    }
}
