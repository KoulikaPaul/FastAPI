from fastapi import FastAPI, Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import Annotated, Literal, Optional
def load_data():
   with open('patients.json','r') as file1:
      data1= json.load(file1)
   return(data1)

def save_data(data):
   with open('patients.json','w') as file2:
       json.dump(data,file2)
   
class example_patient(BaseModel):
     id:Annotated[str,Field(...,description="id of patient",example='P001')]
     name:Annotated[str,Field(...,description='name of the patient')]
     city:Annotated[str,Field(...,description='name of the city the patient belongs')]
     age:Annotated[int, Field(...,description='age of patient',gt=0,lt=100)]
     gender:Annotated[Literal['male','female','others'],Field(...,description="gender of the patient")]
     height:Annotated[float,Field(...,description='height of the patient',gt=0)]
     weight:Annotated[float,Field(...,description='height of the patient',gt=0)]
   
     @computed_field
     @property
     def bmi(self)->float:
       bmi= round(self.weight/(self.height**2),2)
       return(bmi)
     
     @computed_field
     @property
     def verdict(self)->str:
        if self.bmi<15:
           return('underweight')
           
        elif(self.bmi<25):
          return('Normal')  
        else: 
         return('Obese')
   

ex_app= FastAPI()
@ex_app.get("/patient")
def hello():
    return({"message: Patient"})

@ex_app.get("/view")
def view():
    data = load_data()
    return(data)

@ex_app.get('/view/{patient_id}')

def view_particular(patient_id:str = Path(...,description='hello hullu mullu',example="P001")):
    data = load_data()
    if patient_id in data:
      return(data[patient_id])
    raise HTTPException(status_code=404, detail='Patient not available')

@ex_app.get("/sort")
def view_sorted(sort_by:str=Query(...,description='sorting column'),order_by:str=Query('asc')):
   sort_cols= ['weight','height','bmi']
   order_cols=['desc','asc']
   if sort_by in sort_cols:
      data= load_data()
      sort_order = True if order_by =='desc' else False
      sorted_data= sorted(data.values(),key= lambda x: x.get(sort_by,0),reverse= sort_order)
      return(sorted_data)
   else:
      raise HTTPException(status_code=400,detail='invalid selection')

@ex_app.post('/info')
def info(patient:example_patient):
   data= load_data()
   if patient.id in data:
      raise HTTPException(status_code=400,detail='already existing patient')
   
   data[patient.id]= patient.model_dump_json(exclude=['id'])# convert the pydantic class to json format
   save_data(data)  # save the new data enter 
   return JSONResponse(status_code= 201,content={'message':'succesful data entry'})


class Patient_edit(BaseModel):
     name:Annotated[Optional[str],Field(default= None)]
     city:Annotated[Optional[str],Field(default= None)]
     age:Annotated[Optional[int], Field(default= None)]
     gender:Annotated[Optional[Literal['male','female','others']],Field(default= None)]
     height:Annotated[Optional[float],Field(default= None)]
     weight:Annotated[Optional[float],Field(default= None)]
   
    
        
@ex_app.put('/update/{patient_id}') 
def updating(patient_id: str, patient_change:Patient_edit):
      
      data= load_data()
      if patient_id not in data:
         raise HTTPException(status_code=404, detail='patient does not exist')
      existing_patient= data[patient_id]
      updated_patient= patient_change.model_dump(exclude_unset= True)
      for key, value in updated_patient.items():
         existing_patient[key]=value
      
      existing_patient['id']=patient_id
      pyd_obj = example_patient(**existing_patient)## dict to pydantic obj for computed fields to the main pydantic class
      fin_updated_patient_dict= pyd_obj.model_dump(exclude='id')## pydantic obj to dict
      data[patient_id]= fin_updated_patient_dict ## replacing the existing data with the updated data

      save_data(data)
      return JSONResponse(status_code=201, content= "updated patient")

@ex_app.delete('/{patient_id}')
def delete_patient(patient_id:str):
   data= load_data()
   if patient_id not in data:
      raise HTTPException(status_code=404, detail="patient doesnot exist")
   
   del data[patient_id]
   save_data(data)
   
   return JSONResponse(status_code=201, content='Patient deleted')
      

