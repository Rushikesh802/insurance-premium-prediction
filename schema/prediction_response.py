from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):

    predicted_category: str = Field(..., description='The predicted insurace premium category')
    confidence: float = Field(..., description='Model confidence score for the predicted class form 0 to 1')
    class_probabilities: Dict[str, float] = Field(..., description='Probabilty description among all categories')

    