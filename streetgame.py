

import streamlit as st
import pandas as pd
import requests
import json

import folium # pip install folium
from folium import plugins
# import ipywidgets
# import geocoder # pip install geocoder
# import geopy # pip install geopy
import geopy.distance
import numpy as np

from streamlit_folium import st_folium


# Este es mi script

st.set_page_config(page_title='StretGame', layout='wide', page_icon=':map:')

# menu = st.sidebar.selectbox(
#     "Seleccione una opción del menu",
#     ('Home', 'Datos', 'Filtros')
# )
# # map

col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.write(' ')


    

with col3:
    st.write(' ')
    

@st.cache_resource(experimental_allow_widgets=True) 
def generate_map_1():
    map_lat_long = folium.Map(location=[53.48, -2.24], zoom_start=14)
    jugar = False
    # add latitude and longitude tool to map
    map_lat_long.add_child(folium.LatLngPopup())
    with st.expander("Map", expanded=True):
    # display map
        
        st_data = st_folium(map_lat_long, width=900, height=500)
        try:
            # st.write("Latitude:", st_data["last_clicked"]["lat"])
            st.write("Longitude:", st_data["last_clicked"]["lng"])
            st.write("Latitude", st_data["last_clicked"]["lat"])
        except:
            st_data = {"last_clicked": {"lat": None, "lng":None}}
    try:
        
        
        try:
            lat = st_data["last_clicked"]["lat"]
            lng = st_data["last_clicked"]["lng"]
            r = requests.get(f"https://api.openstreetcam.org/2.0/photo/?lat={lat}&lng={lng}&radius=50")
            images = [x["fileurlProc"] for x in json.loads(r.text)["result"]["data"]]
            url_pic = None
            for imagen in images:
                r = requests.get(imagen)
                if r.ok:
                    url_pic = imagen
                    break




            st.image(url_pic,
                width=900)
            jugar = True
            
        except:
            st.write(" No pics found!")
        
        
    except:
        pass
    return jugar, st_data["last_clicked"]["lat"], st_data["last_clicked"]["lng"]


@st.cache_resource(experimental_allow_widgets=True) 
def generate_map_2(jugar):
    checking = False
    st_data2 = {"last_clicked": {"lat": None, "lng":None}}
    if jugar:
        map_lat_long2 = folium.Map(location=[53.48, -2.24], zoom_start=14)
        map_lat_long2.add_child(folium.LatLngPopup())
        
        with st.expander("Click to play", expanded=False):
        # display map
            st.subheader("Click in the location of the picture above: ")
            st_data2 = st_folium(map_lat_long2, width=900, height=500, key="hjsksjh")
            try: 
                st.write("Selected Longitude:", st_data2["last_clicked"]["lng"])
                st.write("Selected Latitude", st_data2["last_clicked"]["lat"])
                checking = True
            except:
                st_data2 = {"last_clicked": {"lat": None, "lng":None}}
    return checking, st_data2["last_clicked"]["lat"], st_data2["last_clicked"]["lng"]


@st.cache_resource(experimental_allow_widgets=True) 
def generate_map_3(checking, init_lat, init_lng, end_lat, end_lng):

    if checking:

        # st.write(init)
        # st.write(end)
        st.subheader(f"Distancia en kMs: {round(geopy.distance.geodesic([init_lat, init_lng], [end_lat, end_lng]).km, 2)}!")
        map_lat_long3 = folium.Map(location=[init_lat, init_lng], zoom_start=13)
        
        plugins.AntPath([[end_lat, end_lng], [init_lat, init_lng]]).add_to(map_lat_long3)
        folium.Marker(location=[init_lat, init_lng], 
                  popup="Init",
                  icon=folium.Icon(color="green", icon="flag", prefix='fa')).add_to(map_lat_long3)
        folium.Marker(location=[end_lat, end_lng], 
                  popup="End",
                  icon=folium.Icon(color="red", icon="remove", prefix='fa')).add_to(map_lat_long3)
        
        st_folium(map_lat_long3, width=900, height=500, key="lol")
with col2:
    jugar, init_lat, init_lng = generate_map_1()
    checking, end_lat, end_lng = generate_map_2(jugar)
    generate_map_3(checking, init_lat, init_lng, end_lat, end_lng)   



    
