import streamlit as st
from utils.data import load_data
st.title('Dataset Explorer'); d=load_data(); a,b,c=st.columns(3); a.metric('Rows',f'{len(d):,}'); b.metric('Columns',len(d.columns)); c.metric('Missing cells',int(d.isna().sum().sum()))
st.dataframe(d,use_container_width=True,height=520); st.subheader('Missing-value profile'); st.bar_chart(d.isna().mean().sort_values(ascending=False)); st.download_button('Download CSV',d.to_csv(index=False).encode(), 'employment_dataset.csv','text/csv')
