import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

class MLEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = ['Attendance', 'Assignment_Score', 'Quiz_Score', 'Mid_Exam', 'Study_Hours']
        self.is_trained = False
        
    def train(self, df):
        # We need a target variable. Let's create one based on Result or final exam if Result is not present
        if 'Result' in df.columns:
            # Pass = 0, Fail = 1 for risk probability
            y = df['Result'].apply(lambda x: 1 if x == 'Fail' else 0)
        else:
            y = df['Final_Exam'].apply(lambda x: 1 if x < 50 else 0)
            
        X = df[self.features].fillna(df[self.features].mean())
        self.model.fit(X, y)
        self.is_trained = True
        
    def predict_risk(self, df):
        if not self.is_trained:
            # Fallback heuristic if not trained
            risk_score = 100 - df['Attendance']
            return risk_score.clip(0, 100), ["Medium"] * len(df)
            
        X = df[self.features].fillna(df[self.features].mean())
        # Probability of class 1 (Fail)
        probs = self.model.predict_proba(X)[:, 1]
        
        risk_scores = probs * 100
        categories = []
        for score in risk_scores:
            if score >= 70:
                categories.append("High")
            elif score >= 40:
                categories.append("Medium")
            else:
                categories.append("Low")
                
        return risk_scores, categories
