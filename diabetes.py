import urllib.request
import json
import os
import ssl
import streamlit as st


#------------------------------------(3) APPLICATION MAIN INTERFACE/////// 
st.write("""
# MSDE4 : Diabetes prediction  
presented by EL HAMDI ALAOUI
""")
st.sidebar.header('Please Insert the fields below :')

#---------------------------------------START-----------------------------------------------

#(2) global variables for the interface

Pregnancies = st.sidebar.slider('Pregnancies',min_value=0,max_value=40,format='%d',step=1)
Glucose = st.sidebar.slider('Glucose',min_value=40,max_value=200,format='%d',step=1)
BloodPressure = st.sidebar.slider('BloodPressure',min_value=60,max_value=140,format='%d',step=1)
SkinThickness = st.sidebar.slider('SkinThickness',min_value=20,max_value=60,format='%d',step=1)
Insulin = st.sidebar.slider('Insulin',min_value=0,max_value=1000,format='%d',step=1)
BMI = st.sidebar.slider('BMI',min_value=0.0,max_value=60.0,format='%f',step=0.1)
DiabetesPedigreeFunction = st.sidebar.slider('DiabetesPedigreeFunction',min_value=0.000,max_value=1.000,format='%f',step=0.001)
Age = st.sidebar.slider('Age',min_value=18,max_value=100,format='%d',step=1)



def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

#allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "data": [
    {
      "Age": Age,
      "BMI": BMI,
      "BloodPressure": BloodPressure,
      "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
      "Glucose": Glucose,
      "Insulin": Insulin,
      "Pregnancies": Pregnancies,
      "SkinThickness": SkinThickness
    }
  ],
  "method": "predict"
}

body = str.encode(json.dumps(data))

url = 'http://9d57b920-a11b-48c4-b702-a6120fe7f6cd.uksouth.azurecontainer.io/score'
api_key = '' # Replace this with the API key for the web service

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

if st.sidebar.button('Estimate the Possibility of Diabetes'):
    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        st.write(result)
    except urllib.error.HTTPError as error:
        st.write("The request failed with status code: " + str(error.code))

    # st.write the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        st.write(error.info())
        st.write(error.read().decode("utf8", 'ignore'))
