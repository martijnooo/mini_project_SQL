# Import functions from data_cleaning_functions.py
from data_cleaning_functions import create_countries, clean_movies_data, clean_ufo_reports, clean_subscriber_data
import pandas as pd

# Use the functions
if __name__ == "__main__":
    # Create countries DataFrame
    countries_df = create_countries()
    
    # Clean movies data
    movies_df = pd.read_csv(r"C:\Users\Martijn\Downloads\netflix_titles_anandshaw.csv") 
    cleaned_movies_df = clean_movies_data(movies_df)
    
    # Clean UFO reports data
    ufo_report_df = pd.read_csv(r"C:\Users\Martijn\Downloads\nuforc_reports (1).csv")
    cleaned_ufo_df = clean_ufo_reports(ufo_report_df, countries_df)
    
    # Clean subscribers data
    subscribers_df = pd.read_csv(r"C:\Users\Martijn\Downloads\subscribers_netflix_2024 (1).csv")
    cleaned_subscribers_df = clean_subscriber_data(subscribers_df, countries_df)