export class Pagination {
    constructor({ last_id, size } = {}) {
        this.last_id = last_id;
        this.size = size;
    }

    toQueryString() {
        const params = new URLSearchParams();

        if (this.last_id !== undefined && this.last_id !== null) {
            params.append("last_id", this.last_id);
        }

        if (this.size !== undefined && this.size !== null) {
            params.append("size", this.size);
        }

        return params.toString();
    }
}

export function resolvePagination(input) {
    if (!input) {
        return new Pagination();
    }

    return input instanceof Pagination
        ? input
        : new Pagination(input);
}