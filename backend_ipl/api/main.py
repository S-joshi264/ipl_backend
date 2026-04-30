from fastapi import FastAPI, Request, HTTPException, Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from logtail import LogtailHandler
import pandas as pd
import os
import joblib
from datetime import datetime
app=FastAPI()
LOG_TOKEN="7Q6jyhbjjEvMzBLN1MAFUxqg"
BASE_DIR = os.path.dirname(__file__)
LOG_DIR=os.getcwd()
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = LogtailHandler(
    source_token=os.getenv(LOG_TOKEN)
)

logger.addHandler(handler)
# def log_pred(input_data,prediction):
#     os.makedirs(os.path.join(LOG_DIR,"logs") ,exist_ok=True)

#     log_path=os.path.join(LOG_DIR,"logs","pred_logs.csv")
#     log_data=pd.DataFrame([{
#         "Time Stamp":datetime.now(),
#         "input_data":input_data,
#         "prediction":prediction

#     }])
    # if(os.path.exists(log_path)):
    #     log_data.to_csv(log_path,header=False,index=False,mode="a")
    # else:
    #     log_data.to_csv(log_path,index=False)

model = joblib.load(os.path.join(BASE_DIR, "model_pipe.pkl"))
ss = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

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
        logger.info({
            "event": "prediction",
            "input": data,
            "prediction": pred(df_scaled)
        })
        return {"Prediction":pred(df_scaled)}
    except Exception as e:
        raise HTTPException (status_code=404,detail=str(e))


