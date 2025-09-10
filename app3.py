import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import streamlit as st
import requests
from io import StringIO
import os


def load_data(filename="bank.csv", file_url="https://drive.google.com/file/d/1cndLIuK994yU6ba-zXsj35KGjtGjyk5f/view?usp=sharing"):
    possible_paths = [
        filename,
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join("/data", filename)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    
    if file_url is not None:
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text))
        except:
            pass
    
    raise FileNotFoundError(f"Fichier {filename} non trouvé")

data = load_data("bank.csv")


st.set_page_config(page_title="Real time Analysis Dashboard",page_icon="✅",layout="wide")


st.title("Real Dashboard")

job_filter = st.selectbox("select a job",pd.unique(data.job))
data = data[data["job"]== job_filter]

avg_age = np.mean(data["age"])


count_married = int(data[(data['marital']=='married')]['marital'].count())


balance = np.mean(data["balance"])

c,o,l = st.columns(3)
c.metric(label="Age🧔",value=round(avg_age),delta=round(avg_age))
o.metric(label="Married Count💍",value=int(count_married),delta=round(count_married))
l.metric(label="Balance ⚖",value= f" ${round(balance,2)}",delta=round(balance/count_married)*100)


col1,col2 = st.columns(2)
with col1:
    fig1=plt.figure(figsize=(9,8))
    sns.barplot(data=data,y="age",x="marital",palette="pastel")
    st.pyplot(fig1)
with col2:
    fig2=plt.figure(figsize=(9,8))
    sns.histplot(data=data,x="age",palette="Oranges")
    st.pyplot(fig2)





