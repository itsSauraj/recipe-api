from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.orm import Session

from pydantic import UUID4

from modals import DBUserModal
from database.engine import engine
from database.utils import load_initial_data

class UserFunction:
    def get_user_by_email(email: str):
        ''' Dababase call to Get user by email '''
        with engine.connect() as conn:
            query = select(DBUserModal).where(DBUserModal.email == email)
            result = conn.execute(query, {"email": email})
        return result.first()

    def get_user_by_id(user_id: UUID4):
        ''' Database call to Get user by id '''
        with engine.connect() as conn:
            query = select(DBUserModal).where(DBUserModal.id == str(user_id))       
            result = conn.execute(query, {"id": user_id})
        return result.first()

    @load_initial_data
    def create_user(user: DBUserModal):
        ''' Databse call to Create new user '''
        with Session(engine) as session:
            query = insert(DBUserModal).values(**user.dict())
            result = session.execute(query)
            session.commit()
        return result