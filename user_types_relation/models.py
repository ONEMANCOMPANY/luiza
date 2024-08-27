import traceback
import sqlalchemy as db
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.sql import func
from sqlalchemy.orm import Query, relationship
from sqlalchemy.ext.declarative import declarative_base
from internal.database import PostgreSql, Base, session
from internal.security import hash_password
from user_types.models import TypeModel
from users.models import UserModel


class UserTypeRelationModel(Base):
    __tablename__ = "user_type_relation"

    id = db.Column(db.Integer, primary_key=True, index=True)
    type_id = db.Column(db.Integer, db.ForeignKey("types.type_id"), nullable=False) #type or subtype id
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    # Relacionamentos bidirecionais
    user = relationship("UserModel", back_populates="user_type")
    type = relationship("TypeModel", back_populates="user_type")

    def create_relation(relation):
        query = UserTypeRelationModel(
            type_id=relation.type_id,
            user_id=relation.user_id
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

    def get_relation(plan):
        query = session.query(
            UserTypeRelationModel.id.label("id"),
            UserTypeRelationModel.type_id.label("type_id"),
            UserTypeRelationModel.user_id.label("user_id")
        )
        try:
            results = UserTypeRelationModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def dict_columns(query) -> dict:
        return [{
            "id": data[0],
            "type_id": data[1],
            "user_id": data[2]
        } for data in query] 

