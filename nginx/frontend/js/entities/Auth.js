export class Auth {
    constructor({
        user_id,
        access_token,
        refresh_token,
        token_type = "bearer",
    }) {
        this.user_id = user_id;
        this.access_token = access_token;
        this.refresh_token = refresh_token;
        this.token_type = token_type;
    }
}
