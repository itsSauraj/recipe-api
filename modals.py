from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime

from pydantic import UUID4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped
import uuid

class DBBaseModel(DeclarativeBase):
    created_at: Mapped[str] = mapped_column(default=datetime.now)
    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)

class BaseModel(PydanticBaseModel):
    id: UUID4 | None = None
    created_at: datetime | None = None

class User(BaseModel):
    name: str
    email: str

class UserInDB(User):
    password: str
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'name': 'John Doe',
                'email': 'jhondoe@gmail.com',
                'password': 'password'
            }
        }
    }
    
class Token(PydanticBaseModel):
    access_token: str
    token_type: str
    
class TokenData(PydanticBaseModel):
    username: str | None = None


class DBUserModal(DBBaseModel):
    __tablename__ = "user_account"

    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    
    recipies: Mapped[list["DBRecipeModal"]] = relationship("DBRecipeModal", back_populates="owner")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
      
class Recipie(BaseModel):
    name: str | None = None
    ingredients: str | None = None
    instructions: str | None = None
    owner_id: UUID4 | None = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Recipe Name",
                "ingredients": "Ingredients",
                "instructions": "Instructions",
            }
        }
    }
    
    
class UpdateRecipie(PydanticBaseModel):
    name: str | None = None
    ingredients: str | None = None
    instructions: str | None = None
      
class DBRecipeModal(DBBaseModel):
    __tablename__ = "recipie"

    name: Mapped[str]= mapped_column(nullable=True)
    ingredients: Mapped[str]= mapped_column(nullable=True)
    instructions: Mapped[str]= mapped_column(nullable=True)
    owner_id: Mapped[str]= mapped_column(ForeignKey("user_account.id"))

    owner: Mapped[DBUserModal] = relationship("DBUserModal", back_populates="recipies")
    
    def __repr__(self) -> str:
        return f"Recipie(id={self.id!r}, title={self.name!r})"