from app.src.base.base_model import BaseModel
import pathlib
import joblib
import pandas as pd
import sklearn

from app.src.dto.prediction_request import PredictionRequest

def get_model() -> BaseModel:
    return ModelStarter()

class ModelStarter(BaseModel):
    def __init__(self):
        super().__init__("Description of the model")
        path = pathlib.Path(__file__).parent.parent / "local_model" / "wine_quality_model.pkl"
        #path = pathlib.Path(__file__).parent / "local_model" / "wine_quality_model.pkl"
        #print(path)#/app/src/base/local_model/wine_quality_model.pkl
        if path.exists():
            with open(path, 'rb') as file:
                self.model = joblib.load(file)
        else:
            raise Exception('Model doesnt exist')

    def predict_result(self, input: PredictionRequest) -> float:
        input_data = input  # чтобы по алиасам! без этого  либо missed поле - когда передавали без пробелов в body или когда передавали с пробелами в body ошибка 500 internal server error
        input_df = pd.DataFrame(input_data, index=[0])
        result = self.model.predict(input_df)[0]
        return result