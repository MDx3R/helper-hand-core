import { showError } from "../utils.js";

export const ADMIN_BASE = "admin";
export const CONTRACTEE_BASE = "contractee";
export const CONTRACTOR_BASE = "contractor";

export const Methods = Object.freeze({
    GET: "GET",
    POST: "POST",
    PATCH: "PATCH",
    PUT: "PUT",
    DELETE: "DELETE",
});

export class HttpClient {
    constructor({ baseURL, tokenManager }) {
        this.baseURL = baseURL;
        this.tokenManager = tokenManager;

        this.isRefreshing = false;
        this.pendingRequests = [];
    }

    async request(
        path,
        method = "GET",
        data = {},
        customHeaders = {},
        auth = true
    ) {
        const url = this.baseURL + path;
        const contentType = customHeaders["Content-Type"] || "application/json";
        const isFormData = data instanceof FormData;

        let headers = {};
        if (!isFormData) {
            headers = { "Content-Type": contentType, ...customHeaders };
        }

        const accessToken = this.tokenManager.getAccessToken();
        if (auth && accessToken) {
            headers["Authorization"] = `Bearer ${accessToken}`;
        }

        const options = { method, headers };
        if (data && method !== "GET" && method !== "DELETE") {
            if (isFormData) {
                options.body = data;
            } else if (contentType === "application/json") {
                options.body = JSON.stringify(data);
            } else if (contentType === "application/x-www-form-urlencoded") {
                options.body = data;
            } else {
                options.body = data;
            }
        }
        try {
            const response = await fetch(url, options);

            if (response.status === 401) {
                return this._handleUnauthorized(
                    path,
                    method,
                    data,
                    customHeaders
                );
            }

            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch {
                    errorData = {
                        message: response.text(),
                        status: response.status,
                    };
                }
                showError(
                    `Ошибка ${errorData.status || ""}: ${errorData.message}`
                );
                throw errorData;
            }

            const contentType = response.headers.get("Content-Type") || "";
            if (!contentType.includes("application/json")) {
                return null;
            }

            return response.json();
        } catch (err) {
            throw err;
        }
    }

    async _handleUnauthorized(path, method, data, customHeaders) {
        if (this.isRefreshing) {
            return new Promise((resolve, reject) => {
                this.pendingRequests.push({
                    resolve,
                    reject,
                    path,
                    method,
                    data,
                    customHeaders,
                });
            });
        }

        this.isRefreshing = true;

        try {
            await this._refreshTokens();

            this.isRefreshing = false;

            // повторяем оригинальный запрос с новым токеном
            const result = await this.request(
                path,
                method,
                data,
                customHeaders
            );

            this.pendingRequests.forEach(({ resolve }) => resolve(result));
            this.pendingRequests = [];

            return result;
        } catch (err) {
            this.isRefreshing = false;

            this.pendingRequests.forEach(({ reject }) => reject(err));
            this.pendingRequests = [];

            throw err;
        }
    }

    async _refreshTokens() {
        const refreshToken = this.tokenManager.getRefreshToken();

        if (!refreshToken) {
            throw new Error("No refresh token available");
        }

        const response = await fetch(this.baseURL + "/auth/refresh", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${refreshToken}`,
            },
        });

        if (!response.ok) {
            throw new Error("Failed to refresh token");
        }

        const data = await response.json();

        if (!data.access_token || !data.refresh_token) {
            throw new Error("Invalid tokens received from refresh");
        }

        this.tokenManager.setTokens({
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
        });
    }
}
