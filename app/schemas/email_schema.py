from pydantic import BaseModel, EmailStr


class EmailBase(BaseModel):
    email: EmailStr

class EmailCreate(EmailBase):
    pass

class EmailUpdate(EmailBase):
    pass

class EmailResponse(EmailBase):
    id  : int

    class Config:
        orm_mode = True

