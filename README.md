# Epoch Citizen — Reporting App

Minimal Streamlit app to collect civic incident reports, classify severity, and notify an email recipient.

Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Train the severity model using the provided CSV:

```bash
python train_model.py
```

3. Set SMTP credentials and recipient via environment variables or Streamlit secrets. See `.env.example` for names.

4. Run the app:

```bash
streamlit run app.py
```

Files added
- `app.py`: Streamlit UI and email integration
- `train_model.py`: Script to train a simple severity classifier from `data/emergency_reports.csv`
- `utils.py`: helper functions for loading model and sending email
- `.env.example`: environment variable names for SMTP and recipient

Notes
- The model trained by `train_model.py` is a simple baseline (TF-IDF + RandomForest). Replace or improve as needed.
- For Gmail SMTP you will need an app password or SMTP access credentials.