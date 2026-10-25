# Insurance Premium Prediction API

A FastAPI service that predicts an insurance premium category from basic applicant information. The API derives BMI, age group, lifestyle risk, and city tier from the submitted data, then returns the model's predicted category, confidence, and class probabilities.

## Requirements

- Python version compatible with the pinned dependencies
- Dependencies listed in [`requirements.txt`](./requirements.txt)

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Run the API

Start the development server from the project root:

```bash
uvicorn app:app --reload
```

The service runs at `http://127.0.0.1:8000` by default. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Service and model health information |
| `POST` | `/predict` | Predict an insurance premium category |

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "OK",
  "version": "1.25.30",
  "model_loaded": true
}
```

### Make a prediction

Send a JSON object to `POST /predict`:

```json
{
  "age": 35,
  "weight": 72,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Pune",
  "occupation": "private_job"
}
```

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"age\":35,\"weight\":72,\"height\":1.75,\"income_lpa\":12.5,\"smoker\":false,\"city\":\"Pune\",\"occupation\":\"private_job\"}"
```

The response contains the predicted category, its confidence, and probabilities for each category:

```json
{
  "response": {
    "predicted_category": "example_category",
    "confidence": 0.91,
    "class_probabilities": {
      "example_category": 0.91,
      "another_category": 0.09
    }
  }
}
```

The category names and probability values are determined by the bundled model.

### Input fields

| Field | Type | Constraints / notes |
| --- | --- | --- |
| `age` | Integer | Greater than 0 and less than 120 |
| `weight` | Number | Greater than 0; in kilograms |
| `height` | Number | Greater than 0; in meters |
| `income_lpa` | Number | Greater than 0; annual income in lakhs per annum |
| `smoker` | Boolean | Whether the applicant smokes |
| `city` | String | City name; surrounding whitespace is removed and capitalization normalized |
| `occupation` | String | One of `retired`, `freelancer`, `student`, `government_job`, `bussiness_owner`, `unemployed`, or `private_job` |

The API derives BMI from weight and height, maps age to an age group, estimates lifestyle risk from smoking and BMI, and assigns a city tier from the configured city lists. Cities not listed in the tier 1 or tier 2 configuration are assigned tier 3.

## Project structure

```text
app.py                       FastAPI application and API routes
config/city_tier.py          Tier 1 and tier 2 city lists
model/model.pkl              Serialized prediction model
model/predict.py             Model loading and prediction logic
schema/user_input.py         Input validation and derived features
schema/prediction_response.py Prediction response schema
requirements.txt             Python dependencies
```

Predictions are model-generated estimates and should not be treated as financial or insurance advice.
