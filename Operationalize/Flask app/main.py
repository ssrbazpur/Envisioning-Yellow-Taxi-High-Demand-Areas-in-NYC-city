############################################################
#                                                          # 
#   ENVISIONING YELLOW TAXI CAB DEMAND IN NYC CITY         #
#       SUBMITTED BY : SIMRANJEET RANDHAWA                 #
#                                                          #
#                                                          #
############################################################





############################################################
#                                                          # 
#                IMPORTING HEADER FILES                    #    
#                                                          #
############################################################


from flask import flash,Flask,render_template,request,url_for
from flask import jsonify
from bs4 import BeautifulSoup as bs
import requests
from google.cloud import bigquery
import pandas as pd
import numpy as np
import lightgbm as lgb
import pickle
import json
import datetime, pytz
import pandas_gbq as gbq
from datetime import datetime
import datetime
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta
import lightgbm as lgb
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


############################################################
#                                                          # 
#       CALLING FLASK APPLICATION                          #    
#                                                          #
############################################################

app = Flask(__name__)

# ___Load Model using Job Lib____

model=joblib.load('final2.pkl')

# __Importing my Google Cloud Credentials____

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="nyc-taxi-265120-baf9a3e4cf9b.json"
project_id = 'nyc-taxi-265120'
client = bigquery.Client(project = project_id)



# __Scrapping Weather Data from Google__
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"


############################################################
#                                                          # 
#       LIVE WEATHER SCRAPPER FROM GOOGLE URL              #    
#                                                          #
############################################################

# url : The parameter that consist the url of Google Weather Feed
def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a soup
    soup = bs(html.text, "html.parser")
    # store all results on this dictionary
    result = {}
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
    # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        day_name = day.find("div", attrs={"class": "vk_lgy"}).attrs['aria-label']
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        max_temp = min(int(temp[1].text),int(temp[0].text))
        min_temp = min(int(temp[3].text),int(temp[2].text))
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    result['next_days'] = next_days
    return result

############################################################
#                                                          # 
#                CONVERT DATE TO NTH DAY                   #    
#                                                          #
############################################################

def date_to_nth_day(date, format='%Y-%m-%d'):
    date = pd.to_datetime(date, format=format)
    new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1

############################################################
#                                                          # 
#             CREATING ROUTES IN FLASK APP                 #    
#                                                          #
############################################################
    


# _____Route / renders index.html in template folder______

@app.route("/")
def index():
	return render_template("index.html")

# _____predict Route renders result.html if no error______
    
@app.route('/predict',methods=['POST'])
def predict():
    region="New York"
    URL="https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    URL += region
    ###########  Getting live weather feed ####################
    data = get_weather_data(URL)    
    for dayweather in data["next_days"]:
        print("="*40, dayweather["name"], "="*40)
        print("Description:", dayweather["weather"])	
    ###########  Getting index.html Form data ####################
    int_features = [x for x in request.form.values()]
    date=int_features[0]
    output = int_features[1]
    input1=int_features[2]
    df=pd.read_csv("temp.csv")
    tempdate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
    nthday=date_to_nth_day(tempdate)
    print("The nthday is as",nthday)
    enterdatemintemp=df.loc[df['Day '] == nthday]['Min '].iloc[0]
    enterdatemaxtemp=df.loc[df['Day '] == nthday]['Max'].iloc[0]
    query="""SELECT * FROM `bigquery-public-data.new_york_taxi_trips.taxi_zone_geom` WHERE ST_CONTAINS(zone_geom, ST_GEOGPOINT({1}, {0}))""".format(output,input1)
    df = client.query(query).to_dataframe()
    ###########  TRY CATCH BLOCK ####################
    try:
        ######### Getting Information about the Zone ##########
        a=df.iloc[0]['zone_name']
        b=df.iloc[0]['borough']
        print(df.head())
        first=df.iloc[0]['zone_id']
        print(date) 
        my_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
        time=data["dayhour"]
        temp=data['temp_now']
        noting = 0
        for dayweather in data["next_days"]:
            print("="*40, dayweather["name"], "="*40)
            print("Description:", dayweather["weather"])
            if dayweather["name"][0]=='r':
                noting=1
        ########## Getting the data into appropriate format #########
        fourth=my_date.weekday()
        third=my_date.hour
        period=third+1
        second=my_date.timetuple().tm_yday
        daynumbervalue=int(second)
        print("The daynumber is as",daynumbervalue)
        todaydate=datetime.datetime.today()
        todayday=int(todaydate.timetuple().tm_yday)
        print("Today date is as",todayday)
        for i in range(0,7):
            if i+todayday== daynumbervalue:
                print("Value of I IS",i)
                enterdatemintemp=data["next_days"][i]['min_temp']
                enterdatemaxtemp=data["next_days"][i]['max_temp']
        six=data["next_days"][0]['max_temp']
        five=data["next_days"][0]['min_temp']
        ###########  Predicting the result using the model ####################
        ans=model.predict([[first,second,third,fourth,five,six,noting]])
    
        ans=int(ans)
        return render_template('results.html',entermin=enterdatemintemp,entermax=enterdatemaxtemp,da1=my_date,lat=output,long=input1,time1=third,temp=temp,time=time,boro=b,ZoneName=a,zoneid=first,trips=ans, prediction_text='Zone is {0} and Number of trips will be  {1}'.format(a,ans),mtemp1=data["next_days"][0]['min_temp'],temp1=data["next_days"][0]['max_temp'],mtemp2=data["next_days"][1]['min_temp'],temp2=data["next_days"][1]['max_temp'],temp3=data["next_days"][2]['max_temp'],temp4=data["next_days"][3]['max_temp'],temp5=data["next_days"][4]['max_temp'],temp6=data["next_days"][5]['max_temp'],temp7=data["next_days"][6]['max_temp'],mtemp3=data["next_days"][2]['min_temp'],mtemp4=data["next_days"][3]['min_temp'],mtemp5=data["next_days"][4]['min_temp'],mtemp6=data["next_days"][5]['min_temp'],mtemp7=data["next_days"][6]['min_temp'])
    except:
        return render_template('error.html')


