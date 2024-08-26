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


class UserPlanModel(Base):
    __tablename__ = "user_plan"

    id = db.Column(db.Integer, primary_key=True, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.plan_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    # Relacionamentos bidirecionais
    user = relationship("UserModel", back_populates="user_plans")
    plan = relationship("PlanModel", back_populates="plan_users")

    def create_relation(relation):
        query = UserPlanModel(
            plan_id=relation.plan_id,
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
            UserPlanModel.id.label("id"),
            UserPlanModel.plan_id.label("plan_id"),
            UserPlanModel.user_id.label("user_id")
        )
        try:
            results = UserPlanModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def dict_columns(query) -> dict:
        return [{
            "id": data[0],
            "plan_id": data[1],
            "user_id": data[2]
        } for data in query] 

