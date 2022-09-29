import pandas as pd
import streamlit as st
import pandas as pd
import datetime
from PIL import Image

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

sensor_columns = ['Internal Temperature', 'External Temperature', 'Pressure', 'Voltage', 'RSSI',  'Altitude', 'Distance', 'Power', 'Received', 'Lost']
radiation_columns = ['Counts per Minute']
location_columns = ['Latitude', 'Longitude']


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

# Beautify column names



option = st.selectbox(
    'Choose window',
    ('General Stats', 'Radiation', 'Location', 'Other'))

if option == 'General Stats':
    st.title('General Stats')

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Internal Temperature", value=f"{df['Internal Temperature'].iloc[-1]} °C", delta=f"{df['Internal Temperature'].iloc[-1]-df['Internal Temperature'].iloc[-2]} °C")
    col2.metric(label="External Temperature", value=f"{df['External Temperature'].iloc[-1]} °C", delta=f"{df['External Temperature'].iloc[-1]-df['External Temperature'].iloc[-2]} °C")
    col3.metric(label="Pressure", value=f"{df['Pressure'].iloc[-1]} hPa", delta=f"{df['Pressure'].iloc[-1]-df['Pressure'].iloc[-2]} hPa")
    col4.metric(label="Voltage", value=f"{df['Voltage'].iloc[-1]} V", delta=f"{df['Voltage'].iloc[-1]-df['Voltage'].iloc[-2]} V")
    col5.metric(label="RSSI", value=f"{df['RSSI'].iloc[-1]} dBm", delta=f"{df['RSSI'].iloc[-1]-df['RSSI'].iloc[-2]} dBm")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Altitude", value=f"{df['Altitude'].iloc[-1]} meters", delta=f"{df['Altitude'].iloc[-1]-df['Altitude'].iloc[-2]} meters")
    col2.metric(label="Distance", value=f"{df['Distance'].iloc[-1]} meters", delta=f"{df['Distance'].iloc[-1]-df['Distance'].iloc[-2]} meters")
    col3.metric(label="Power", value=f"{df['Power'].iloc[-1]} mW", delta=f"{df['Power'].iloc[-1]-df['Power'].iloc[-2]} mW")
    col4.metric(label="Received", value=f"{df['Received'].iloc[-1]} packets", delta=f"{df['Received'].iloc[-1]-df['Received'].iloc[-2]} packets")
    col5.metric(label="Lost", value=f"{df['Lost'].iloc[-1]} packets", delta=f"{df['Lost'].iloc[-1]-df['Lost'].iloc[-2]} packets")


    st.markdown(f"### Plots")

    for column in sensor_columns:
        # Plot the data, plots must all have the same size
        st.write(f"Graph for **{column}**")
        st.line_chart(df[column], height=300)

elif option == 'Radiation':
    st.title('Radiation')

    col1, col2 = st.columns(2)
    col1.metric(label="Time", value=f"{df['Time'].iloc[-1]}")
    col2.metric(label="Counts per Minute", value=f"{df['Counts per Minute'].iloc[-1]}")

    st.markdown(f"### Plots")

    for column in radiation_columns:
        # Plot the data, plots must all have the same size
        st.write(f"Graph for **{column}**")
        st.line_chart(df[column], height=300)
    col2.metric(label="Counts per Minute", value=f"{df['Counts per Minute'].iloc[-1]} counts", delta=f"{df['Counts per Minute'].iloc[-1]-df['Counts per Minute'].iloc[-2]} counts")
    

    st.markdown(f"### Plots")

    for column in radiation_columns:
        # Plot the data, plots must all have the same size
        st.write(f"Graph for **{column}**")
        st.line_chart(df[column], height=300)

elif option == 'Location':
    st.title('Location')

    st.metric(label="Time", value=f"{df['Time'].iloc[-1]}")
    col1, col2 = st.columns(2)
    col1.metric(label="Latitude", value=f"{df['Latitude'].iloc[-1]}")
    col2.metric(label="Longitude", value=f"{df['Longitude'].iloc[-1]}")

    st.markdown(f"### Plots")
    st.map(df[['Latitude', 'Longitude']].rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}), zoom=10)
    st.area_chart(df['Altitude'], height=300)

elif option == 'Other':
    st.title('Other Relevant Data-Specific Information')
    
    st.markdown(f"""
    Nan values in the dataframe: \n{df.isna().sum()}
    Final shape of the dataframe: {df.shape}
    """)


    
