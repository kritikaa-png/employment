import streamlit as st,plotly.express as px
from utils.data import load_data
st.title('Employment Analysis'); d=load_data(); a=d.groupby('Industry').agg(Candidates=('Candidate_ID','count'),Employment_Rate=('Employment_Status',lambda s:(s=='Employed').mean())).reset_index(); b=d.groupby('Education').Employment_Status.apply(lambda s:(s=='Employed').mean()).reset_index(name='Employment_Rate'); c=d.groupby('Experience_Years').Employment_Status.apply(lambda s:(s=='Employed').mean()).reset_index(name='Employment_Rate')
x,y=st.columns(2)
with x:st.plotly_chart(px.bar(a,x='Industry',y='Employment_Rate',title='Employment rate by industry',range_y=[0,1]),use_container_width=True)
with y:st.plotly_chart(px.bar(b,x='Education',y='Employment_Rate',title='Employment rate by education',range_y=[0,1]),use_container_width=True)
st.plotly_chart(px.line(c,x='Experience_Years',y='Employment_Rate',markers=True,title='Employment rate by experience'),use_container_width=True); st.caption('Descriptive associations in simulated data, not causal effects or real hiring probabilities.')
