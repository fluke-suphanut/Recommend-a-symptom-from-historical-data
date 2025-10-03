from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend_symptoms

app = FastAPI()

class InputData(BaseModel):
    gender: str
    age: int
    symptoms: list[str]

@app.post("/recommend")
def get_recommendation(data: InputData):
    gender_value = 0 if data.gender.lower() == "male" else 1

    result = recommend_symptoms(
        gender=gender_value,
        age=data.age,
        user_symptoms=data.symptoms,
        top_n=5
    )
    return {"recommendations": result}
