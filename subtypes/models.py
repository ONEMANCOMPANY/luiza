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



class SubTypeModel(Base):
    __tablename__ = "subtypes"

    subtype_id = db.Column(db.Integer, primary_key=True, index=True)
    subtype_name = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey("types.type_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    type = relationship("TypeModel", back_populates="subtypes")

    def create_user_subtype(subtype):
        query = SubTypeModel(
            subtype_name=subtype.subtype_name,
            type_id=subtype.type_id
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

    def get_subtype(subtype):
        query = session.query(
            SubTypeModel.subtype_id.label("subtype_id"),
            SubTypeModel.subtype_name.label("subtype_name"),
            SubTypeModel.type_id.label("type_id"),
        )
        if subtype:
            query = query.filter(SubTypeModel.subtype_id==subtype)
        query = query.all()
        try:
            results = SubTypeModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def dict_columns(query) -> dict:
        return [{
            "susubbtype_id": data[0],
            "subtype_name": data[1],
            "type_id": data[2]
        } for data in query] 

