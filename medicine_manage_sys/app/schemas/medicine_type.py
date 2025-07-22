from pydantic import BaseModel


class MedicineTypeBase(BaseModel):
    id: str
    type_name: str


class MedicineType(BaseModel):
    type_name: str


class MedicineTypeCreate(MedicineType):
    pass


class MedicineTypeUpdate(MedicineType):
    pass


