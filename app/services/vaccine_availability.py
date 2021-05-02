from typing import List, Optional, Type
from uuid import UUID

from app.schemas.misc import FilterParamsBase
from app.schemas.vaccine_availability import (
    VaccineAvailabilityExpandedResponse,
    VaccineAvailabilityResponse,
    VaccineAvailabilityCreateRequest,
    VaccineAvailabilityUpdateRequest,
)
from app.services.base import BaseService
from app.services.locations import LocationService
from app.services.organizations import OrganizationService
from loguru import logger


class VaccineAvailabilityService(
    BaseService[
        VaccineAvailabilityResponse,
        VaccineAvailabilityCreateRequest,
        VaccineAvailabilityUpdateRequest,
    ]
):
    read_procedure_id_parameter = "availabilityID"

    @property
    def table(self) -> str:
        return "vaccine_availability"

    @property
    def db_response_schema(self) -> Type[VaccineAvailabilityResponse]:
        return VaccineAvailabilityResponse

    @property
    def create_response_schema(self) -> Type[VaccineAvailabilityCreateRequest]:
        return VaccineAvailabilityCreateRequest

    @property
    def update_response_schema(self) -> Type[VaccineAvailabilityUpdateRequest]:
        return VaccineAvailabilityUpdateRequest
    
    async def _expand(
        self,
        vaccine_availability: VaccineAvailabilityResponse
    ) -> VaccineAvailabilityExpandedResponse:
        location = await LocationService(self._db).get_by_id_expanded(
            vaccine_availability.location
        )
        assert (
            location is not None
        ), f"""
            Could not find location {vaccine_availability.location}
            for vaccine_availability {vaccine_availability.id}
            """

        vaccine_availability_expanded = vaccine_availability.dict()
        vaccine_availability_expanded.update({
            'location': location,
        })
        
        # logger.critical(vaccine_availability_expanded)

        return VaccineAvailabilityExpandedResponse(
            **vaccine_availability_expanded
        )
        

    async def get_by_id_expanded(
        self, id: UUID
    ) -> Optional[VaccineAvailabilityExpandedResponse]:
        vaccine_availability = await super().get_by_id(id)

        if vaccine_availability is not None:
            return await self._expand(vaccine_availability=vaccine_availability)

        return vaccine_availability

    async def get_all_expanded(
        self, filters: Optional[FilterParamsBase] = None
    ) -> List[VaccineAvailabilityExpandedResponse]:
        vaccine_availabilities = await super().get_all(filters=filters)

        # TODO: should be done all at once instead of in a for loop
        vaccine_availabilities_expanded: List[VaccineAvailabilityExpandedResponse] = []
        for vaccine_availability in vaccine_availabilities:
            vaccine_availabilities_expanded.append(await self._expand(vaccine_availability))

        return vaccine_availabilities_expanded