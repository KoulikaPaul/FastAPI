import streamlit as st
import requests

API_URL='http://127.0.0.1:8000/diabetes_info'

st.title("Diabetic Patients")

P = st.number_input("Enter number of kids")
G =st.number_input("Enter glucose level")
B= st.number_input("Enter BP")
S= st.number_input("Enter skin thickness")
I= st.number_input("Enter insulin level")
BMI= st.number_input("Enter BMI")
D=st.number_input("Enter Diabteic level")
age=st.number_input("Enter Age")

if st.button("Predict Diabetes"):
  input_data={
               'Pregnancies':P,
               'Glucose': G,
               'BloodPressure': B,
               'SkinThickness':S,
               'Insulin':I,
               'BMI':BMI,
               'DiabetesPedigreeFunction':D,
               'Age':age
               } 
  try:
    print("Hello")
    response= requests.post(API_URL,json=input_data)
    print(response)
    if response.status_code==200:
      result= response.json()
      st.success(f"Predicted Result: **{result['Patient_pred']}**")
    else:
      st.error(f"API Error")
  except requests.exceptions.ConnectionError:
    st.error("Could Not Connect")    