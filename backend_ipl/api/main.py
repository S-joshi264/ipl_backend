from fastapi import FastAPI, Request, HTTPException, Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import joblib

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "model_pipe.pkl"))
ss = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Features(BaseModel):
    features:list
def pred(feature):
    prediction=model.predict(feature)
    return prediction.tolist()
@app.get("/")   
def home():
    return {"message":"Hello World"}

@app.post("/predict")
def Prediction(data:Features):
    print(type(data))
    try:
        df = pd.DataFrame(dict(data).values(),columns=['strike_rate', 'boundary_Percent', 'Dot_Percent', 'Runs', 'POM',
       'is_capped_international', 'base_price_lakh',
       'playing_role_All-Rounder', 'playing_role_Batsman',
       'playing_role_Bowler', 'playing_role_Wicketkeeper-Batsman'])
        print(df)
        df_scaled = ss.transform(df)
        print(df_scaled)

        return {"Prediction":pred(df_scaled)}
    except Exception as e:
        raise HTTPException (status_code=404,detail=str(e))


