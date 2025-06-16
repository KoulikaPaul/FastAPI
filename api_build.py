from fastapi import FastAPI
from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pandas as pd 
import json
import pickle

with open('KNN_model.pkl','rb') as f:
   KNN_model=pickle.load(f)


app_diabetic= FastAPI()
class Patient_Diabetic(BaseModel):
    Pregnancies: Annotated[int, Field(...,description="No.of children")]
    Glucose: Annotated[int, Field(...,description="Glucose level")]
    BloodPressure: Annotated[int,Field(...,description="BP",gt=50,lt=200)]
    SkinThickness: Annotated[int, Field(...,description="Thickness of skin")]
    Insulin :  Annotated[int, Field(...,description="Insulin level",gt=0)]
    BMI:  Annotated[float, Field(...,description="bmi",gt=0,lt=100)]
    DiabetesPedigreeFunction : Annotated[float, Field(...,description="Diabetic func",gt=0,lt=3)]
    Age : Annotated[int, Field(...,description="Age",gt=0)]
    


@app_diabetic.post('/diabetes_info')
def diabetes_info(New_patient:Patient_Diabetic):
  input_patient= pd.DataFrame({'Pregnancies':New_patient.Pregnancies,'Glucose': New_patient.Glucose,'BloodPressure': New_patient.BloodPressure,'SkinThickness':New_patient.SkinThickness,'Insulin':New_patient.Insulin,'BMI':New_patient.BMI,'DiabetesPedigreeFunction':New_patient.DiabetesPedigreeFunction,'Age':New_patient.Age},index=[0])
  prediction_new = KNN_model.predict1(input_patient)[0]
  print(prediction_new)
  prediction_new=json.dumps(int(prediction_new))
  return JSONResponse(status_code=200,content={'Patient_pred':prediction_new})