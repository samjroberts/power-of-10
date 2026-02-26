import pandas as pd, numpy as np
import matplotlib.pyplot as plt


def convert_to_seconds(t):
    time = t.split(":")
    time = [int(i) for i in time]
    return 60 * time[0] + time[1]


def _sort_age_categories(categories):
    """
    Sorts age categories in logical athletic order:
    Under categories (U17, U20) → SEN → Veterans (V35, V40, V45, ...)
    """
    def sort_key(cat):
        if cat.startswith("U"):
            return (0, int(cat[1:]))
        elif cat == "SEN":
            return (1, 0)
        elif cat.startswith("V"):
            return (2, int(cat[1:]))
        else:
            return (3, 0)

    return sorted(categories, key=sort_key)


# Performance bands: (lower_seconds, upper_seconds, label, colour)
_PERFORMANCE_BANDS = [
    (0,        18 * 60, "Sub 18:00",      "#2ecc71"),
    (18 * 60,  21 * 60, "18:00 – 21:00",  "#82ca50"),
    (21 * 60,  24 * 60, "21:00 – 24:00",  "#f1c40f"),
    (24 * 60,  27 * 60, "24:00 – 27:00",  "#e67e22"),
    (27 * 60,  30 * 60, "27:00 – 30:00",  "#e74c3c"),
    (30 * 60,  float("inf"), "30:00+",    "#8e44ad"),
]


def generate_age_sex_barchart(df):
    """
    Creates a grouped bar chart showing member distribution by age category and
    sex. Age categories are sorted in logical athletic order (U → SEN → V).
    Count labels are drawn above each bar.

    Output: barchart.png
    """
    age_categories = _sort_age_categories(df["age"].unique().tolist())
    sex_categories = ["M", "W"]
    colors = ["#3498db", "#e91e8c"]

    counts = {
        sex: [len(df[(df["age"] == age) & (df["sex"] == sex)]) for age in age_categories]
        for sex in sex_categories
    }

    x = np.arange(len(age_categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (sex, color) in enumerate(zip(sex_categories, colors)):
        bars = ax.bar(
            x + (i - 0.5) * width, counts[sex], width,
            label="Male" if sex == "M" else "Female",
            color=color, alpha=0.85,
        )
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(
                    str(int(height)),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9,
                )

    ax.set_xticks(x)
    ax.set_xticklabels(age_categories)
    ax.set_title("Membership by Age Category and Sex", fontsize=14)
    ax.set_xlabel("Age Category")
    ax.set_ylabel("Number of Members")
    ax.legend(title="Sex")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig("barchart.png", dpi=150)
    plt.clf()


def generate_boxplot(df):
    """
    Creates a box plot showing the distribution of best parkrun times by age
    category. Age categories are sorted in logical athletic order. The y-axis
    displays time as MM:SS.

    Output: boxplot.png
    """
    age_categories = _sort_age_categories(df["age"].unique().tolist())

    data = []
    valid_cats = []
    for age in age_categories:
        times = [
            convert_to_seconds(t)
            for t in df.loc[df["age"] == age, "parkrun"].dropna().tolist()
        ]
        if times:
            data.append(times)
            valid_cats.append(age)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data, patch_artist=True, labels=valid_cats,
               boxprops=dict(facecolor="#aed6f1", color="#2980b9"),
               medianprops=dict(color="#e74c3c", linewidth=2))
    ax.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Best Parkrun Times by Age Category", fontsize=14)
    ax.set_xlabel("Age Category")
    ax.set_ylabel("Time (MM:SS)")

    yticks = np.arange(780, 2400, 60)
    ylabels = [f"{x // 60}:{x % 60:02d}" for x in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    plt.tight_layout()
    plt.savefig("boxplot.png", dpi=150)
    plt.clf()


def generate_performance_level_chart(df):
    """
    Creates a stacked bar chart showing how many members in each age category
    fall into each parkrun time band. This gives a clear view of overall
    performance level across the club's demographics.

    Performance bands (absolute parkrun time):
        Sub 18:00 | 18–21 | 21–24 | 24–27 | 27–30 | 30:00+

    Output: performance_levels.png
    """
    age_categories = _sort_age_categories(df["age"].unique().tolist())

    df = df.copy()
    df["seconds"] = df["parkrun"].apply(convert_to_seconds)

    fig, ax = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(age_categories))

    for lo, hi, label, color in _PERFORMANCE_BANDS:
        counts = []
        for age in age_categories:
            subset = df[df["age"] == age]["seconds"]
            counts.append(int(((subset >= lo) & (subset < hi)).sum()))
        ax.bar(age_categories, counts, bottom=bottom, label=label, color=color, alpha=0.9)
        bottom += np.array(counts, dtype=float)

    ax.set_title("Performance Levels by Age Category", fontsize=14)
    ax.set_xlabel("Age Category")
    ax.set_ylabel("Number of Members")
    ax.legend(title="Parkrun Time Band", loc="upper right", fontsize=9)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig("performance_levels.png", dpi=150)
    plt.clf()


def generate_sex_split_performance_boxplot(df):
    """
    Creates two side-by-side box plots — one for male members, one for female —
    each showing the distribution of best parkrun times per age category.
    The shared y-axis makes it easy to compare performance levels between sexes.

    Output: sex_split_boxplot.png
    """
    age_categories = _sort_age_categories(df["age"].unique().tolist())
    sex_info = [("M", "Male", "#3498db"), ("W", "Female", "#e91e8c")]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for ax, (sex, label, color) in zip(axes, sex_info):
        sex_df = df[df["sex"] == sex]
        data = []
        valid_cats = []
        for age in age_categories:
            times = [
                convert_to_seconds(t)
                for t in sex_df.loc[sex_df["age"] == age, "parkrun"].dropna().tolist()
            ]
            if times:
                data.append(times)
                valid_cats.append(age)

        if data:
            bp = ax.boxplot(
                data, patch_artist=True, labels=valid_cats,
                boxprops=dict(facecolor=color, alpha=0.6),
                medianprops=dict(color="#2c3e50", linewidth=2),
            )

        ax.yaxis.grid(True, linestyle="-", which="major", color="lightgrey", alpha=0.5)
        ax.set_axisbelow(True)
        ax.set_title(f"{label} Members", fontsize=12)
        ax.set_xlabel("Age Category")
        if sex == "M":
            ax.set_ylabel("Time (MM:SS)")

        yticks = np.arange(780, 2400, 60)
        ylabels = [f"{x // 60}:{x % 60:02d}" for x in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)

    fig.suptitle("Best Parkrun Times by Age Category and Sex", fontsize=14)
    plt.tight_layout()
    plt.savefig("sex_split_boxplot.png", dpi=150)
    plt.clf()
