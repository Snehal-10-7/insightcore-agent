# InsightCore Agent — Behavioral Pattern & Action Dashboard

##  Overview

The *InsightCore Agent* is a lightweight behavioral analytics engine for a smart assistant.
It logs user tasks (completed, skipped, repeated), analyzes patterns (time windows, task types, completion rates), and generates *insights & suggestions* to improve productivity and wellbeing.

---

##  Project Structure


/insightcore-agent/
├── user_behavior_log.csv      # sample input log of user tasks
├── data_logger.py             # helper to append new events
├── insights_generator.py      # generates insights from logs
├── insights_report_auto.csv   # generated CSV insights
├── insights_auto.json         # generated JSON insights
├── README.md                  # documentation
└── summary.pdf                # architecture & explanation report


---

## ⚙ How to Run

1. Clone or unzip the repo.
2. Ensure Python 3.8+ is installed.
3. Install dependencies:
   pip install pandas
4. Run the insights generator:
   python insights_generator.py
5. Check the outputs:
   * *insights\_report\_auto.csv* → tabular insights
   * *insights\_auto.json* → structured insights for dashboards

---

 Features

* Logs and tracks user tasks (CSV-based).
* Calculates:

  * Completion rate
  * Best time window
  * Top task types
  * Weekly productivity score
* Exports insights as CSV & JSON.
* Generates human-readable suggestions.
* Rule-based reward (+1 completed, -1 skipped, 0 repeated).

---

# Demo Recording Guide (2–3 min)

1. *Intro (10 sec):* Title screen “InsightCore Agent Demo”.
2. *Input (30 sec):* Open user_behavior_log.csv and explain fields.
3. *Run Script (30 sec):* Show python insights_generator.py in terminal.
4. *Output (30 sec):* Open insights_report_auto.csv and highlight metrics.
5. *JSON (30 sec):* Show insights_auto.json.
6. *Closing (20 sec):* Mention suggestions and possible extensions (Power BI, feedback loop).

---

##  Next Steps (Stretch Goals)

* Integrate with SQLite for scalable storage.
* Add Google Collab dashboard for real-time visualization.
* Introduce reinforcement learning feedback loop (thumbs up/down).
* Display top 3 positive habits and 3 drop-off areas weekly.


👤 Author
Snehal Kadam