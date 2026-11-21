# Employment Intelligence & Salary Prediction

A Streamlit educational application for employment analysis, salary regression, employment classification, and simulated job-market trends.

## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Workflow
1. Open **Machine Learning Model Performance** and click **Train / retrain models**.
2. Models are saved to `models/employment_model.pkl` and `models/salary_model.pkl`.
3. Open **Interactive Predictions** to test candidate profiles.
4. Explore the analysis pages.

## Data and limitations
The included workbook contains 1,500 fully synthetic records. It does not represent actual candidates, employers, vacancies, or Indian labour-market statistics. Salary regression uses employed records only. Employment classification predicts the synthetic Employment_Status label. Candidate_ID and age are excluded from model features. Never use this educational prototype to make real hiring decisions. Holdout performance on synthetic data is not proof of real-world validity.
