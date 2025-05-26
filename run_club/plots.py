import pandas as pd, numpy as np
import matplotlib.pyplot as plt


def convert_to_seconds(t):
    time = t.split(":")
    time = [int(i) for i in time]
    return 60 * time[0] + time[1]


def generate_age_sex_barchart(df):
    age_categories = df["age"].unique()
    sex_categories = ["M", "W"]

    bardata = pd.DataFrame()
    for sex in sex_categories:
        age_split = []
        for age in age_categories:
            age_split.append(len(df[(df["age"] == age) & (df["sex"] == sex)]))
        additional = pd.DataFrame(data={sex: age_split})
        bardata = pd.concat([bardata, additional], axis=1)

    barchart = bardata.plot(kind="bar")
    barchart.set_xticklabels(age_categories)
    plt.title("Shape of Membership")
    plt.xlabel("Age Category")
    plt.ylabel("# Members")
    plt.savefig("barchart.png")
    plt.clf()

def generate_boxplot(df):
    age_categories = df["age"].unique().tolist()
    print("ages:", age_categories)
    
    boxdata = pd.DataFrame()
    for age in age_categories:
        list = df.loc[df["age"] == age, "parkrun"].dropna().tolist()
        times = [convert_to_seconds(i) for i in list]
        additional = pd.DataFrame(data={age: times})
        boxdata = pd.concat([boxdata, additional], axis=1)
    
    boxplot = boxdata.boxplot(column=age_categories)
    boxplot.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
    boxplot.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Best Parkrun Times by Age Category",
        xlabel="Distribution",
        ylabel="Value",
    )
    yticks = np.arange(780, 2400, 60)
    ylabels = [int(x / 60) for x in yticks]
    boxplot.set_yticks(yticks, ylabels)
    plt.savefig("boxplot.png")
    plt.clf()
