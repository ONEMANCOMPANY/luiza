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


class PlanModel(Base):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True, index=True)
    plan_name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String)
    created_by = db.Column(db.DateTime, server_default=func.now())

    def create_plan(plan):
        query = PlanModel(
            plan_id=plan.plan_id,
            plan_name=plan.plan_name,
            description=plan.description,
            price=plan.price
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

    def get_plans(plan):
        query = session.query(
            PlanModel.plan_name.label("plan_name"),
            PlanModel.description.label("description"),
            PlanModel.price.label("price")
        )
        try:
            results = PlanModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def dict_columns(query) -> dict:
        return [{
            "plan_id": data[0],
            "plan_name": data[1],
            "description": data[2],
            "price": data[3]
        } for data in query] 

