import streamlit as st
from utils.data import load_data, metrics
from utils.ui import inject_css, sidebar_filters, kpi
from utils.charts import employment_donut, salary_by_industry, salary_trend
st.set_page_config(page_title='Employment Intelligence', page_icon='📊', layout='wide')
inject_css(); df=load_data()
st.title('Employment Intelligence'); st.caption('Employment analysis • Salary prediction • Job-market insights')
df=sidebar_filters(df); m=metrics(df)
cols=st.columns(4)
kpi(cols[0],'Candidates',f"{m['candidates']:,}"); kpi(cols[1],'Employment rate',f"{m['employment_rate']:.1%}"); kpi(cols[2],'Median annual salary',f"₹{m['median_salary']:,.0f}" if m['median_salary'] else '—'); kpi(cols[3],'Industries',str(df.Industry.nunique()))
a,b=st.columns(2)
with a: st.subheader('Employment status'); st.plotly_chart(employment_donut(df),use_container_width=True)
with b: st.subheader('Median salary by industry'); st.plotly_chart(salary_by_industry(df),use_container_width=True)
st.subheader('Salary trend by observation year'); st.plotly_chart(salary_trend(df),use_container_width=True)
st.info('This is a fully synthetic educational dataset. Results do not represent actual labour-market conditions or real candidates.')
