export class User {
    constructor({
        surname,
        name,
        patronymic,
        user_id,
        photos,
        role,
        status,
        phone_number,
    }) {
        this.surname = surname;
        this.name = name;
        this.patronymic = patronymic;
        this.user_id = user_id;
        this.photos = photos;
        this.role = role;
        this.status = status;
        this.phone_number = phone_number;
    }
}

export class Contractee extends User {
    constructor({
        surname,
        name,
        patronymic,
        phone_number,
        photos,
        role,
        birthday,
        height,
        gender,
        citizenship,
        positions,
        user_id,
        status,
    }) {
        super({
            surname,
            name,
            patronymic,
            user_id,
            photos,
            role,
            status,
            phone_number,
        });
        this.birthday = birthday;
        this.height = height;
        this.gender = gender;
        this.citizenship = citizenship;
        this.positions = positions;
    }
}

export class Contractor extends User {
    constructor({
        surname,
        name,
        patronymic,
        phone_number,
        photos,
        role,
        about,
        user_id,
        status,
    }) {
        super({
            surname,
            name,
            patronymic,
            user_id,
            photos,
            role,
            status,
            phone_number,
        });
        this.about = about;
    }
}

export class Admin extends User {
    constructor({
        surname,
        name,
        patronymic,
        user_id,
        photos,
        role,
        status,
        phone_number,
        about,
        contractor_id,
    }) {
        super({
            surname,
            name,
            patronymic,
            user_id,
            photos,
            role,
            status,
            phone_number,
        });
        this.about = about;
        this.contractor_id = contractor_id;
    }
}

export class RegisterContractee {
    constructor({ credentials, user }) {
        this.credentials = credentials;
        this.user = user;
    }
}

export class RegisterContractor {
    constructor({ credentials, user }) {
        this.credentials = credentials;
        this.user = user;
    }
}

export class CompleteContractee {
    constructor({ credentials, user }) {
        this.credentials = credentials;
        this.user = user;
    }
}

export class CompleteContractor {
    constructor({ credentials, user }) {
        this.credentials = credentials;
        this.user = user;
    }
}

export class CompleteAdmin {
    constructor({ credentials, user, contractor }) {
        this.credentials = credentials;
        this.user = user;
        this.contractor = contractor;
    }
}

export function concatFullname({ surname, name, patronymic }) {
    let fullName = `${surname} ${name}`;
    if (patronymic) {
        fullName += ` ${patronymic}`;
    }
    return fullName;
}
