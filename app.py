import os
import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_pipeline, send_email_smtp


st.set_page_config(page_title="Epoch Citizen — Report an Issue", layout="wide")


@st.cache_resource
def get_model():
    try:
        return load_pipeline()
    except Exception as e:
        st.warning("Model not found. Run `python train_model.py` to create a model.")
        return None


pipeline = get_model()


def append_report(row: dict):
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, "data", "emergency_reports.csv")
    df = pd.DataFrame([row])
    header = not os.path.exists(data_path)
    df.to_csv(data_path, mode="a", index=False, header=header)


def send_notification(report: dict, severity: str):
    recipient = os.environ.get("RECIPIENT_EMAIL") or st.secrets.get("RECIPIENT_EMAIL", None) or "f26202641@gmail.com"
    subject = f"New Report — Severity: {severity} — {report.get('Category')}"

    body_lines = [
        f"Report ID: {report.get('ReportID', '')}",
        f"Reporter: {report.get('ReporterName')} ({report.get('ReporterContact')})",
        f"Location: {report.get('Location')}",
        f"Time: {report.get('DateTime')}",
        f"Category: {report.get('Category')}",
        f"Severity: {severity}",
        "",
        "Description:",
        report.get('Description', ''),
    ]
    body = "\n".join(body_lines)

    try:
        send_email_smtp(subject=subject, body=body, recipient=recipient)
        return True, f"Email sent to {recipient}"
    except Exception as e:
        return False, str(e)


def build_ui():
    st.markdown("""
    <style>
    .report-box {background:linear-gradient(90deg,#f7fbff,#eef6ff); padding:20px; border-radius:12px}
    .submit-btn {background:#0b5cff;color:white}
    </style>
    """, unsafe_allow_html=True)

    st.title("Epoch Citizen — Report an Issue")
    st.write("Help us prioritize civic responses by reporting incidents with details.")

    with st.form("report_form"):
        c1, c2 = st.columns([2,1])
        with c1:
            reporter_name = st.text_input("Your name", placeholder="Full name")
            reporter_age = st.number_input("Your age", min_value=0, max_value=120, value=30)
            reporter_contact = st.text_input("Contact phone or WhatsApp")
            reporter_email = st.text_input("Your email (optional)")
            location = st.text_input("Location (address or description)")
            category = st.selectbox("Category", ["Flooding","Power Outage","Water Supply","Road Damage","Waste Management","Public Safety","Other"]) 
            description = st.text_area("Describe the situation", height=150)
            image = st.file_uploader("Upload image (optional)", type=["png","jpg","jpeg"])
        with c2:
            st.markdown("### Preview & Actions")
            st.write("Provide accurate details to help classification and response.")
            submit = st.form_submit_button("Submit Report")

    if submit:
        now = datetime.utcnow().isoformat()
        report_id = f"RPT{int(datetime.utcnow().timestamp())}"
        row = {
            "ReportID": report_id,
            "Description": description,
            "Location": location,
            "DateTime": now,
            "Category": category,
            "ReporterName": reporter_name,
            "ReporterContact": reporter_contact or reporter_email,
            "Latitude": "",
            "Longitude": "",
            "ImageURL": "",
            "ResponseStatus": "pending",
        }

        # predict severity
        if pipeline is not None:
            text = category + " -- " + description
            try:
                severity = pipeline.predict([text])[0]
            except Exception:
                severity = "Unknown"
        else:
            severity = "Unknown"

        row["Severity"] = severity
        append_report(row)

        st.success(f"Report submitted. Predicted severity: {severity}")

        sent, msg = send_notification(row, severity)
        if sent:
            st.info(msg)
        else:
            st.error(f"Failed to send email: {msg}")


if __name__ == "__main__":
    build_ui()
