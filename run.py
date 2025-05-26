import power_of_10, parkrun, run_club
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

df = run_club.fetch_members_from_xlsx("members.xlsx", "Members")
print("Found ", len(df), " members from Excel...\n")

df = run_club.combine_power_of_ten(df)
print(df)

# Generate charts...
run_club.generate_age_sex_barchart(df)
run_club.generate_boxplot(df)

# parkrun.get_results(club_num="947")
