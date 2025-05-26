import pandas as pd, numpy as np
from tqdm import tqdm
import power_of_10

def fetch_members_from_xlsx(file, sheet_name):
    df = pd.read_excel(file, sheet_name=sheet_name)
    # Splitting the 'Name' column
    df["first_name"] = df["Name"].str.split().str[0]
    df["surname"] = df["Name"].str.split().str[1]
    return df.drop(columns=["Name"])

def combine_power_of_ten(df):
    current_year = "24"
    
    print("Fetching data for", len(df), "athletes from Power of 10:")
    for index, row in tqdm(df.iterrows(), total=df.shape[0], ascii="░▒█"):
        try:
            athletes = power_of_10.search_athletes(
                firstname=row["first_name"], surname=row["surname"], club="Ranelagh"
            )
            if athletes[0]:
                performances = power_of_10.get_athlete(athletes[0].get("athlete_id"))["performances"]
                fastest_parkrun = min(
                    x["value"]
                    for x in performances
                    if x["event"] == "parkrun" and current_year in x["date"]
                )
                df.loc[index, "parkrun"] = fastest_parkrun
                df.loc[index, "athlete_id"] = athletes[0].get("athlete_id")
                df.loc[index, "age"] = athletes[0].get("xc")
                df.loc[index, "sex"] = athletes[0].get("sex")
        except Exception as ex:
            x = ex.args[0]
    
    # Remove those without an Athlete ID
    df = df.dropna(subset=["athlete_id"])
    df = df.dropna(subset=["parkrun"])
    
    return df