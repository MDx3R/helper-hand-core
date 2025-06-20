import { User } from "../entities/User.js";
import { Methods } from "./HttpClient.js";

const PHOTOS_BASE = "photos";

export class PhotoService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.base = PHOTOS_BASE;
    }

    async uploadPhoto(file) {
        const formData = new FormData();
        formData.append("file", file);

        const data = await this.httpClient.request(
            `/${this.base}`,
            Methods.POST,
            formData
        );

        return new User(data);
    }

    async getPhoto(photoId) {
        const response = await fetch(
            `${this.httpClient.baseURL}/${this.base}/${photoId}`,
            {
                method: Methods.GET,
                headers: {
                    Authorization: `Bearer ${this.httpClient.tokenManager.getAccessToken()}`,
                },
            }
        );

        if (!response.ok) {
            throw new Error("Не удалось получить фото");
        }

        return response.blob();
    }

    async removePhoto(photoId) {
        const data = await this.httpClient.request(
            `/${this.base}/${photoId}`,
            Methods.DELETE
        );

        return new User(data);
    }
}
