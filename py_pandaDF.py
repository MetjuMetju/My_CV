import pandas as pd

# Create a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Access a specific column
print(df["Name"])

# Filter rows
print(df[df["Age"] > 30])

