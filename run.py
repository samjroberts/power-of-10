import power_of_10, parkrun
import pandas as pd, numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

df = pd.read_excel("members.xlsx", sheet_name="Members")

# Splitting the 'Name' column
df["first_name"] = df["Name"].str.split().str[0]
df["surname"] = df["Name"].str.split().str[1]
df = df.drop(columns=["Name"])

print("Found ", len(df), " members from Excel...\n")
print("Searching Power of 10 for associated Athlete IDs:")
for index, row in tqdm(df.iterrows(), total=df.shape[0], ascii="░▒█"):
    try:
        athletes = power_of_10.search_athletes(
            firstname=row["first_name"], surname=row["surname"], club="Ranelagh"
        )
        df.loc[index, "athlete_id"] = athletes[0].get("athlete_id")
        df.loc[index, "age"] = athletes[0].get("xc")
        df.loc[index, "sex"] = athletes[0].get("sex")
    except Exception as ex:
        x = ex.args[0]

df = df.dropna(subset=["athlete_id"])

print("\n", len(df), "associated Athelete IDs found...")
print("\nIterating over past performances to find fastest parkrun:")


for index, row in tqdm(df.iterrows(), total=df.shape[0], ascii="░▒█"):
    try:
        performances = power_of_10.get_athlete(row["athlete_id"])["performances"]
        year = "24"
        fastest_parkrun = min(
            x["value"]
            for x in performances
            if x["event"] == "parkrun" and year in x["date"]
        )
        df.loc[index, "parkrun"] = fastest_parkrun
    except Exception as ex:
        x = ex.args[0]

df = df.dropna(subset=["parkrun"])

print("\n", len(df), "athletes with parkrun times found...", len(df))

boxplot_df = pd.DataFrame()
age_categories = df["age"].unique()

def convert_to_seconds(t):
    time = t.split(":")
    time = [int(i) for i in time]
    return 60 * time[0] + time[1]

for age in age_categories:
    list = df.loc[df["age"] == age, "parkrun"].dropna().tolist()
    times = [convert_to_seconds(i) for i in list]
    print(times)
    d = {age: times}
    additional = pd.DataFrame(data=d)
    boxplot_df = pd.concat([boxplot_df, additional], axis=1)

boxplot = boxplot_df.boxplot(column=["SEN", "V45", "V50"])
plt.title("Basic Box Plot")

boxplot.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
boxplot.set(
    axisbelow=True,  # Hide the grid behind plot objects
    title="Ranelagh Harriers 5k (Parkrun) Times by Age Category",
    xlabel="Distribution",
    ylabel="Value",
)
# locs, labels = plt.yticks()
yticks = np.arange(780, 2400, 60)
ylabels = [int(x / 60) for x in yticks]
boxplot.set_yticks(yticks, ylabels)

# y_timedelta = [str(timedelta(seconds=s)) for s in plt.yticks()]
# plt.yticks(y_timedelta)

plt.savefig("boxplot.png")

# parkrun.get_results(club_num="947")
