import pickle
import pandas as pd

# import ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.25.30'

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])
    predicted_class = model.predict(input_df)[0]

    probalities = model.predict_proba(input_df)[0]
    confidence = max(probalities)

    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probalities)))

    return {
        'predicted_category': predicted_class,
        'confidence': round(confidence, 4),
        'class_probabilities': class_probs
    }