import databases
import ormar
import sqlalchemy
from fastapi import FastAPI
from fastapi_crudrouter import OrmarCRUDRouter
#from config import settings

DATABASE_URL = "postgresql://danielmoraes:1234@localhost/postgres"
#DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

#DATABASE_URL = "postgresql://postgres:1234@localhost/postgres" #via Docker

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


def _setup_database():
    # if you do not have the database run this once
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine, database


class Usuario(ormar.Model):
    class Meta(BaseMeta):
        pass


    id: int = ormar.Integer(primary_key=True)
    cpf: int = ormar.Integer(name="cpf")
    nome: str = ormar.String(max_length=100)
    email: str = ormar.String(max_length=200)
    telefone: int = ormar.Integer(name="telefone")

app.include_router(
    OrmarCRUDRouter(
        schema=Usuario,delete_all_route=False,
        prefix="usuario",
    )
)

