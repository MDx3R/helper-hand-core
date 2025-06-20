import { Auth } from "../entities/Auth.js";
import { Credentials } from "../entities/Credentials.js";
import { Methods } from "./HttpClient.js";

export class AuthService {
    constructor(httpClient, tokenManager) {
        this.httpClient = httpClient;
        this.tokenManager = tokenManager;
        this.base = "auth";
    }

    async login(username, password) {
        const body = new URLSearchParams();
        body.append("username", username);
        body.append("password", password);

        const data = await this.httpClient.request(
            `/${this.base}/login`,
            Methods.POST,
            body.toString(),
            { "Content-Type": "application/x-www-form-urlencoded" }
        );
        const token = new Auth(data);

        this._setAuth({
            accessToken: token.access_token,
            refreshToken: token.refresh_token,
            userId: token.user_id,
        });

        return token;
    }

    async logout() {
        await this.httpClient.request(`/${this.base}/logout`, Methods.POST);
        this._removeAuth();
    }

    async registerContractor(userData) {
        const data = await this.httpClient.request(
            `/${this.base}/register/contractor`,
            "POST",
            userData
        );

        const token = new Auth(data.token);
        this._setAuth({
            accessToken: token.access_token,
            refreshToken: token.refresh_token,
            userId: token.user_id,
        });

        return token;
    }

    async registerContractee(userData) {
        const data = await this.httpClient.request(
            `/${this.base}/register/contractee`,
            "POST",
            userData
        );

        const token = new Auth(data.token);
        this._setAuth({
            accessToken: token.access_token,
            refreshToken: token.refresh_token,
            userId: token.user_id,
        });

        return token;
    }

    _removeAuth() {
        this.tokenManager.clearTokens();
        localStorage.removeItem("userId");
    }

    _setAuth({ accessToken, refreshToken, userId }) {
        if (accessToken && refreshToken) {
            this.tokenManager.setTokens({ accessToken, refreshToken });
        }
        if (userId) {
            localStorage.setItem("userId", userId);
        }
    }
}
