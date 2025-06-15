from abc import abstractmethod, ABC
from app.src.dto.prediction_request import PredictionRequest

class BaseModel(ABC):

    def __init__(self, description: str) -> None:
        self._description = description

    @abstractmethod
    def predict_result(self, input: PredictionRequest) -> float:
        pass

    @property
    def desc(self) -> str:
        return self._description