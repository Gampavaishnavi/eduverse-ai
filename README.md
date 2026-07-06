# Eduverse AI – Student Decision Intelligence Platform

## Problem Statement
Educational institutions generate large volumes of academic data. Faculty often analyze these records manually after examinations, making interventions reactive rather than proactive. 
Eduverse AI automatically analyzes student performance, predicts academic risk, explains the causes of poor performance using AI, and recommends appropriate interventions before students fail.

## Architecture

The platform uses a modular architecture combining traditional machine learning with Generative AI.

### Google Cloud Architecture
Student Dataset -> Google Cloud Storage -> BigQuery -> NVIDIA RAPIDS cuDF -> Machine Learning -> Gemini -> Looker Dashboard -> Faculty Decision Support

### NVIDIA Integration
The data layer is designed with an abstraction to use NVIDIA RAPIDS cuDF if a GPU is available, providing significant acceleration for data processing. It gracefully falls back to pandas if a GPU is not present.

## Features
- **Predictive Analytics**: Random Forest/XGBoost models predict failure probabilities.
- **Decision Intelligence**: Gemini AI explains why a student is at risk and suggests interventions.
- **Dynamic Dashboards**: Interactive Plotly charts for class and student-level insights.
- **Reporting**: Downloadable PDF reports for students.

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: Scikit-learn, XGBoost
- **Visualization**: Plotly
- **Data**: Pandas / NVIDIA RAPIDS cuDF
- **AI**: Google Gemini API

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file from `.env.example` and add your `GEMINI_API_KEY`.
4. Run the app: `streamlit run app.py`

## Usage
1. Login as Faculty.
2. View the dashboard to see high-risk students.
3. Click on a student to view their detailed profile.
4. Interact with the Gemini AI to get specific recommendations.

## Future Scope
- Integration with LMS (Canvas, Moodle, Blackboard).
- Automated email alerts to students and parents.
- Trend forecasting using advanced time-series models.
