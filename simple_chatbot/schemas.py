from pydantic import BaseModel

class Person(BaseModel):
    """
    Represents a person with a name and age.
    """
    name: str
    age: int
    occupation: str

