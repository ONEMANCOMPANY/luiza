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



class UserModel(Base):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    phone = db.Column(db.String)
    mail = db.Column(db.String)
    cpf_cnpj = db.Column(db.String)
    user_since = db.Column(db.DateTime, server_default=func.now())
    password = db.Column(db.String)

    user_plans = relationship("UserPlanModel", back_populates="user")

    def create_user(user):
        password = hash_password(user.password)
        query = UserModel(
            name=user.name, 
            surname=user.surname,
            phone=user.phone,
            mail=user.mail,
            cpf_cnpj=user.cpf_cnpj,
            password=password.decode('utf8')
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

    def get_user(user):
        query = session.query(
            UserModel.user_id.label("user_id"),
            UserModel.name.label("name"),
            UserModel.surname.label("surname"),
            UserModel.phone.label("phone"),
            UserModel.mail.label("mail"),
            UserModel.cpf_cnpj.label("cpf_cnpj"),
            UserModel.user_since.label("user_since")
        )
        if user:
            query = query.filter(UserModel.user_id==user)
        query = query.all()
        try:
            results = UserModel.dict_columns(query)
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def get_user_email(email: str):
        query = session.query(
            UserModel.user_id.label("user_id"),
            UserModel.name.label("name"),
            UserModel.surname.label("surname"),
            UserModel.phone.label("phone"),
            UserModel.mail.label("mail"),
            UserModel.cpf_cnpj.label("cpf_cnpj"),
            UserModel.user_since.label("user_since")
        ).filter(UserModel.mail==email)
        query = query.all()
        try:
            results = UserModel.dict_columns(query)
            print(f'RESULTS::: {results}')
            return results
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def get_password_email(email: str):
        query = session.query(
            UserModel.password.label("password"),
            UserModel.mail.label("mail")
        ).filter(UserModel.mail==email)
        query = query.all()
        try:
            results = [passw for passw in query]
            return results[0]
        except Exception as error:
            print(error)
            traceback.print_exc()
        finally:
            session.close()

    def change_password(user_id: str, new_password: str):
        password = hash_password(new_password)

        db_item = session.query(UserModel).filter(
            UserModel.user_id == user_id
        ).first()

        print(f'DB ITEM::: {db_item}')

        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update the fields you need
        db_item.password = password.decode("utf8")

        session.commit()
        session.refresh(db_item)
        session.close()       

    def dict_columns(query) -> dict:
        return [{
            "user_id": data[0],
            "name": data[1],
            "surname": data[2],
            "phone": '({}) {}-{}-{}'.format(data[3][0:2], data[3][2] ,data[3][3:7], data[3][7:]),
            "mail": data[4],
            "cpf_cnpj": data[5],
            "user_since": data[6],
        } for data in query] 

