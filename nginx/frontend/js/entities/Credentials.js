export class Credentials {
    constructor({ web, telegram }) {
        this.web = web;
        this.telegram = telegram;
    }
}

export class WebCredentials {
    constructor({ email, password }) {
        this.email = email;
        this.password = password;
    }
}

export class TelegramCredentials {
    constructor({ telegram_id, chat_id }) {
        this.telegram_id = telegram_id;
        this.chat_id = chat_id;
    }
}
