export class Reply {
    constructor({ contractee_id, detail_id, reply_id, status }) {
        this.contractee_id = contractee_id;
        this.detail_id = detail_id;
        this.reply_id = reply_id;
        this.status = status;
    }
}

export class CompleteReply {
    constructor({ reply, contractee, detail, order }) {
        this.reply = reply;
        this.contractee = contractee;
        this.detail = detail;
        this.order = order;
    }
}
