import streamlit as st,pandas as pd,plotly.express as px
from utils.data import load_data
from utils.modeling import train_models
st.title('Machine Learning Model Performance'); st.write('Train classifiers and regressors using held-out test data.');
if st.button('Train / retrain models',type='primary'):
 with st.spinner('Training models...'):st.session_state['results']=train_models(load_data())
 st.success('Training complete. Best models saved in models/.')
r=st.session_state.get('results')
if r:
 st.subheader('Employment classification'); st.dataframe(pd.DataFrame(r['employment']).set_index('Model'),use_container_width=True); st.subheader('Salary regression'); st.dataframe(pd.DataFrame(r['salary']).set_index('Model'),use_container_width=True)
 st.subheader('Factors associated with employment classification')
 st.plotly_chart(px.bar(pd.DataFrame(r['employment_importance']).sort_values('Importance'),x='Importance',y='Feature',orientation='h',title='Permutation importance (F1 score)'),use_container_width=True)
 st.subheader('Factors associated with salary prediction')
 st.plotly_chart(px.bar(pd.DataFrame(r['salary_importance']).sort_values('Importance'),x='Importance',y='Feature',orientation='h',title='Permutation importance (negative MAE score)'),use_container_width=True)
else:st.info('Click Train / retrain models to evaluate and save models.')
st.caption('Holdout metrics on synthetic data are not evidence of real-world predictive validity.')
