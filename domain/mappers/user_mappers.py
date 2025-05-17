from domain.dto.user.base import UserCredentialsDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.admin.create_admin_dto import AdminInputDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    ContracteeInputDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    ContractorInputDTO,
)
from domain.dto.user.request.user_input_dto import (
    TelegramCredentialsInputDTO,
    WebCredentialsInputDTO,
)
from domain.dto.user.response.admin.admin_output_dto import (
    AdminOutputDTO,
    AdminProfileOutputDTO,
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
    ContracteeOutputDTO,
    ContracteeProfileOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
    ContractorOutputDTO,
    ContractorProfileOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    CompleteUserOutputDTO,
    TelegramCredentialsOutputDTO,
    UserCredentialsOutputDTO,
    UserOutputDTO,
    UserProfileOutputDTO,
    WebCredentialsOutputDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.context import UserContext
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import (
    TelegramCredentials,
    UserCredentials,
    WebCredentials,
)
from domain.entities.user.user import User
from domain.mappers.base import from_entity_to_dto, from_dto_to_entity


class UserMapper:
    @staticmethod
    def to_output(user: User) -> UserOutputDTO:
        return from_entity_to_dto(user, UserOutputDTO)

    @staticmethod
    def to_profile(user: User) -> UserProfileOutputDTO:
        return from_entity_to_dto(user, UserProfileOutputDTO)


class UserRoleMapper:
    @staticmethod
    def to_output(
        user: Admin | Contractor | Contractee,
    ) -> AdminOutputDTO | ContracteeOutputDTO | ContractorOutputDTO:
        mapper = {
            Admin: AdminOutputDTO,
            Contractor: ContractorOutputDTO,
            Contractee: ContracteeOutputDTO,
        }
        return from_entity_to_dto(
            user,
            mapper.get(type(user), UserOutputDTO),
        )

    @staticmethod
    def to_profile(
        user: Admin | Contractor | Contractee,
    ) -> (
        AdminProfileOutputDTO
        | ContractorProfileOutputDTO
        | ContracteeProfileOutputDTO
    ):
        mapper = {
            Admin: AdminProfileOutputDTO,
            Contractor: ContractorProfileOutputDTO,
            Contractee: ContracteeProfileOutputDTO,
        }
        return from_entity_to_dto(
            user,
            mapper.get(type(user), UserProfileOutputDTO),
        )

    @staticmethod
    def to_complete(
        user: CompleteAdmin | CompleteContractor | CompleteContractee,
    ) -> (
        CompleteAdminOutputDTO
        | CompleteContractorOutputDTO
        | CompleteContracteeOutputDTO
    ):
        mapper = {
            CompleteAdmin: CompleteAdminOutputDTO,
            CompleteContractor: CompleteContractorOutputDTO,
            CompleteContractee: CompleteContracteeOutputDTO,
        }
        return from_entity_to_dto(
            user,
            mapper.get(type(user), CompleteUserOutputDTO),
        )


class ContracteeMapper:
    @staticmethod
    def to_output(user: Contractee) -> ContracteeOutputDTO:
        return from_entity_to_dto(user, ContracteeOutputDTO)

    @staticmethod
    def to_profile(user: Contractee) -> ContracteeProfileOutputDTO:
        return from_entity_to_dto(user, ContracteeProfileOutputDTO)

    @staticmethod
    def to_complete(user: CompleteContractee) -> CompleteContracteeOutputDTO:
        return from_entity_to_dto(user, CompleteContracteeOutputDTO)

    @staticmethod
    def from_input(
        request: ContracteeInputDTO,
    ) -> Contractee:
        return from_dto_to_entity(request, Contractee)


class ContractorMapper:
    @staticmethod
    def to_output(user: Contractor) -> ContractorOutputDTO:
        return from_entity_to_dto(user, ContractorOutputDTO)

    @staticmethod
    def to_profile(user: Contractor) -> ContractorProfileOutputDTO:
        return from_entity_to_dto(user, ContractorProfileOutputDTO)

    @staticmethod
    def to_complete(user: CompleteContractor) -> CompleteContractorOutputDTO:
        return from_entity_to_dto(user, CompleteContractorOutputDTO)

    @staticmethod
    def from_input(
        request: ContractorInputDTO,
    ) -> Contractor:
        return from_dto_to_entity(request, Contractor)


class AdminMapper:
    @staticmethod
    def to_output(user: Admin) -> AdminOutputDTO:
        return from_entity_to_dto(user, AdminOutputDTO)

    @staticmethod
    def to_profile(user: Admin) -> AdminProfileOutputDTO:
        return from_entity_to_dto(user, AdminProfileOutputDTO)

    @staticmethod
    def to_complete(user: CompleteAdmin) -> CompleteAdminOutputDTO:
        return from_entity_to_dto(user, CompleteAdminOutputDTO)

    @staticmethod
    def from_input(
        request: AdminInputDTO,
    ) -> Admin:
        return from_dto_to_entity(request, Admin)


class TelegramCredentialsMapper:
    @staticmethod
    def to_output(creds: TelegramCredentials) -> TelegramCredentialsOutputDTO:
        return from_entity_to_dto(creds, TelegramCredentialsOutputDTO)

    @staticmethod
    def from_input(
        creds: TelegramCredentialsInputDTO, user_id: int
    ) -> TelegramCredentials:
        return from_dto_to_entity(creds, TelegramCredentials, user_id=user_id)


class WebCredentialsMapper:
    @staticmethod
    def to_output(creds: WebCredentials) -> WebCredentialsOutputDTO:
        return from_entity_to_dto(creds, WebCredentialsOutputDTO)

    @staticmethod
    def from_input(
        creds: WebCredentialsInputDTO, user_id: int
    ) -> WebCredentials:
        return from_dto_to_entity(creds, WebCredentials, user_id=user_id)


class UserCredentialsMapper:
    @staticmethod
    def to_output(creds: UserCredentials) -> UserCredentialsOutputDTO:
        return from_entity_to_dto(creds, UserCredentialsOutputDTO)


class UserContextMapper:
    @staticmethod
    def to_dto(context: UserContext) -> UserContextDTO:
        return from_entity_to_dto(context, UserContextDTO)
