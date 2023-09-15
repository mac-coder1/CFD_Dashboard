import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


st.title('CFDs')

#import CFDs AR1-4
Auc_early = pd.read_csv('Data_inputs/auction-outcomes.csv')

#import CFDs AR5
Auc_late = pd.read_csv('Data_inputs/AR5.csv')

#clean up data
Auc_early.columns = Auc_early.columns.str.strip()
for col in ['Version', 'Publication_Date', 'Homes_Powered']:
    Auc_early = Auc_early.drop(col, axis=1)

#clean up data
Auc_late.columns = Auc_late.columns.str.strip()
Auc_late['Auction'] = 'AR5'
columns_to_drop = ['Project Location', 'Pot']
Auc_late = Auc_late.drop(columns_to_drop, axis=1)

# #rename columns
Auc_late = Auc_late.rename(columns={'Project Name': 'Project_Name', 'Applicant':'Developer', 'Technology Type':'Technology_Type', 'Size (MW)':'Capacity_MW','Strike Price (£/MWh)':'Strike_Price_GBP_Per_MWh', 'Delivery Year':'Delivery_Year'})

#concate two dataframes
Auc = pd.concat([Auc_early, Auc_late], ignore_index=True)

#drop any rows with missing values in Technology_Type
Auc = Auc.dropna(subset=['Technology_Type'])

# Find rows where 'Technology_Type' contains 'solar' or 'Solar', case-insensitive
mask = Auc['Technology_Type'].str.contains('solar', case=False)
# Update those rows to just say 'Solar'
Auc.loc[mask, 'Technology_Type'] = 'Solar'

# Find rows where 'Technology_Type' contains 'solar' or 'Solar', case-insensitive
mask = Auc['Technology_Type'].str.contains('tidal', case=False)
# Update those rows to just say 'Solar'
Auc.loc[mask, 'Technology_Type'] = 'Tidal'

# Find rows where 'Technology_Type' contains 'solar' or 'Solar', case-insensitive
mask = Auc['Technology_Type'].str.contains('offshore', case=False)
# Update those rows to just say 'Solar'
Auc.loc[mask, 'Technology_Type'] = 'Offshore Wind'

# Find rows where 'Technology_Type' contains 'solar' or 'Solar', case-insensitive
mask = Auc['Technology_Type'].str.contains('remote', case=False)
# Update those rows to just say 'Solar'
Auc.loc[mask, 'Technology_Type'] = 'Remote Island Wind'

# Find rows where 'Technology_Type' contains 'solar' or 'Solar', case-insensitive
mask = Auc['Technology_Type'].str.contains('onshore', case=False)
# Update those rows to just say 'Solar'
Auc.loc[mask, 'Technology_Type'] = 'Onshore Wind'


st.subheader('By Auction')
#sum up by different Techonlogy_Type
Auc_sum = Auc[['Auction','Capacity_MW']].groupby(['Auction']).sum()
st.bar_chart(Auc_sum)

st.subheader('By Type')
Auc_type_sum = Auc[['Technology_Type','Capacity_MW']].groupby(['Technology_Type']).sum()

no_offshore = st.checkbox('Without Offshore Wind')
if no_offshore:
    st.bar_chart(Auc_type_sum.drop(['Offshore Wind']), y='Capacity_MW')
else:
    st.bar_chart(Auc_type_sum, y='Capacity_MW')

gen_type = st.selectbox('Select Technology Type', Auc['Technology_Type'].unique())

Auc_type = Auc[Auc['Technology_Type'] == gen_type]
Auc_type_sum = Auc_type[['Auction','Capacity_MW']].groupby(['Auction']).sum()
st.bar_chart(Auc_type_sum, y='Capacity_MW')



st.header('Locations')


# geolocator = Nominatim(user_agent="geoapiExercises")
# st.write(geolocator.geocode('Energy Works (Hull), England'))
# #cycle through all projects and get lat and long
# Auc['Latitude'] = None
# Auc['Longitude'] = None
# for i in range(2):
#     location = geolocator.geocode(Auc['Project_Name'][i])
#     if location is not None:
#         Auc['Latitude'][i] = location.latitude
#         Auc['Longitude'][i] = location.longitude
#     else:
#         Auc['Latitude'][i] = None
#         Auc['Longitude'][i] = None

# st.write(Auc)



# df = Auc[['Project_Name']][:3]
# df = df.rename(columns={'Project_Name': 'Address'})


# def get_lat_lon(address):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     try:
#         location = geolocator.geocode(address)
#         if location is not None:
#             return location.latitude, location.longitude
#         else:
#             return None, None
#     except GeocoderTimedOut:
#         return get_lat_lon(address)

# def add_lat_lon_to_df(df):
#     df['latitude'], df['longitude'] = zip(*df['Address'].apply(get_lat_lon))
#     return df

# # Add latitude and longitude to the DataFrame
# df = add_lat_lon_to_df(df)

# # Streamlit app
# st.title("Address to Coordinates")

# # Display DataFrame on Streamlit
# st.write(df)

