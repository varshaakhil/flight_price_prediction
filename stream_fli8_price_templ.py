

from pycaret.regression import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import datetime
model = load_model('final_model')






def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():
    from PIL import Image
    image = Image.open('top.jpg')
    image_office = Image.open('side.jpg')
    st.image(image,use_column_width=True)
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))
    st.sidebar.info('This app is created to predict flight ticket price')
    st.sidebar.success('https://www.ipsr.edu.in')
    st.sidebar.image(image_office,use_column_width=True)
    st.title("Predicting flight ticket price")
    
    
    if add_selectbox == 'Online':
        Airline=st.selectbox('Airline: The name of the airline', ['Jet Airways','IndiGo','Air India','Multiple carriers','SpiceJet','Vistara','Air Asia','GoAir','Multiple carriers Premium economy','Jet Airways Business','Vistara Premium economy','Trujet'])
        Source=st.selectbox('Source: The source from which the service begins', ['Delhi','Kolkata','Banglore','Mumbai','Chennai'])
        Destination=st.selectbox(' Destination: The destination where the service ends', ['Delhi','Banglore','Delhi','New Delhi','Hyderabad'])
        Total_Stops = st.selectbox('Total_Stops: Total stops between the source and destination', ['1 stop', '2 stops','3 stops','4 stops','non-stop'])
        
        Journey_date = st.date_input("Date of journey",datetime.datetime.now())
        Journey_day=int(pd.to_datetime(Journey_date, format="%Y/%m/%d").day)
        Journey_month=int(pd.to_datetime(Journey_date, format = "%Y/%m/%d").month)
        Week_day=pd.to_datetime(Journey_date, format = "%Y/%m/%d").day_name()

        Dep_Time = st.time_input("Departure Time",datetime.time())
        str1=str(Dep_Time)
        list1=str1.split(':')
        Dep_hour=int(list1[0])
        Dep_min=int(list1[1])
     

        Arrival_Time=st.time_input("Arrival Time",datetime.time())
        str2=str(Arrival_Time)
        list2=str2.split(':')
        Arrival_hour=int(list2[0])
        Arrival_min=int(list2[1])


        Duration=abs((Arrival_hour*60 +Arrival_min*1)-(Dep_hour*60+Dep_min*1))

        output=""
        input_dict={'Airline':Airline,'Source':Source,'Destination':Destination,'Total_Stops':Total_Stops,'Journey_day':Journey_day ,'Journey_month':Journey_month,'Week_day' : Week_day,'Dep_hour':Dep_hour,'Dep_min' :Dep_min,'Arrival_hour' : Arrival_hour,'Arrival_min':Arrival_min,'Duration':Duration}
        input_df = pd.DataFrame([input_dict])
        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = str(output)
        st.success('The output is {}'.format(output))

        
    if add_selectbox == 'Batch':
        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)
def main():
    run()

if __name__ == "__main__":
  main()