# _____weekpred Route to render index1.html______

@app.route('/weekpred')
def weekpred():
    
    return render_template('index1.html')

# ___go12 Route (for Weekly Prediction) and rendering index.html____

@app.route('/go12')
def go12():
    '''
    For rendering results on HTML GUI
    '''
    first=[]
    for i in range(0,264):
        first.append(i)
    nyc_datetime = datetime.datetime.now(pytz.timezone('US/Eastern'))
    nyc_datetime.timetuple()
    actualdate=[]
    b=nyc_datetime.now().date().strftime('%Y-%m-%d')
    for i in range(0,7):
        d=(nyc_datetime.now().date()+timedelta(days=i)).strftime('%Y-%m-%d')
        actualdate.append(d)
    second1=nyc_datetime.timetuple().tm_yday
    second=[]
    for i in range(second1,second1+7):
        second.append(i)
    third1=nyc_datetime.today().hour
    third=[]
    for i in range(third1,third1+24):
        third.append(i%24)
    four=[]
    fourth=nyc_datetime.today().weekday()
    for i in range(fourth,fourth+7):
        four.append(i%7)
    l2=first*7*24
    a1=actualdate*263*24
    l3=second*263*24
    l4=third*263*7
    l5=four*263*24
    
    ####### Creation of Dataframe ############
    df = pd.DataFrame(list(zip(l2, a1,l3,l4,l5)), 
               columns =['Zone', 'ActualDate','DayNumber','Hour','DayofwEEK']) 
    region="New York"
    URL="https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    URL += region
    # get data
    data = get_weather_data(URL)
    b1=data['dayhour']
    max1=[]
    min1=[]
    a=b1.split(" ", 1)
    b1=a[0]
    if b1=='Saturday':
          week=6
    elif b1=='Friday':
          week=5
    elif b1=='Thursday':
          week=4
    elif b1=='Wednesday':
          week=3
    elif b1=='Tuesday':
          week=2
    elif b1=='Monday':
          week=1
    else:
          week=0
    for dayweather in data["next_days"]:
        
        min1.append(dayweather['min_temp'])
        max1.append(dayweather['max_temp'])
    result1=[]
    result2=[]
    ########### Making Dataframe for the next week ###########
    for value in df["DayofwEEK"]: 
      
        if value == (week %7): 
            result1.append(min1[0]) 
            result2.append(max1[0]) 
        elif value == (week+1) %7 : 
            result1.append(min1[1]) 
            result2.append(max1[1])  
        elif value == (week+2) %7 : 
            result1.append(min1[2]) 
            result2.append(max1[2]) 
        elif value == (week+3) %7 : 
            result1.append(min1[3]) 
            result2.append(max1[3]) 
        elif value == (week+4) %7 : 
            result1.append(min1[4]) 
            result2.append(max1[4])
        elif value == (week+5) %7 : 
            result1.append(min1[5]) 
            result2.append(max1[5]) 
        elif value == (week+6) %7 : 
            result1.append(min1[6]) 
            result2.append(max1[6])  
        else: 
            result2.append("Fail") 
    result1=[float(i) for i in result1]
    result2=[float(i) for i in result2]
    df["min"] = result1
    df["max"]=result2
    rain=[]
    for i in range(0,44184):
        rain.append(0)
    
    for dayweather in data["next_days"]:
        if "rain" in dayweather["weather"]:
            rain=1
    df["rain"]=rain
    print(df.head())
    ans=model.predict(df[['Zone', 'DayNumber','Hour','DayofwEEK','min','max','rain']] )
    df['ans']=ans
    df.loc[df['ans'] < 0, 'ans'] = 0
    df["ans"] = df["ans"].astype(int)
    gbq.to_gbq(df, 'hello.test_table1', 'nyc-taxi-265120', if_exists='replace')
    return render_template('index1.html')


############################################################
#                                                          # 
#                   MAIN FUNCTION                          #    
#                                                          #
############################################################
    
if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)
    
    
    
############################################################
#                                                          # 
#                THANK YOU FOR VIEWING                     #    
#                                                          #
############################################################    
    
    

