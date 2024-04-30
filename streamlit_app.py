from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import streamlit as st
import pandas as pd
import time

USER_AGENT = "geoconvert"


geolocator = Nominatim(user_agent=USER_AGENT)


def geocode_location(row):
    """Fetch coordinates for a given location name using the Nominatim API."""
    time.sleep(1)
    location_name = row["location"]
    location = geolocator.geocode(location_name)
    if location:
        return (location.latitude, location.longitude)
    return "not_found"


def reverse_geocode(row):
    """Fetch location information for given coordinates using the Nominatim API."""
    time.sleep(1)
    lat, lon = row["latitude"], row["longitude"]
    geo_reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    location = geo_reverse((lat, lon))
    if location:
        return location.address
    return "not_found"


def has_required_columns(df, required_columns):
    """Check if a DataFrame has all the required columns."""
    # Get a set of the DataFrame's columns
    df_columns = set([column.lower() for column in df.columns])

    # Check if all required columns are present
    return df_columns.issuperset(required_columns)


def calculate_batch_size(df):
    return df.shape[0] // 100


def process_reverse_geocode(df, batch_size):
    progress_text = "Searching, please wait..."
    my_bar = st.progress(0, text=progress_text)
    for i in range(0, 100):
        my_bar.progress(i + 1, text=progress_text)
        i = i * batch_size
        df.loc[i:i + batch_size] = df.loc[i:i + batch_size]
        df.loc[i:i + batch_size, "location"] = df.apply(reverse_geocode, axis=1)
    time.sleep(1)
    my_bar.progress(100, text="Done!")


# Define the columns you're checking for
coordinates_required_columns = {"latitude", "longitude"}
locations_required_columns = {"location"}

st.title("GeoConvert")
st.write("Upload a file with coordinates or location names.")
uploaded_file = st.file_uploader("Choose a file", type=["csv"])
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    batch_size = calculate_batch_size(dataframe)
    progress_text = "Searching, please wait..."
    my_bar = st.progress(0, text=progress_text)
    if has_required_columns(dataframe, coordinates_required_columns):
        st.success("Found coordinates data!", icon="✅")
        dataframe["location_name"] = [None] * len(dataframe)
        try:
            for i in range(0, 100):
                my_bar.progress(i + 1, text=progress_text)
                i = i * batch_size
                dataframe.loc[i:i + batch_size] = dataframe.loc[i:i + batch_size]
                dataframe.loc[i:i + batch_size, "location"] = dataframe.apply(reverse_geocode, axis=1)
        except ValueError as e:
            st.write(e)
    elif has_required_columns(dataframe, locations_required_columns):
        st.success("Found locations data!", icon="✅")
        dataframe["latitude", "longitude"] = [None, None] * len(dataframe)
        try:
            for i in range(0, 100):
                my_bar.progress(i + 1, text=progress_text)
                i = i * batch_size
                dataframe.loc[i:i + batch_size] = dataframe.loc[i:i + batch_size]
                dataframe.loc[i:i + batch_size, "latitude":"longitude"] = dataframe.apply(geocode_location, axis=1)
        except ValueError as e:
            st.write(e)
    else:
        st.error("No coordinate or location data has been found!", icon="🚨")
    my_bar.progress(100, text="Done!")
