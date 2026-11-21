import streamlit as st,pandas as pd
from utils.data import load_data
from utils.modeling import load_model
st.title('Interactive Predictions'); d=load_data(); sm=load_model('salary_model.pkl'); em=load_model('employment_model.pkl')
if sm is None or em is None:st.warning('Train models on the Model Performance page first.'); st.stop()
with st.form('candidate'):
 a,b,c=st.columns(3); edu=a.selectbox('Education',sorted(d.Education.unique())); ind=b.selectbox('Industry',sorted(d.Industry.unique())); role=c.selectbox('Job role',sorted(d.Job_Role.unique())); exp=a.slider('Experience (years)',0,35,3); loc=b.selectbox('Location',sorted(d.Location.unique())); et=c.selectbox('Employment type',sorted(d.Employment_Type.unique())); mode=a.selectbox('Work mode',sorted(d.Work_Mode.unique())); skills=b.slider('Number of skills',1,6,3); score=c.slider('Skill score',0,100,65); cert=a.slider('Certifications',0,4,1); go=st.form_submit_button('Predict',type='primary')
if go:
 x=pd.DataFrame([{'Education':edu,'Industry':ind,'Job_Role':role,'Location':loc,'Employment_Type':et,'Work_Mode':mode,'Experience_Years':exp,'Skill_Count':skills,'Skill_Score_0_100':score,'Certifications_Count':cert}]); salary=float(sm.predict(x)[0]); probability=float(em.predict_proba(x)[0,1]); u,v=st.columns(2); u.metric('Estimated annual salary',f'₹{salary:,.0f}'); v.metric('Estimated monthly salary',f'₹{salary/12:,.0f}'); st.metric('Model-estimated employment probability',f'{probability:.1%}'); bench=d[(d.Industry==ind)&(d.Job_Role==role)].Annual_Salary_INR.median()
 if pd.notna(bench):st.write(f'Dataset median for this role and industry: ₹{bench:,.0f} annually.')
 st.caption('Synthetic-data model output only; not a guaranteed salary, calibrated confidence interval, or actual hiring probability.')
