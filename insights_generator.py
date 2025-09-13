import json
import pandas as pd

WINDOWS = [
    ("early_morning_04_08", 4, 8),
    ("morning_08_12", 8, 12),
    ("afternoon_12_16", 12, 16),
    ("evening_16_20", 16, 20),
    ("night_20_24", 20, 24),
]

def hour_to_window(hour):
    for name, start, end in WINDOWS:
        if start <= hour < end:
            return name
    return "night_20_24"

def generate_insights(input_csv, out_csv, out_json):
    df = pd.read_csv(input_csv)

    # ✅ Fix timestamp parsing (handles ISO8601 + timezone)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')

    if df['timestamp'].isnull().any():
        raise ValueError("Some timestamps could not be parsed. Check CSV values.")

    # Completion stats
    total_tasks = df[df['action'].isin(['completed', 'skipped'])]
    completed = (total_tasks['action'] == 'completed').sum()
    skipped = (total_tasks['action'] == 'skipped').sum()
    completion_rate = round(completed / (completed + skipped), 2) if (completed + skipped) > 0 else 0

    # Time window analysis
    df['hour'] = df['timestamp'].dt.hour
    df['window'] = df['hour'].apply(hour_to_window)
    window_stats = df[df['action'].isin(['completed', 'skipped'])].groupby('window')['action'].apply(
        lambda x: (x == 'completed').mean()
    )
    best_window = window_stats.idxmax() if not window_stats.empty else None
    best_window_rate = round(window_stats.max(), 2) if not window_stats.empty else None

    # Top tasks
    top_tasks = df[df['action'] == 'completed']['task_type'].value_counts().head(3).index.tolist()

    # Reward system
    rewards = []
    for _, row in df.iterrows():
        if row['action'] == 'completed':
            rewards.append(1)
        elif row['action'] == 'skipped':
            rewards.append(-1)
        else:
            rewards.append(0)
    df['reward'] = rewards
    weekly_score = df['reward'].sum()

    # Suggestions
    suggestions = []
    if best_window:
        suggestions.append(f"You complete more tasks in the {best_window.replace('_',' ')}. Schedule focus work then.")

    if 'study' in df['task_type'].values and (df.loc[df['task_type'] == 'study', 'action'] == 'skipped').any():
        suggestions.append("Study tasks are often skipped. Try breaking them into smaller chunks.")

    if 'relax' in df['task_type'].values and (df.loc[df['task_type'] == 'relax', 'action'] == 'skipped').any():
        suggestions.append("Relaxation is often skipped; consider shorter breaks earlier in the day.")

    insights = {
        "overall_completion_rate": completion_rate,
        "best_time_window": best_window,
        "top_tasks": top_tasks,
        "weekly_productivity_score": int(weekly_score),
        "suggestions": suggestions,
    }

    # Save CSV report
    rows = [
        {"metric": "overall_completion_rate", "value": completion_rate, "details": f"completed:{completed}, skipped:{skipped}"},
        {"metric": "best_time_window", "value": best_window, "details": f"completion_rate:{best_window_rate}"},
        {"metric": "top_task_types", "value": "|".join(top_tasks), "details": ""},
        {"metric": "weekly_productivity_score", "value": weekly_score, "details": "sum of rewards"},
    ]
    for i, s in enumerate(suggestions, start=1):
        rows.append({"metric": f"suggestion{i}", "value": s, "details": ""})

    pd.DataFrame(rows).to_csv(out_csv, index=False)

    # Save JSON report
    with open(out_json, "w") as f:
        json.dump(insights, f, indent=2)

    print("✅ Insights generated and saved.")
    return insights

if __name__ == "__main__":
    print("Insights generator started...")
    generate_insights(
        'user_behavior_log.csv',
        'insights_report_auto.csv',
        'insights_auto.json'
    )

