import streamlit as st,plotly.express as px
from utils.data import load_data
st.title('Salary Analysis'); d=load_data().dropna(subset=['Annual_Salary_INR']); a,b=st.columns(2)
with a:st.plotly_chart(px.box(d,x='Education',y='Annual_Salary_INR',title='Salary distribution by education'),use_container_width=True)
with b:st.plotly_chart(px.scatter(d,x='Experience_Years',y='Annual_Salary_INR',color='Industry',title='Salary vs experience',opacity=.65),use_container_width=True)
r=d.groupby('Job_Role',as_index=False).Annual_Salary_INR.median().sort_values('Annual_Salary_INR',ascending=False).head(15); st.plotly_chart(px.bar(r,x='Annual_Salary_INR',y='Job_Role',orientation='h',title='Top 15 roles by median synthetic salary'),use_container_width=True)
l=d.groupby('Location',as_index=False).Annual_Salary_INR.median(); st.plotly_chart(px.bar(l,x='Location',y='Annual_Salary_INR',title='Median salary by location'),use_container_width=True)
