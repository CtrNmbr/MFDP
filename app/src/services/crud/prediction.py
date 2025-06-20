from typing import List

from sqlmodel import Session, select

from app.src.models.quality_prediction import QualityPrediction


def create_prediction(
    prediction: QualityPrediction, session: Session
) -> QualityPrediction:
    session.add(prediction)#todo
    session.commit()
    session.refresh(prediction)
    return prediction


def get_predictions(user_id: int, session: Session) -> List[QualityPrediction]:
    statement = select(QualityPrediction).where(
        QualityPrediction.user_id == user_id
    )
    predictions = session.exec(statement).all()
    print(predictions)
    return predictions
