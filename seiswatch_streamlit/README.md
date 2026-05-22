# 🌋 SEISWATCH — Streamlit Edition

AI-powered Earthquake Early Warning System built entirely in Streamlit.
Deploy in one click on Streamlit Cloud.

## Files

```
seiswatch_streamlit/
├── app.py                  ← entire app (single file)
├── requirements.txt        ← pip dependencies
├── .streamlit/
│   ├── config.toml         ← dark theme + wide layout
│   └── secrets.toml        ← API key (DO NOT commit)
└── README.md
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud (free)

1. Push this folder to a **GitHub repo**
2. Go to → https://share.streamlit.io
3. Click **New app**
4. Select your repo, branch `main`, file `app.py`
5. Click **Advanced settings → Secrets** and paste:

```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxx"
```

6. Click **Deploy** — live in ~60 seconds ✅

## Features

| Tab | What's inside |
|-----|---------------|
| 📊 Dashboard      | Live quake feed, filter/search, detail panel, P-wave chart, risk zones |
| 🗺️ Seismic Map    | Interactive Plotly globe with real quake markers + tectonic fault lines |
| 🤖 AI Prediction  | 6-parameter ML sliders → risk gauge, aftershock %, intensity, radius |
| 📈 LSTM Forecast  | 14-day magnitude forecast with confidence bands + model architecture |
| 🌊 Data Viz       | Live P/S wave chart, scatter, tectonic pressure gauges, tremor timeline |
| 🚨 Emergency      | Danger gauge, evacuation score, alert zones, voice alerts, siren toggle |
| 📉 Analytics      | Monthly/yearly charts, region comparison, heatmap, records table |
| 📡 Sensors        | 10-station status board + coverage pie chart |
| 🔔 Notifications  | Push notification center with dismiss/clear |
| ⚙️ Admin          | System log, ML radar chart, download report & CSV |
| 💬 Seismic AI     | Claude-powered geological intelligence chatbot |

> ⚠️ For demonstration purposes only. Not for use in real emergencies.
