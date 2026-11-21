from pathlib import Path
import joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor,HistGradientBoostingClassifier,HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,mean_absolute_error,mean_squared_error,r2_score
ROOT=Path(__file__).resolve().parents[1]; MODEL_DIR=ROOT/'models'; MODEL_DIR.mkdir(exist_ok=True)
CAT=['Education','Industry','Job_Role','Location','Employment_Type','Work_Mode']; NUM=['Experience_Years','Skill_Count','Skill_Score_0_100','Certifications_Count']
def prep():
    return ColumnTransformer(
        transformers=[
            (
                'cat',
                Pipeline(steps=[
                    ('impute', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
                ]),
                CAT
            ),
            (
                'num',
                Pipeline(steps=[
                    ('impute', SimpleImputer(strategy='median')),
                    ('scale', StandardScaler())
                ]),
                NUM
            )
        ]
    )
def feats(d): return d[CAT+NUM].copy()
def train_models(d):
 out={'employment':[],'salary':[]}; X=feats(d); y=(d.Employment_Status=='Employed').astype(int); a,b,c,e=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
 clfs={'Logistic Regression':LogisticRegression(max_iter=1500,class_weight='balanced'),'Random Forest':RandomForestClassifier(n_estimators=220,min_samples_leaf=3,class_weight='balanced',random_state=42),'Hist Gradient Boosting':HistGradientBoostingClassifier(max_iter=120,random_state=42)}; best=None; score=-1
 for name,model in clfs.items():
  p=Pipeline([('prep',prep()),('model',model)]); p.fit(a,c); pred=p.predict(b); prob=p.predict_proba(b)[:,1] if hasattr(p,'predict_proba') else None
  row={'Model':name,'Accuracy':accuracy_score(e,pred),'Precision':precision_score(e,pred,zero_division=0),'Recall':recall_score(e,pred,zero_division=0),'F1':f1_score(e,pred,zero_division=0),'ROC_AUC':roc_auc_score(e,prob) if prob is not None else None}; out['employment'].append(row)
  if row['F1']>score:best,score=p,row['F1']
 joblib.dump(best,MODEL_DIR/'employment_model.pkl')
 imp=permutation_importance(best,b,e,n_repeats=5,random_state=42,scoring='f1')
 out['employment_importance']=[{'Feature':f,'Importance':float(v)} for f,v in sorted(zip(X.columns,imp.importances_mean),key=lambda z:z[1],reverse=True)]
 s=d.dropna(subset=['Annual_Salary_INR']); X=feats(s); y=s.Annual_Salary_INR; a,b,c,e=train_test_split(X,y,test_size=.2,random_state=42)
 regs={'Ridge Regression':Ridge(alpha=2),'Random Forest':RandomForestRegressor(n_estimators=240,min_samples_leaf=3,random_state=42,n_jobs=-1),'Hist Gradient Boosting':HistGradientBoostingRegressor(max_iter=140,random_state=42)}; best=None; score=float('inf')
 for name,model in regs.items():
  p=Pipeline([('prep',prep()),('model',model)]); p.fit(a,c); pred=p.predict(b); mae=mean_absolute_error(e,pred); out['salary'].append({'Model':name,'MAE':mae,'RMSE':mean_squared_error(e,pred)**.5,'R2':r2_score(e,pred)})
  if mae<score:best,score=p,mae
 joblib.dump(best,MODEL_DIR/'salary_model.pkl')
 imp=permutation_importance(best,b,e,n_repeats=5,random_state=42,scoring='neg_mean_absolute_error')
 out['salary_importance']=[{'Feature':f,'Importance':float(v)} for f,v in sorted(zip(X.columns,imp.importances_mean),key=lambda z:z[1],reverse=True)]
 return out
def load_model(name):
 p=MODEL_DIR/name; return joblib.load(p) if p.exists() else None
