import pandas as pd
import numpy as np

# Load dataset 
# For real data, please refer to repository  : 
#https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsInvocationTrace2021.md
df = pd.read_csv('AzureFunctionsInvocationTraceForTwoWeeksJan2021.txt')


# Step 2: Convert end_timestamp (in seconds) to hour of the day
df["hour"] = pd.to_datetime(df["end_timestamp"], unit='s').dt.hour

# Step 3: Choose 10 unique app IDs
unique_apps = df["app"].unique()[:10]  # First 10 unique apps
df = df[df["app"].isin(unique_apps)]

# Step 4: Count invocations per hour per app
invocation_matrix = (
    df.groupby(["hour", "app"])
    .size()
    .unstack(fill_value=0)
    .reindex(index=range(24), fill_value=0)  # Ensure 24 hours
)

# Step 5: Normalize each column to 0–100 range
normalized_matrix = invocation_matrix.apply(lambda col: 
    100 * (col - col.min()) / (col.max() - col.min()) if col.max() > col.min() else 0
)

# Step 6: Save as a .py file with a variable
with open("data.py", "w") as f:
    f.write("data = [\n")
    for row in normalized_matrix.to_numpy():
        formatted = ", ".join(f"{val:.2f}" for val in row)
        f.write(f"    [{formatted}],\n")
    f.write("]\n")
