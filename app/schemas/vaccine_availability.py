from datetime import date, datetime
from typing import List, Optional, Union
from uuid import UUID

from app.schemas.base import BaseModel
from app.schemas.enums import InputTypeEnum
from app.schemas.locations import LocationExpandedResponse


# ------------------------- Timeslots -------------------------
class VaccineAvailabilityTimeslotResponse(BaseModel):
    id: UUID
    vaccine_availability: UUID
    active: bool
    taken_at: Optional[datetime]
    created_at: datetime
    time: datetime


class VaccineAvailabilityTimeslotCreateRequest(BaseModel):
    parentID: UUID
    time: datetime


class VaccineAvailabilityTimeslotUpdateRequest(BaseModel):
    taken_at: Optional[datetime]


# ------------------------- Requirements -------------------------


class VaccineAvailabilityRequirementsResponse(BaseModel):
    id: int
    vaccine_availability: UUID
    requirement: int
    active: bool
    created_at: datetime


class VaccineAvailabilityRequirementsCreateRequest(BaseModel):
    requirements: List[int]


class VaccineAvailabilityRequirementsUpdateRequest(BaseModel):
    active: bool


# ----------------------------- Root -----------------------------
class VaccineAvailabilityResponseBase(BaseModel):
    numberAvailable: Optional[int]
    numberTotal: Optional[int]
    date: Optional[date]
    vaccine: Optional[int]
    inputType: Optional[InputTypeEnum]
    tags: Optional[str]


class VaccineAvailabilityResponse(VaccineAvailabilityResponseBase):
    id: UUID
    location: int
    created_at: datetime


class VaccineAvailabilityExpandedResponse(VaccineAvailabilityResponseBase):
    id: Union[UUID, int]
    location: LocationExpandedResponse
    created_at: datetime
    timeslots: List[VaccineAvailabilityTimeslotResponse]


class VaccineAvailabilityCreateRequest(VaccineAvailabilityResponseBase):
    location: int


class VaccineAvailabilityUpdateRequest(VaccineAvailabilityResponseBase):
    id: Union[UUID, int]
    location: int
