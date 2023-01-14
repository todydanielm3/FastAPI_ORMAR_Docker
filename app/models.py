import databases
import ormar



class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

class Usuario(ormar.Model):
    class Meta(BaseMeta):
        pass


    id: int = ormar.Integer(primary_key=True)
    cpf: int = ormar.Integer(name="cpf")
    nome: str = ormar.String(max_length=100)
    email: str = ormar.String(max_length=200)
    telefone: int = ormar.Integer(name="telefone")
