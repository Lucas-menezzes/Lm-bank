from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class CreateClient(BaseModel):
    username: str
    name:str
    adress: str
    email: str
    client_email: str
    phone: str
    agency: int
    account: int
    date_birth: datetime
    document: str

class CreateColaborator(BaseModel):
    username: str
    name : str
    phone: str
    email: str
    registration: int
    phone: str
    date_birth: datetime
    document: str
    agency: int
    nivel : str

class CreateAgency(BaseModel):
    phone: str
    adress : str
    agency_number: int
    
class AgencySchema(BaseModel):
    phone: str
    adress : str
    agency_number: int
    date_updated: datetime

class CreateWithdraw(BaseModel):
    value : Decimal
    agency : int
    account : int
    # username : str

class CreateDeposit(BaseModel):
    value: Decimal
    agency : int
    account : int
    name: str

