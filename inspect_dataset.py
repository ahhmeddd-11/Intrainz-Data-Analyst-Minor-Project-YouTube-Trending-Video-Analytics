# inspect_dataset.py
import pandas as pd
pd.set_option('display.max_columns', 200)

df = pd.read_csv('all_trending_videos.csv')  # path if inside repo
print("Rows:", len(df))
print("Columns:", list(df.columns))
print("\nColumn dtypes:\n", df.dtypes)
print("\nMissing value counts:\n", df.isnull().sum())
print("\nSample rows:\n", df.head().to_string(index=False))
# Save a small sample to include in your report
df.head(10).to_csv('sample_rows_for_report.csv', index=False)
# Save a datadict (column name, unique count, dtype)
datadict = []
for c in df.columns:
    datadict.append({'column': c, 'dtype': str(df[c].dtype), 'unique_count': int(df[c].nunique(dropna=True)), 'missing': int(df[c].isnull().sum())})
pd.DataFrame(datadict).to_csv('data_dictionary.csv', index=False)
print("Wrote sample_rows_for_report.csv and data_dictionary.csv")
# counts & specifics
print("Unique videos:", df['video_id'].nunique())
print("Unique channels:", df['channel_title'].nunique())
print("Unique categories:", df['category_id'].nunique())
# top categories by rows
print(df['category_id'].value_counts().head(10))
# if there is a 'publish_time' convert and show unique publish hours
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
print("Publish hours sample:\n", df['publish_time'].dt.hour.value_counts().head(10))
