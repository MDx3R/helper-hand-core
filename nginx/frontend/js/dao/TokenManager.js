export class TokenManager {
    constructor({ accessToken = null, refreshToken = null }) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
    }

    getAccessToken() {
        return this.accessToken;
    }

    getRefreshToken() {
        return this.refreshToken;
    }

    setTokens({ accessToken, refreshToken }) {
        if (accessToken) {
            this.accessToken = accessToken;
            localStorage.setItem("accessToken", accessToken);
        }
        if (refreshToken) {
            this.refreshToken = refreshToken;
            localStorage.setItem("refreshToken", refreshToken);
        }
    }

    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
    }
}
