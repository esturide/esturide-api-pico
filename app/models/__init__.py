from fireo.models import Model
from fireo.fields import TextField, NumberField


class User(Model):
    name = TextField()
    age = NumberField()
