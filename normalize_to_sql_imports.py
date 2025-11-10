# normalize_to_sql_imports.py
import pandas as pd
df = pd.read_csv('all_trending_videos.csv')
df.columns = df.columns.str.strip()

# channels
channels = df[['channel_title']].drop_duplicates().reset_index(drop=True)
channels['channel_id'] = channels.index + 1
channels.to_csv('channels.csv', index=False)

# categories
if 'category_id' in df.columns:
    categories = df[['category_id']].drop_duplicates().sort_values('category_id').reset_index(drop=True)
    categories['category_name'] = None
    categories.to_csv('categories.csv', index=False)

# videos - one row per video_id
videos = df[['video_id','channel_title','title','publish_time','category_id','thumbnail_link','description']].drop_duplicates(subset=['video_id']).reset_index(drop=True)
channels_map = dict(zip(channels['channel_title'], channels['channel_id']))
videos['channel_id'] = videos['channel_title'].map(channels_map)
videos = videos.drop(columns=['channel_title'])
videos.to_csv('videos.csv', index=False)

# video_stats - time series snapshots
video_stats = df[['video_id','trending_date','views','likes','dislikes','comment_count','comments_disabled','ratings_disabled','video_error_or_removed']].copy()
video_stats['trending_date'] = pd.to_datetime(video_stats['trending_date'], errors='coerce').dt.date
video_stats.to_csv('video_stats.csv', index=False)

# tags -> tags.csv and video_tags.csv
if 'tags' in df.columns:
    df_tags = df[['video_id','tags']].drop_duplicates(subset=['video_id']).fillna('')
    tag_map = {}
    tag_rows = []
    video_tag_rows = []
    next_id = 1
    for _, r in df_tags.iterrows():
        vid = r['video_id']
        raw = r['tags']
        parts = [p.strip() for p in str(raw).split('|') if p.strip()]
        for p in parts:
            if p not in tag_map:
                tag_map[p] = next_id
                tag_rows.append({'tag_id': next_id, 'tag_text': p})
                next_id += 1
            video_tag_rows.append({'video_id': vid, 'tag_id': tag_map[p]})
    import pandas as pd
    pd.DataFrame(tag_rows).to_csv('tags.csv', index=False)
    pd.DataFrame(video_tag_rows).to_csv('video_tags.csv', index=False)

print("Wrote: channels.csv, categories.csv, videos.csv, video_stats.csv, tags.csv (if tags exist), video_tags.csv")
