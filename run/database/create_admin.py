import asyncio
from application.usecases.auth.create_user_use_case import CreateAdminUseCase
from domain.dto.user.request.admin.create_admin_dto import (
    AdminInputDTO,
    CreateAdminDTO,
)
from domain.dto.user.request.user_input_dto import (
    CredentialsInputDTO,
    WebCredentialsInputDTO,
)
from infrastructure.app.app import App
from infrastructure.database.models import Base


async def main():
    app = App()
    await app.database.create_database(Base.metadata)

    use_case = CreateAdminUseCase(
        admin_command_repository=app.container.admin_command_repository(),
        create_credentials_use_case=app.container.create_credentials_use_case(),
    )

    request = CreateAdminDTO(
        user=AdminInputDTO(
            surname="Чурилов",
            name="Димитрий",
            patronymic="Александрович",
            phone_number="+79002977098",
            photos=[],
            about="Разработчик",
        ),
        credentials=CredentialsInputDTO(
            web=WebCredentialsInputDTO(
                email="nationmdxr@gmail.com", password="246224682"
            )
        ),
    )

    await use_case.execute(request)


if __name__ == "__main__":
    asyncio.run(main())
