import pandas as pd
import numpy as np

from CountryCodeList import EarthCountries

def DefineCountriesDropdown():
	dataq = pd.read_csv('quake_db_1965-2016.csv')
	dataq = dataq[dataq['Place'] != 'Unknown']

	dataq['CountryCode'] = dataq['Place'].apply(lambda col : col.split(', ')[len(col.split(', ')) - 1])
	top_codes = dataq['CountryCode'].value_counts().nlargest(30).index
	top_codes = list(top_codes)

	risky_countries = {}
	for code in top_codes:
		for country_name, country_code in EarthCountries.items():
			if country_code == code:
				risky_countries[country_name] = country_code
	return risky_countries

risky_countries = DefineCountriesDropdown()
del risky_countries['Philippines']
del risky_countries['Chile']

def GrabContentPerYear(year):
	cn_year_df = country_df[country_df['Year'] == int(year)]
	return cn_year_df

def GetDataYearValue(country_df, value):
	data = country_df[country_df['Year'] == value]
	return data

def GetCountryDataByYear(risky_code, year_value):
	dataq = pd.read_csv('quake_db_1965-2016.csv')
	risky_country = dataq[dataq['Place'].str.contains(risky_code)]
	risky_country = risky_country[['Date', 'Latitude', 'Longitude', 'Magnitude', 'Depth', 'Type', 'Place']]
	_, _, risky_country['Year'] = risky_country['Date'].str.split('/').str
	risky_country.loc[:, 'Year'] = risky_country.loc[:, 'Year'].astype(int)
	risky_country = GetDataYearValue(risky_country, year_value)
	return risky_country