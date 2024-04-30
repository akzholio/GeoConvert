# GeoConvert

### This Streamlit app provides an intuitive interface to process geographical data in one of two ways:

- **Location to Coordinates**: Upload a file containing named locations (e.g., cities, states, countries), and the app will convert these into corresponding geographical coordinates (latitude and longitude).
- **Coordinates to Location**: Upload a file containing geographical coordinates (latitude and longitude), and the app will convert these into corresponding named locations (e.g., cities, states, countries).
### How to Use the App
#### Upload your file:
The app accepts CSV or Excel files containing the necessary information for the conversion.
#### Run the Conversion:
Once your file is uploaded, the app will automatically infer the mode from columns, process the data and display the results.
#### Download Results:
You can download the processed data as a new file, ready for use or further analysis.
### Dependencies
- Python 3.11+
- Streamlit
- pandas
- Geopy
