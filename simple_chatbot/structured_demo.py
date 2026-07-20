from dotenv import load_dotenv
from schemas import Person
from config import model

load_dotenv()


chain = model.with_structured_output(Person)

response = chain.invoke("Tell me about Elon Musk")
print(response)
