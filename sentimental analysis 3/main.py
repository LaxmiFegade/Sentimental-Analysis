import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Sentiment Analysis",page_icon="https://p.kindpng.com/picc/s/207-2071107_satisfied-customer-png-download-happy-customer-icon-png.png")
st.markdown("<h1 style='text-align: center;'>SENTIMENTAL ANALYSIS</h1>", unsafe_allow_html=True)
st.sidebar.image("https://telehub.vn/wp-content/uploads/2021/08/Sentiment-Analysis-trong-Contact-center3.jpeg")
choice=st.sidebar.selectbox("My Menu",("Home","Analyze Sentiment","Visualize the Results","CSV File"))
if(choice=="Home"):
    st.image("https://user-images.githubusercontent.com/57702598/90991088-264c8880-e56c-11ea-9895-90029d3c2139.gif")
    st.markdown("<h1 style='text-align: center';>Welcome</h1>",unsafe_allow_html=True)
elif(choice=="Analyze Sentiment"):
    st.image("https://www.touchpoint.com/wp-content/uploads/2023/11/Sentiment-analysis.png")
    url=st.text_input("Enter Google Sheet URL")
    r=st.text_input("Enter Range")
    c=st.text_input("Enter Column")
    btn=st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('C:/project/Scripts/key.json.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state ['cred']=f.run_local_server(port=0)
            mymodel=SentimentIntensityAnalyzer()
            service=build('Sheets','v4',credentials=st.session_state ['cred']).spreadsheets().values()
            d=service.get(spreadsheetId=url,range=r).execute()
            mycolumns=d['values'][0]
            mydata=d['values'][1:]
            df=pd.DataFrame(data=mydata,columns=mycolumns)
            l=[]
            for i in range(0,len(df)):
                k=df._get_value(i,c)
                pred=mymodel.polarity_scores(k)
                if(pred['compound']>0.5):
                    l.append("Postive")
                elif(pred['compound']<-0.5):
                    l.append("Negative")
                else:
                    l.append("Neutral")
            df['Sentiment']=l
            st.dataframe(df)
            df.to_csv("Review.csv",index=False)
            st.header("This data has been saved by the name of Review.csv")
elif(choice=="Visualize the Results"):
    st.image("https://monkeylearn.com/static/c9fdd85eb695ace6bbe59bee47845158/12fd3/normal.png")
    choice2=st.selectbox("Choose Visualization",("None","Pie","Histogram"))
    if(choice2=="Pie"):
        df=pd.read_csv("Review.csv")
        posper=(len(df[df['Sentiment']=='Positive'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        neupar=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        fig=px.pie(values=[posper,negper,neupar],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)
    elif(choice2=="Histogram"):
        t=st.text_input("Choose any Categorical Column")
        if t:
            df=pd.read_csv("Review.csv")
            fig=px.histogram(x=df['Sentiment'],color=df[t])
            st.plotly_chart(fig)
elif(choice=="CSV File"):
    st.image("https://static.vecteezy.com/system/resources/thumbnails/011/943/654/small_2x/download-csv-icon-file-with-label-on-laptop-screen-downloading-document-concept-vector.jpg")
    path=st.file_uploader("Upload File")
    c=st.text_input("Enter Column")
    btn=st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('C:/project/Scripts/key.json.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state ['cred']=f.run_local_server(port=0)
            mymodel=SentimentIntensityAnalyzer()
            df=pd.read_csv(path)
            l=[]
            for i in range(0,len(df)):
                k=df._get_value(i,c)
                pred=mymodel.polarity_scores(k)
                if(pred['compound']>0.5):
                    l.append("Postive")
                elif(pred['compound']<-0.5):
                    l.append("Negative")
                else:
                    l.append("Neutral")
            df['Sentiment']=l
            st.dataframe(df)
            df.to_csv("Review.csv",index=False)
            st.header("This data has been saved by the name of Review.csv")
    
