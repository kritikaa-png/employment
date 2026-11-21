import plotly.express as px
TEAL='#19a7a1'
def employment_donut(d):
 x=d.Employment_Status.value_counts().rename_axis('Status').reset_index(name='Candidates')
 f=px.pie(x,names='Status',values='Candidates',hole=.62,color='Status',color_discrete_map={'Employed':TEAL,'Not Employed':'#e6a44b'}); f.update_layout(margin=dict(l=5,r=5,t=20,b=5)); return f
def salary_by_industry(d):
 x=d.dropna(subset=['Annual_Salary_INR']).groupby('Industry',as_index=False).Annual_Salary_INR.median().sort_values('Annual_Salary_INR')
 f=px.bar(x,x='Annual_Salary_INR',y='Industry',orientation='h',color_discrete_sequence=[TEAL],labels={'Annual_Salary_INR':'Median annual salary (INR)'}); return f
def salary_trend(d):
 x=d.dropna(subset=['Annual_Salary_INR']).groupby('Year',as_index=False).Annual_Salary_INR.median()
 return px.line(x,x='Year',y='Annual_Salary_INR',markers=True,labels={'Annual_Salary_INR':'Median annual salary (INR)'})
