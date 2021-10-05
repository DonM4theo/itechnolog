from pydantic import BaseModel

class User(BaseModel):
    login: str
    hashed_password: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    is_active: bool
    can_edit: bool
    can_remove: bool
    can_create: bool
    is_admin: bool
    notification: bool