import traceback
import sqlalchemy as db
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.sql import func
from sqlalchemy.orm import Query, relationship
from sqlalchemy.ext.declarative import declarative_base
from internal.database import PostgreSql, Base, session, postgresql
from internal.security import hash_password



class TypeModel(Base):
    __tablename__ = "types"

    type_id = db.Column(db.Integer, primary_key=True, index=True)
    type_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())

    subtypes = relationship("SubTypeModel", back_populates="type")

    def create_user_type(type):
        query = TypeModel(
            type_name=type.type_name
        )
        try:
            session.add(query)
            session.commit()
            return query
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def get_type(type):
        query = session.query(
            TypeModel.type_id.label("type_id"),
            TypeModel.type_name.label("type_name")
        )
        if type:
            query = query.filter(TypeModel.type_id==type)
        query = query.all()
        try:
            results = TypeModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def dict_columns(query) -> dict:
        return [{
            "type_id": data[0],
            "type_name": data[1]
        } for data in query] 

