import pygrib
import pandas as pd

def load_grib2_to_dataframe(grib_file_path):
    # Open the .grib2 file using pygrib
    grib_file = pygrib.open(grib_file_path)

    # Get the first GRIB message (this can be changed if needed)
    grib_message = grib_file.message(1)  # Change the index if you want different messages
    
    # Extract the data, latitudes, and longitudes
    data, lats, lons = grib_message.data()

    # Reshape the data to 1D
    data_flat = data.flatten()
    lats_flat = lats.flatten()
    lons_flat = lons.flatten()

    # Create a pandas DataFrame using the flattened data
    df = pd.DataFrame({
        'Latitude': lats_flat,
        'Longitude': lons_flat,
        'Value': data_flat
    })

    # Close the GRIB file after processing
    grib_file.close()
    
    return df


def save_dataframe_to_excel(df, output_xlsx):
    # Save the entire DataFrame to an Excel file
    df.to_excel(output_xlsx, engine='openpyxl', index=False)
    print(f"Data saved to {output_xlsx}")


def main():
    # Specify the path to your GRIB2 file and output XLSX file
    grib_file_path = './bdd/constant-arome-eurw1s40-2024.grib2'  # Replace with your actual .grib2 file path
    output_xlsx = 'output_data.xlsx'  # The path where the Excel file will be saved

    # Load GRIB2 data into a pandas DataFrame
    df = load_grib2_to_dataframe(grib_file_path)
    
    # Show a portion of the DataFrame (for example, the first 10 rows)
    print("Showing a portion of the DataFrame:")
    print(df.head(10))  # Change the number as needed (e.g., df.head(20) for a larger preview)
    
    # Save the entire DataFrame to an Excel file
    save_dataframe_to_excel(df.head(1000), output_xlsx)


# Run the main function
if __name__ == '__main__':
    main()
