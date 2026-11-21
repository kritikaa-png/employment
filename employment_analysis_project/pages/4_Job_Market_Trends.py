import streamlit as st,plotly.express as px,pandas as pd
from utils.data import load_data
st.title('Job Market Trends'); st.warning('All observations are simulated; these are not real Indian labour-market trends.'); d=load_data(); y=d.groupby('Year').agg(Candidates=('Candidate_ID','count'),Employment_Rate=('Employment_Status',lambda s:(s=='Employed').mean())).reset_index()
st.plotly_chart(px.line(y,x='Year',y='Candidates',markers=True,title='Synthetic candidate records by year'),use_container_width=True); st.plotly_chart(px.line(y,x='Year',y='Employment_Rate',markers=True,title='Synthetic employment rate by year',range_y=[0,1]),use_container_width=True)
rows=[]
for _,r in d.dropna(subset=['Annual_Salary_INR']).iterrows():
 for skill in str(r.Skills).split(', '):rows.append((skill,r.Annual_Salary_INR))
s=pd.DataFrame(rows,columns=['Skill','Salary']).groupby('Skill',as_index=False).agg(Median_Salary=('Salary','median'),Mentions=('Salary','size')).sort_values('Median_Salary',ascending=False); st.plotly_chart(px.bar(s,x='Median_Salary',y='Skill',orientation='h',title='Median salary by listed skill'),use_container_width=True)
