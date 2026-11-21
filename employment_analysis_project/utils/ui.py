import streamlit as st
def inject_css():
 st.markdown('''<style>.stApp{background:#f5f7fb}.block-container{padding-top:1.7rem;max-width:1500px}[data-testid="stSidebar"]{background:#101d35}[data-testid="stSidebar"] *{color:#f4f7ff!important}div[data-testid="stMetric"]{background:white;padding:16px;border:1px solid #e7ebf3;border-radius:14px}h1,h2,h3{color:#172b4d}</style>''',unsafe_allow_html=True)
def sidebar_filters(d):
 st.sidebar.title('Employment Intelligence'); st.sidebar.caption('Explore synthetic records')
 for col,label in [('Industry','Industry'),('Location','Location'),('Year','Year')]:
  opts=sorted(d[col].dropna().unique()); chosen=st.sidebar.multiselect(label,opts)
  if chosen:d=d[d[col].isin(chosen)]
 st.sidebar.caption(f'{len(d):,} records selected'); return d
def kpi(c,label,value): c.metric(label,value)
