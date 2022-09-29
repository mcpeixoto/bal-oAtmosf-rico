import pandas as pd
import streamlit as st
import pandas as pd
import datetime

option = st.selectbox(
    'Choose dataset',
    ('Dataset 1', 'Dataset 2'))

if option == 'Dataset 1':
    df = pd.read_csv("dataset1.csv", index_col=0, sep=';')
elif option == 'Dataset 2':
    df = pd.read_csv("dataset2.csv", index_col=0, sep=';')

sensor_columns = ['int_temperature', 'ext_temperature', 'pressure', 'voltage', 'rssi',  'altitude', 'distance', 'Power', '#Received', '#Lost']
radiation_columns = ['cpm']
location_columns = ['latitude', 'longitude']


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
df['time'] = df['time'].apply(lambda x: datetime.timedelta(seconds=x))


option = st.selectbox(
    'Choose window',
    ('General Stats', 'Radiation', 'Location', 'Other'))

if option == 'General Stats':
    st.title('General Stats')

    # Same but now in markdown
    st.markdown(f"""
    ### Mesurements at {df['time'].iloc[-1]}
    - Altitude {df['altitude'].iloc[-1]} meters
    - External Temperature {df['ext_temperature'].iloc[-1]} °C
    - Internal Temperature {df['int_temperature'].iloc[-1]} °C
    - Pressure {df['pressure'].iloc[-1]} hPa
    - Voltage {df['voltage'].iloc[-1]} V
    - RSSI {df['rssi'].iloc[-1]} dBm
    - Distance {df['distance'].iloc[-1]} meters
    - Power {df['Power'].iloc[-1]} mW
    - Received {df['#Received'].iloc[-1]}
    - Lost {df['#Lost'].iloc[-1]}
    """)


    st.markdown(f"### Plots")

    for column in sensor_columns:
        # Plot the data, plots must all have the same size
        st.write(f"Graph for **{column}**")
        st.line_chart(df[column], height=300)

elif option == 'Radiation':
    st.title('Radiation')

    st.markdown(f"""
    ### Mesurements at {df['time'].iloc[-1]}
    - Radiation {df['cpm'].iloc[-1]} cpm
    """)

    st.markdown(f"### Plots")

    for column in radiation_columns:
        # Plot the data, plots must all have the same size
        st.write(f"Graph for **{column}**")
        st.line_chart(df[column], height=300)

elif option == 'Location':
    st.title('Location')

    st.markdown(f"""
    ### Mesurements at {df['time'].iloc[-1]}
    - Latitude {df['latitude'].iloc[-1]}
    - Longitude {df['longitude'].iloc[-1]}
    """)

    st.markdown(f"### Plots")
    st.map(df[['latitude', 'longitude']], zoom=10)

elif option == 'Other':
    st.title('Other Relevant Data-Specific Information')
    
    st.markdown(f"""
    Nan values in the dataframe: \n{df.isna().sum()}
    Final shape of the dataframe: {df.shape}
    """)


    
