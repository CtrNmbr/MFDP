from pydantic import BaseModel,Field

class PredictionRequest(BaseModel):
    fixed_acidity: float = Field(alias='fixed acidity')
    volatile_acidity: float = Field(alias='volatile acidity')
    citric_acid: float = Field(alias='citric acid')
    residual_sugar: float = Field(alias='residual sugar')
    chlorides: float = Field()
    free_sulfur_dioxide: float = Field(alias='free sulfur dioxide')
    total_sulfur_dioxide: float = Field(alias='total sulfur dioxide')
    density: float = Field()
    pH: float = Field()
    sulphates: float = Field()
    alcohol: float = Field()
    # задачи начали приниматься в запросе через worker-2     | Received task: id=UUID('e53569b9-e0f5-40ca-b4b6-b47e0840c10b') user_id=1 fixed_acidity=0.0 volatile_acidity=0.0 citric_acid=0.0 residual_sugar=0.0 chlorides=0.0 free_sulfur_
    # dioxide=0.0 total_sulfur_dioxide=0.0 density=0.0 pH=0.0 sulphates=0.0 alcohol=0.0 account_transaction_id=1
    # но соответственно поля с нижними подчеркиваниями все-равно
    class Config:
        allow_population_by_field_name = True  # Accept both keys