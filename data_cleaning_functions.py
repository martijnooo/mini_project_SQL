import pandas as pd
import numpy as np
import pycountry

# Function to create countries DataFrame
def create_countries():
    def get_country_code(country_name):
        if isinstance(country_name, str):  # Check if it's a string
            country = pycountry.countries.get(name=country_name)
            return country.alpha_2 if country else None
        return None

    countries_short = [country.alpha_2 for country in pycountry.countries]
    countries_name = [country.name for country in pycountry.countries]
    countries_df = pd.DataFrame({'handle': countries_short, 'name': countries_name}).reset_index()
    countries_df = countries_df.rename(columns={"index": "country_id"})
    return countries_df

# Function to clean movies data
def clean_movies_data(movies_df):
    # Clean and filter movies
    movies_df['ufo_theme'] = np.where(
        movies_df['description'].str.contains(
            'alien|ufo|extraterrestrial|spaceship|spacecraft|cosmic|intergalactic|martian|extraterrestrials|galactic|asteroid|space|starship', 
            case=False, na=False), 
        1, 0
    )
    movies_df['date_added'] = pd.to_datetime(movies_df['date_added'], errors='coerce')
    movies_df = movies_df.dropna(subset=['date_added'])
    movies_df = movies_df[['date_added', 'ufo_theme', 'release_year', 'type', 'title']]
    movies_df['date_added_formatted'] = movies_df['date_added'].dt.strftime('%m/%Y')

    return movies_df

# Function to clean UFO reports data
def clean_ufo_reports(ufo_report_df, countries_df):
    def add_country_code_to_ufo(ufo_report_df):
        def get_country_code(country_name):
            if isinstance(country_name, str):  # Check if it's a string
                country = pycountry.countries.get(name=country_name)
                return country.alpha_2 if country else None
            return None

        ufo_report_df['country_code'] = ufo_report_df['country'].apply(lambda x: get_country_code(x) 
            if isinstance(x, str) and x.lower() not in ['non applicable', 'unknown', 'in orbit', 'at sea'] else None)
        ufo_report_df = ufo_report_df.dropna(subset=['country_code'])
        return ufo_report_df

    def country_indexing(ufo_report_df, countries_df):
        ufo_report_df = ufo_report_df.merge(countries_df[['handle', 'country_id']], how='left', left_on='country_code', right_on='handle')
        ufo_report_df['country_code'] = ufo_report_df['country_id']
        ufo_report_df.drop(columns=['handle', 'country_id', "country"], inplace=True)
        ufo_report_df = ufo_report_df.rename(columns={"country_code": "country_id"})
        return ufo_report_df

    # Clean UFO reports data
    ufo_report_df.columns = ufo_report_df.columns.str.lower()
    ufo_report_df = ufo_report_df.drop(columns=['date','posted', 'shape', 'duration', 'image', 'link', 'summary', 'text'])
    ufo_report_df = ufo_report_df.rename(columns={'date_table': 'date'})
    
    correct_format = r'^\d{1,2}/\d{4}$'
    ufo_report_df = ufo_report_df[ufo_report_df['date'].str.match(correct_format, na=False)]
    
    invalid_countries = ['no', 'unknown', 'none', 'not applicable', 'unknown/at sea', 'unavailable', 'in orbit', 'space', 'atlantic ocean', 'caribbean sea', 'pacific ocean', 'international space station', 'moon', 'mars', 'none', 'not found']
    ufo_report_df = ufo_report_df[~ufo_report_df['country'].str.lower().isin(invalid_countries)]

    # Call the functions to add country code and merge with country information
    ufo_report_df = add_country_code_to_ufo(ufo_report_df)
    ufo_report_df = country_indexing(ufo_report_df, countries_df)

    return ufo_report_df

# Function to clean subscribers data
def clean_subscriber_data(subscribers_df, countries_df):
    # Clean subscribers data
    subscribers_df = subscribers_df.rename(columns={'estimated_subscribers': 'subscribers'}).reset_index(drop=True)
    
    # country indexing
    subscribers_df = subscribers_df.merge(countries_df[['handle', 'country_id']], how='left', left_on='country_code', right_on='handle')
    subscribers_df['country_code'] = subscribers_df['country_id']
    subscribers_df.drop(columns=['handle', 'country_id', "country"], inplace=True)
    subscribers_df = subscribers_df.rename(columns={"country_code": "country_id"})
    
    return subscribers_df

# Function to create a date index DataFrame and adjust dates in UFO and movies data
def create_date_index(ufo_report_df, movies_df):
    # Get unique entries from both columns
    unique_dates_ufo = ufo_report_df["date"].unique()
    unique_dates_movies = movies_df["date_added_formatted"].unique()

    # Combine and get all unique entries
    all_unique_dates = pd.unique(np.concatenate((unique_dates_ufo, unique_dates_movies)))

    # Create a DataFrame for the date index
    date_index_df = pd.DataFrame({
        "date": all_unique_dates,
        "date_id": range(len(all_unique_dates))
    })

    # Create a mapping of dates to their indices in all_unique_dates
    date_to_index = {date: idx for idx, date in enumerate(all_unique_dates)}

    # Replace dates in ufo_report_df["date"] with their corresponding indices
    ufo_report_df["date_id"] = ufo_report_df["date"].map(date_to_index)

    # Replace dates in movies_df["date_added_formatted"] with their corresponding indices
    movies_df["date_id"] = movies_df["date_added_formatted"].map(date_to_index)

    return ufo_report_df, movies_df, date_index_df