from datetime import datetime

from pydantic import BaseModel,Field

class Prediction(BaseModel):
    id: int = Field() # так как валидация типов на алиасах то ломается при выдаче истории
    fixed_acidity: float = Field() #= Field(alias='fixed acidity')
    volatile_acidity: float = Field() #= Field(alias='volatile acidity')
    citric_acid: float = Field() #= Field(alias='citric acid')
    residual_sugar: float = Field()#= Field(alias='residual sugar')
    chlorides: float = Field()
    free_sulfur_dioxide: float = Field()#= Field(alias='free sulfur dioxide')
    total_sulfur_dioxide: float = Field() #= Field(alias='total sulfur dioxide')
    density: float = Field()
    pH: float = Field()
    sulphates: float = Field()
    alcohol: float = Field()
    predicted_quality: float = Field()
    created_at: datetime = Field()
    class Config:
        allow_population_by_field_name = True  # Accept both keys