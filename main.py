from calendar import c
import pandas as pd
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import time
import os

update_time = 0.5

# Increase web page width
# st.set_page_config(layout="wide")

image = Image.open('LIP_B.png')
st.image(image, width=500, use_column_width=False)


st.markdown("# Atmospheric Balloon Tracker") 

option = st.selectbox(
    'Choose dataset',
    ('Dataset 1', 'Dataset 2'))

if option == 'Dataset 1':
    file_to_load = "dataset1.csv"
elif option == 'Dataset 2':
    file_to_load = "dataset2.csv"


sensor_columns = ['Internal Temperature', 'External Temperature', 'Pressure', 'Voltage', 'RSSI',  'Altitude', 'Distance', 'Power', 'Received', 'Lost']
radiation_columns = ['Counts per Minute']
location_columns = ['Latitude', 'Longitude']

class FileReference:
    def __init__(self, filename):
        self.filename = filename

def hash_file_reference(file_reference):
    filename = file_reference.filename
    return (filename, os.path.getmtime(filename))


#@st.cache(suppress_st_warning=False, hash_funcs={FileReference: hash_file_reference})
def get_csv(file_to_load):
    df = pd.read_csv(file_to_load, index_col=0, sep=';')

    df.rename(columns={'cpm': 'Counts per Minute', 
                        'int_temperature': 'Internal Temperature',
                        'ext_temperature': 'External Temperature',
                        'pressure': 'Pressure',
                        'voltage': 'Voltage',
                        'rssi': 'RSSI',
                        'altitude': 'Altitude',
                        'distance': 'Distance',
                        'Power': 'Power',
                        '#Received': 'Received',
                        '#Lost': 'Lost',
                        'latitude': 'Latitude',
                        'longitude': 'Longitude',
                        'time': 'Time'}, inplace=True)

    ###############################################
    ##### Data preparation
    ###############################################


    df = df.infer_objects()

    # Ignore some cases
    #df = df[df['latitude'] != 0]
    #df = df[df['longitude'] != 0]
    #df = df[df['time'] != 0]

    df.reset_index(drop=True, inplace=True)


    # Time column is the current second of the day, convert to HH:MM:SS
    df['Time'] = df['Time'].apply(lambda x: datetime.timedelta(seconds=x))

    return df



option = st.selectbox(
    'Choose window',
    ('General Stats', 'Radiation', 'Location', 'Other'))

if option == 'General Stats':
    st.title('General Stats')    

    columns1 = st.empty()
    columns2 = st.empty()

    graph_placeholders = [(st.empty(), st.empty()) for _ in sensor_columns]


    while True:
        with columns1:
            col1, col2, col3, col4, col5 = st.columns(5)
        with columns2:
            col6, col7, col8, col9, col10 = st.columns(5)
        df = get_csv(file_to_load)

        col1.metric(label="Internal Temperature", value=f"{df['Internal Temperature'].iloc[-1]} °C", delta=f"{df['Internal Temperature'].iloc[-1]-df['Internal Temperature'].iloc[-2]} °C")
        col2.metric(label="External Temperature", value=f"{df['External Temperature'].iloc[-1]} °C", delta=f"{df['External Temperature'].iloc[-1]-df['External Temperature'].iloc[-2]} °C")
        col3.metric(label="Pressure", value=f"{df['Pressure'].iloc[-1]} hPa", delta=f"{df['Pressure'].iloc[-1]-df['Pressure'].iloc[-2]} hPa")
        col4.metric(label="Voltage", value=f"{df['Voltage'].iloc[-1]} V", delta=f"{df['Voltage'].iloc[-1]-df['Voltage'].iloc[-2]} V")
        col5.metric(label="RSSI", value=f"{df['RSSI'].iloc[-1]} dBm", delta=f"{df['RSSI'].iloc[-1]-df['RSSI'].iloc[-2]} dBm")

        col6.metric(label="Altitude", value=f"{df['Altitude'].iloc[-1]} meters", delta=f"{df['Altitude'].iloc[-1]-df['Altitude'].iloc[-2]} meters")
        col7.metric(label="Distance", value=f"{df['Distance'].iloc[-1]} meters", delta=f"{df['Distance'].iloc[-1]-df['Distance'].iloc[-2]} meters")
        col8.metric(label="Power", value=f"{df['Power'].iloc[-1]} mW", delta=f"{df['Power'].iloc[-1]-df['Power'].iloc[-2]} mW")
        col9.metric(label="Received", value=f"{df['Received'].iloc[-1]} packets", delta=f"{df['Received'].iloc[-1]-df['Received'].iloc[-2]} packets")
        col10.metric(label="Lost", value=f"{df['Lost'].iloc[-1]} packets", delta=f"{df['Lost'].iloc[-1]-df['Lost'].iloc[-2]} packets")


        for i, column in enumerate(sensor_columns):
            # Plot the data, plots must all have the same size
            graph_placeholders[i][0].write(f"Graph for **{column}**")
            graph_placeholders[i][1].line_chart(df[column], height=300)

        #columns.empty()

        time.sleep(update_time)

elif option == 'Radiation':
    st.title('Radiation')

    col1, col2 = st.columns(2)
    col1 = st.empty()
    col2 = st.empty()
    sub_title = st.empty()
    label = st.empty()
    chart = st.empty()

    while True:
        df = get_csv(file_to_load)
        
        col1.metric(label="Time", value=f"{df['Time'].iloc[-1]}")
        col2.metric(label="Counts per Minute", value=f"{df['Counts per Minute'].iloc[-1]}")

        sub_title.markdown(f"### Plots")
        
        label.write(f"Graph for **Counts per Minute**")
        chart.line_chart(df['Counts per Minute'], height=300)

        time.sleep(update_time)

elif option == 'Location':
    st.title('Location')
    time_place = st.empty()
    columns = st.empty()
    plot1 = st.empty()
    plot2 = st.empty()

    while True:
        df = get_csv(file_to_load)

        time_place.metric(label="Time", value=f"{df['Time'].iloc[-1]}")
        with columns:
            col1, col2 = st.columns(2)
        col1.metric(label="Latitude", value=f"{df['Latitude'].iloc[-1]}")
        col2.metric(label="Longitude", value=f"{df['Longitude'].iloc[-1]}")

        plot1.map(df[['Latitude', 'Longitude']].rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}), zoom=10)
        plot2.area_chart(df['Altitude'], height=300)

        time.sleep(update_time)

elif option == 'Other':
    st.title('Other Relevant Data-Specific Information')
    placeholder = st.empty()
    while True:
        df = get_csv(file_to_load)
    
        placeholder.markdown(f"""
        Nan values in the dataframe: \n{df.isna().sum()}
        Final shape of the dataframe: {df.shape}
        """)

        time.sleep(update_time)


    
