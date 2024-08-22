import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# engine = create_engine('sqlite:///meta.db', echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

class PostgreSql:
    """
        Classe que agrupa as funções de
        gerenciamento do PostgreSql.
    """

    def __init__(self, user, password, host, port, database):
        """
            Classe que instancia as conexões com
            o serviço PostgreSql.
            PARAMETROS:
                user: Username do PostgreSql;
                password: Senha do PostgreSql;
                host: Ponto de acesso do PostgreSql;
                port: Porta do ponto de acesso do PostgreSql;
                database: Banco de dados do PostgreSql.
        """

        args = {
            'connect_args': {
                'options': f'-c timezone=America/Sao_Paulo'
            }
        }

        self.connection = f"postgresql://{user}:{password}@{host}/{database}"
        self.engine = create_engine(self.connection, **args)

    def get_engine(self):
        """
            Obtém a sessão com o PostgreSql
            RETURN:
                Retorna a engine
        """

        return self.engine

    def create_session(self):
        """
            Cria uma sessão com o PostgreSql.
            RETURN:
                Retorna a sessão criada.
        """

        try:
            self.Session = sessionmaker(self.engine)
            self.session = self.Session()
            return self.session
        except Exception as error:
            print(f"ERROR: funcion {PostgreSql.create_session.__name__} -> error -> {str(error)}")
            return str(error)

    def close_engine(self):
        """
            Obtém a sessão com o PostgreSql
            RETURN:
                Fecha a engine
        """

        try:
            self.engine.dispose()
        except Exception as error:
            print(f"ERROR: funcion {PostgreSql.close_engine.__name__} -> error -> {str(error)}")
