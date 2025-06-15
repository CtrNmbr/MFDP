from typing import List
from uuid import UUID

from pydantic import BaseModel,Field

class PredictTaskPayload(BaseModel):
    id: UUID = Field()
    user_id: int = Field()
    fixed_acidity: float  = Field()#= Field(alias='fixed acidity')
    volatile_acidity: float  = Field()#= Field(alias='volatile acidity')
    citric_acid: float  = Field()#= Field(alias='citric acid')
    residual_sugar: float  = Field()#= Field(alias='residual sugar')
    chlorides: float = Field()#= Field()
    free_sulfur_dioxide: float  = Field()#= Field(alias='free sulfur dioxide')
    total_sulfur_dioxide: float  = Field()#= Field(alias='total sulfur dioxide') не пройдет валидацию - так как она по алиасам - а до этого заменилось на поля с _
    density: float = Field()
    pH: float = Field()
    sulphates: float = Field()
    alcohol: float = Field()
    account_transaction_id: int = Field()
    class Config:
        allow_population_by_field_name = True  # Accept both keys
    #worker-2     |     data = PredictTaskPayload.model_validate_json(body)
    #worker-2     |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #worker-2     |   File "/usr/local/lib/python3.11/site-packages/pydantic/main.py", line 531, in model_validate_json
    #worker-2     |     return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)
    #worker-2     |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #worker-2     | pydantic_core._pydantic_core.ValidationError: 6 validation errors for PredictTaskPayload
    #worker-2     | fixed acidity
    #worker-2     |   Field required [type=missing, input_value={'id': '61283b38-cfaa-494...ount_transaction_id': 1}, input_type=dict]
    #worker-2     |     For further information visit https://errors.pydantic.dev/2.3/v/missing
    #worker-2     | volatile acidity
