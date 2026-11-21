from pathlib import Path
import pandas as pd
import streamlit as st
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "employment_dataset_clean.xlsx"

@st.cache_data
def load_data():
    d=pd.read_excel(DATA_PATH,sheet_name='Dataset'); d['Annual_Salary_INR']=pd.to_numeric(d.Annual_Salary_INR,errors='coerce'); return d
def metrics(d):
    e=d[d.Employment_Status=='Employed']
    return {'candidates':len(d),'employment_rate':(d.Employment_Status=='Employed').mean() if len(d) else 0,'median_salary':e.Annual_Salary_INR.median() if len(e) else None}
