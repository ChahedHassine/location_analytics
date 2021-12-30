import streamlit as st
import folium
from streamlit_folium import folium_static
#from bs4 import BeautifulSoup
#import requests
import pickle
import numpy as np
import datetime
st.title("NYC crimes created by hassine and wassim")

def getCoords(coords):  
    for i in range(len(coords)):
        if(coords[i] == '['):
            start = i 
        if(coords[i] == ']'):
            end = i+1
            break 

    coords = coords[start+1 : end-1]
    pair = coords.split(",")
    x = float(pair[0])
    y = float(pair[1])        
    return x , y 
def getAgeGroup(age):
    try : 
        age = int(age)
        if(age>64):
            return 5
        if(age<18):
            return 2
        if(age>19 and age<25):
            return 3
        if(age>24 and age<45):
            return 0
        if(age>44 and age<65):
            return 1

    except : 
        return 4  
def getSex(sexe):
    d = 0 
    m = 0 
    f = 0
    e = 0
    if(sexe=='Company'):
        d=1
    if(sexe=='Female'):
        f=1
    if(sexe=='Male'):
        m=1
    return d,m,f,e
def getRaces(race):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    if(race=='AMERICAN INDIAN/ALASKAN NATIVE'):
        a = 1
    if(race=='ASIAN / PACIFIC ISLANDER'):
        b = 1
    if(race=='BLACK'):
        c = 1
    if(race=='BLACK HISPANIC'):
        d = 1
    if(race=='UNKNOWN'):
        e = 1
    if(race=='WHITE'):
        f = 1
    if(race=='WHITE HISPANIC'):
        g = 1
    return a , b, c , d, e , f , g
def getTime(time):
    time = str(time)
    tmp = time.split(':')[0]
    if int(tmp)>6 and int(tmp)<=12:
        return 1
    elif int(tmp)>12 and int(tmp)<=17 :
        return 0
    elif int(tmp)<20:
        return 2
    else : 
        return 3
name = st.sidebar.text_input("Put your name")
gender = st.sidebar.selectbox("select your gender", ("Male", "Female","Company"))
race = st.sidebar.selectbox("select your gender", ("AMERICAN INDIAN/ALASKAN NATIVE","ASIAN / PACIFIC ISLANDER,BLACK","BLACK HISPANIC","WHITE","WHITE HISPANIC","UNKNOWN"))
age = st.sidebar.text_input("Put your age")
trip_time = st.sidebar.date_input(" Select the date")
time = st.sidebar.time_input('Setect the time')


 
map_geojson = folium.Map(location=[40.654223,-73.911563], zoom_start=10)

# add geojson file to map
folium.GeoJson('NYPD Sectors.geojson', name='NYPD Sectors').add_to(map_geojson)
folium.GeoJson('Police Precincts.geojson', name='Police Precincts').add_to(map_geojson)
folium.GeoJson('NYCHA PSA (Police Service Areas).geojson', name='NYCHA PSA (Police Service Areas)').add_to(map_geojson)
# add layer control to map (allows layer to be turned on or off)
folium.LayerControl().add_to(map_geojson)
popup1 = folium.LatLngPopup()

map_geojson.add_child(popup1)

folium_static(map_geojson)
st.write("""#### Referring to the map""")
lat = st.text_input("Latitude",40.7493)
lon = st.text_input("Longitude",-73.8185)
model = pickle.load(open('location_model.pickle', 'rb'))
age=getAgeGroup(age)
VIC_SEX_D, VIC_SEX_M, VIC_SEX_F, VIC_SEX_E = getSex(gender)
a, b, c, d, e, f, g = getRaces(race)
trip_time = datetime.datetime.strptime(str(trip_time), '%Y-%m-%d')
time=getTime(time)
m=np.array([lat,lon,age,VIC_SEX_D, VIC_SEX_M, VIC_SEX_F, VIC_SEX_E,a,b,c,d,e,f,g,trip_time.month, trip_time.year, trip_time.day,time]).reshape(-1,18)
a=model.predict(m)
st.write('#### Probabily of crime is ',str(round(a[0],4)*10),'%')