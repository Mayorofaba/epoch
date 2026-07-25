import os
import streamlit as st
import pandas as pd
import plotly.express as px
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


def apply_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f5f7ff 0%, #fff7f0 100%);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .section-header {
            background: linear-gradient(135deg, #4f46e5, #2563eb, #38bdf8);
            color: #ffffff;
            padding: 24px 28px;
            border-radius: 24px;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.12);
            margin-bottom: 1rem;
        }
        .section-header h1 {
            margin: 0;
            font-size: 2.6rem;
            letter-spacing: -0.04em;
        }
        .section-header p {
            margin: 0.4rem 0 0;
            color: rgba(255, 255, 255, 0.88);
            font-size: 1rem;
        }
        .report-box {
            background: linear-gradient(90deg, #eef6ff, #f0f9ff);
            padding: 24px;
            border-radius: 22px;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
        }
        .submit-btn > button {
            background: #0b5cff !important;
            color: white !important;
            border-radius: 14px !important;
            padding: 12px 18px !important;
            font-weight: 700;
        }
        .submit-btn > button:hover {
            background: #2563eb !important;
        }
        .metric-card, .metric-card-alt {
            border-radius: 20px;
            padding: 20px;
            color: white;
            box-shadow: 0 15px 35px rgba(15, 23, 42, 0.12);
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9);
        }
        .metric-card-alt {
            background: linear-gradient(135deg, #f43f5e, #fb7185);
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>div>div, .stTextArea>div>div>textarea {
            border-radius: 14px;
            border: 1px solid rgba(96, 165, 250, 0.45);
        }
        .stFileUploader>div>div {
            border-radius: 14px;
        }
        .status-heading {
            color: #0b5cff;
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            padding: 18px 22px;
            border-radius: 24px;
            display: inline-block;
            box-shadow: 0 20px 35px rgba(59, 130, 246, 0.12);
            margin-bottom: 1rem;
            font-size: 1.8rem;
            font-weight: 700;
        }
        .stButton>button {
            background: linear-gradient(135deg, #0b5cff, #22d3ee) !important;
            color: white !important;
            border-radius: 16px !important;
            padding: 0.9rem 1.4rem !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 16px 30px rgba(15, 23, 42, 0.16) !important;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #2563eb, #38bdf8) !important;
        }
        .stButton>button:active {
            transform: translateY(1px);
        }
        .summary-card {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            padding: 20px;
            margin-bottom: 1.5rem;
        }
        .summary-card div {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 20px;
            padding: 18px;
            box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08);
            text-align: center;
        }
        .summary-card strong {
            display: block;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
            color: #0f172a;
        }
        .summary-card span {
            display: block;
            font-size: 2rem;
            font-weight: 700;
            color: #0b5cff;
        }
        .severity-card-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 1rem 0 1.5rem;
        }
        .severity-card {
            flex: 1 1 180px;
            min-width: 180px;
            border-radius: 20px;
            padding: 20px;
            color: white;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.14);
            font-weight: 600;
        }
        .severity-card span {
            display: block;
            margin-top: 0.65rem;
            font-size: 2rem;
            font-weight: 800;
        }
        .severity-card.critical { background: linear-gradient(135deg, #dc2626, #f43f5e); }
        .severity-card.high { background: linear-gradient(135deg, #f97316, #fb923c); }
        .severity-card.medium { background: linear-gradient(135deg, #facc15, #eab308); color: #111827; }
        .severity-card.low { background: linear-gradient(135deg, #22c55e, #4ade80); }
        .severity-card.unknown { background: linear-gradient(135deg, #6b7280, #9ca3af); }
        .plotly-graph {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 24px;
            padding: 18px;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.1);
            margin-bottom: 1.5rem;
        }
        .plotly-graph h4 {
            margin: 0 0 0.75rem;
            font-size: 1.2rem;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


NIGERIA_COUNTRY = "Nigeria"
NIGERIA_STATES = [
    "Abia",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara",
    "FCT",
]

NIGERIA_STATE_LGAS = {
    "Abia": [
        "Aba North",
        "Aba South",
        "Arochukwu",
        "Bende",
        "Ikwuano",
        "Isiala Ngwa North",
        "Isiala Ngwa South",
        "Isuikwuato",
        "Obi Ngwa",
        "Ohafia",
        "Osisioma Ngwa",
        "Ugwunagbo",
        "Ukwa East",
        "Ukwa West",
        "Umuahia North",
        "Umuahia South",
        "Umu Nneochi",
    ],
    "Adamawa": ["Yola South", "Girei"],
    "Akwa Ibom": ["Uyo", "Eket"],
    "Anambra": ["Onitsha South", "Awka North"],
    "Bauchi": ["Darazo", "Ningi"],
    "Bayelsa": ["Yenagoa", "Sagbama"],
    "Benue": ["Makurdi", "Gboko"],
    "Borno": ["Maiduguri Metropolitan", "Chibok"],
    "Cross River": ["Calabar Municipal", "Ikom"],
    "Delta": ["Ughelli North", "Warri South"],
    "Ebonyi": ["Abakaliki North", "Ikwo"],
    "Edo": ["Oredo", "Uhunmwonde"],
    "Ekiti": ["Ado Ekiti North", "Ikere"],
    "Enugu": ["Enugu North", "Nsukka"],
    "Gombe": ["Akko", "Dukku"],
    "Imo": ["Owerri Municipal", "Orlu"],
    "Jigawa": ["Dutse", "Hadejia"],
    "Kaduna": ["Chikun", "Zaria"],
    "Kano": ["Nassarawa", "Tarauni"],
    "Katsina": ["Funtua", "Kankia"],
    "Kebbi": ["Birnin Kebbi", "Argungu"],
    "Kogi": ["Lokoja", "Idah"],
    "Kwara": ["Ilorin East", "Offa"],
    "Lagos": ["Ikeja", "Alimosho"],
    "Nasarawa": ["Karu", "Akwanga"],
    "Niger": ["Minna", "Suleja"],
    "Ogun": ["Abeokuta North", "Ifo"],
    "Ondo": ["Akure South", "Owo"],
    "Osun": ["Osogbo", "Ife North"],
    "Oyo": ["Ibadan North", "Ogbomosho North"],
    "Plateau": ["Jos North", "Bokkos"],
    "Rivers": ["Port Harcourt City", "Obio/Akpor"],
    "Sokoto": ["Sokoto North", "Binji"],
    "Taraba": ["Jalingo", "Wukari"],
    "Yobe": ["Damaturu", "Potiskum"],
    "Zamfara": ["Gusau", "Tsafe"],
    "FCT": ["Abuja Municipal", "Gwagwalada"],
}

NIGERIA_LGA_TOWNS = {
    ("Abia", "Aba North"): ["Eziama", "Osusu", "Ogbor Hill", "Umuola", "Ehere"],
    ("Abia", "Aba South"): ["Asaokpuaja", "Abariba", "Ohanku", "Ndiegoro", "Eziukwu"],
    ("Abia", "Arochukwu"): ["Arochukwu Town", "Ibom", "Ututu", "Ihechiowa", "Isu"],
    ("Abia", "Bende"): ["Bende Town", "Alayi", "Igbere", "Item", "Nkpa", "Ugwueke"],
    ("Abia", "Ikwuano"): ["Ariam", "Ibere", "Oboro", "Oloko"],
    ("Abia", "Isiala Ngwa North"): ["Isialangwa", "Ameke", "Uturu", "Okpuala Ngwa"],
    ("Abia", "Isiala Ngwa South"): ["Nvosi", "Ovu-Ngwa", "Ovu-Okwu", "Mbutu", "Okpuisiala"],
    ("Abia", "Isuikwuato"): ["Uturu", "Isuikwuato Town", "Achara-Uturu", "Ezere", "Umuasua"],
    ("Abia", "Obi Ngwa"): ["Obohia", "Ohuru", "Azumini", "Itumbuzo", "Amuzu"],
    ("Abia", "Ohafia"): ["Elu", "Ebem", "Akanu", "Asaga", "Nde Okoro"],
    ("Abia", "Osisioma Ngwa"): ["Osisioma", "Amator", "Umuimo", "Abayi"],
    ("Abia", "Ugwunagbo"): ["Ugwunagbo", "Warduma", "Obegu", "Umugo"],
    ("Abia", "Ukwa East"): ["Akwete", "Azumini", "Ohandu", "Ohambele"],
    ("Abia", "Ukwa West"): ["Oke-Ikpe", "Obingwu", "Omuma-Uzor", "Asa"],
    ("Abia", "Umuahia North"): ["Umuahia Town", "Nkwoegwu", "Ofeme", "Isingwu"],
    ("Abia", "Umuahia South"): ["Ubakala", "Amakama", "Nsirimo", "Old Umuahia"],
    ("Abia", "Umu Nneochi"): ["Nneochi", "Ubahu", "Leru", "Lomta", "Amuda"],
    ("Adamawa", "Yola South"): ["Yola"],
    ("Adamawa", "Girei"): ["Girei"],
    ("Akwa Ibom", "Uyo"): ["Uyo"],
    ("Akwa Ibom", "Eket"): ["Eket"],
    ("Anambra", "Onitsha South"): ["Onitsha"],
    ("Anambra", "Awka North"): ["Awka"],
    ("Bauchi", "Darazo"): ["Darazo"],
    ("Bauchi", "Ningi"): ["Ningi"],
    ("Bayelsa", "Yenagoa"): ["Yenagoa"],
    ("Bayelsa", "Sagbama"): ["Sagbama"],
    ("Benue", "Makurdi"): ["Makurdi"],
    ("Benue", "Gboko"): ["Gboko"],
    ("Borno", "Maiduguri Metropolitan"): ["Maiduguri"],
    ("Borno", "Chibok"): ["Chibok"],
    ("Cross River", "Calabar Municipal"): ["Calabar"],
    ("Cross River", "Ikom"): ["Ikom"],
    ("Delta", "Ughelli North"): ["Ughelli"],
    ("Delta", "Warri South"): ["Warri"],
    ("Ebonyi", "Abakaliki North"): ["Abakaliki"],
    ("Ebonyi", "Ikwo"): ["Ikwo"],
    ("Edo", "Oredo"): ["Benin City"],
    ("Edo", "Uhunmwonde"): ["Uromi"],
    ("Ekiti", "Ado Ekiti North"): ["Ado Ekiti"],
    ("Ekiti", "Ikere"): ["Ikere"],
    ("Enugu", "Enugu North"): ["Enugu"],
    ("Enugu", "Nsukka"): ["Nsukka"],
    ("Gombe", "Akko"): ["Gombe"],
    ("Gombe", "Dukku"): ["Dukku"],
    ("Imo", "Owerri Municipal"): ["Owerri"],
    ("Imo", "Orlu"): ["Orlu"],
    ("Jigawa", "Dutse"): ["Dutse"],
    ("Jigawa", "Hadejia"): ["Hadejia"],
    ("Kaduna", "Chikun"): ["Kaduna"],
    ("Kaduna", "Zaria"): ["Zaria"],
    ("Kano", "Nassarawa"): ["Kano"],
    ("Kano", "Tarauni"): ["Kano"],
    ("Katsina", "Funtua"): ["Funtua"],
    ("Katsina", "Kankia"): ["Kankia"],
    ("Kebbi", "Birnin Kebbi"): ["Birnin Kebbi"],
    ("Kebbi", "Argungu"): ["Argungu"],
    ("Kogi", "Lokoja"): ["Lokoja"],
    ("Kogi", "Idah"): ["Idah"],
    ("Kwara", "Ilorin East"): ["Ilorin"],
    ("Kwara", "Offa"): ["Offa"],
    ("Lagos", "Ikeja"): ["Ikeja"],
    ("Lagos", "Alimosho"): ["Ikeja"],
    ("Nasarawa", "Karu"): ["Mararaba"],
    ("Nasarawa", "Akwanga"): ["Akwanga"],
    ("Niger", "Minna"): ["Minna"],
    ("Niger", "Suleja"): ["Suleja"],
    ("Ogun", "Abeokuta North"): ["Abeokuta"],
    ("Ogun", "Ifo"): ["Ifo"],
    ("Ondo", "Akure South"): ["Akure"],
    ("Ondo", "Owo"): ["Owo"],
    ("Osun", "Osogbo"): ["Osogbo"],
    ("Osun", "Ife North"): ["Ile-Ife"],
    ("Oyo", "Ibadan North"): ["Ibadan"],
    ("Oyo", "Ogbomosho North"): ["Ogbomosho"],
    ("Plateau", "Jos North"): ["Jos"],
    ("Plateau", "Bokkos"): ["Bokkos"],
    ("Rivers", "Port Harcourt City"): ["Port Harcourt"],
    ("Rivers", "Obio/Akpor"): ["Rumuokoro"],
    ("Sokoto", "Sokoto North"): ["Sokoto"],
    ("Sokoto", "Binji"): ["Binji"],
    ("Taraba", "Jalingo"): ["Jalingo"],
    ("Taraba", "Wukari"): ["Wukari"],
    ("Yobe", "Damaturu"): ["Damaturu"],
    ("Yobe", "Potiskum"): ["Potiskum"],
    ("Zamfara", "Gusau"): ["Gusau"],
    ("Zamfara", "Tsafe"): ["Tsafe"],
    ("FCT", "Abuja Municipal"): ["Abuja"],
    ("FCT", "Gwagwalada"): ["Gwagwalada"],
}


def load_reports():
    base = os.path.dirname(__file__)
    data_path = os.path.join(base, "data", "emergency_reports.csv")
    expected_columns = [
        "ReportID",
        "Description",
        "Location",
        "DateTime",
        "Category",
        "Severity",
        "ReporterName",
        "ReporterContact",
        "Latitude",
        "Longitude",
        "ImageURL",
        "ResponseStatus",
        "Country",
        "State",
        "LocalGovernment",
        "Town",
    ]

    if not os.path.exists(data_path):
        st.warning("Report dataset not found. Run the app from the project root.")
        return pd.DataFrame(columns=expected_columns)

    df = pd.read_csv(data_path, dtype=str, keep_default_na=False, na_filter=False)
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""
    df = df[expected_columns]
    return df


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

    smtp_host = os.environ.get("SMTP_HOST") or st.secrets.get("SMTP_HOST")
    smtp_port = os.environ.get("SMTP_PORT") or st.secrets.get("SMTP_PORT")
    smtp_user = os.environ.get("SMTP_USER") or st.secrets.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD") or st.secrets.get("SMTP_PASSWORD")

    try:
        send_email_smtp(
            subject=subject,
            body=body,
            recipient=recipient,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
        )
        return True, f"Email sent to {recipient}"
    except Exception as e:
        return False, str(e)


def get_location_options(column: str, filters: dict, reports: pd.DataFrame):
    location_df = reports.copy()
    for key, value in filters.items():
        if value:
            location_df = location_df[location_df[key] == value]
    values = location_df[column].astype(str)
    values = values[values != ""]
    return sorted(values.unique())


def file_report_page():
    st.markdown("""
    <style>
    .report-box {background:linear-gradient(90deg,#eef6ff,#f0f9ff); padding:24px; border-radius:22px;}
    .submit-btn {background:#0b5cff;color:white}
    .submit-btn > button {width:100%;}
    .field-section {background: rgba(255,255,255,0.90); padding: 20px; border-radius: 18px;}
    .section-note {font-size: 0.95rem; color: #475569; margin-bottom: 1rem;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class='report-box'>
            <h2>File a report</h2>
            <p class='section-note'>Use this form to submit incident details, and our dataset will update with your report.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Place location selectors outside the form so town options update immediately
    country = st.selectbox("Country", [NIGERIA_COUNTRY])
    state = st.selectbox("State", NIGERIA_STATES)
    local_government = st.selectbox("Local Government", NIGERIA_STATE_LGAS.get(state, []))
    town_options = NIGERIA_LGA_TOWNS.get((state, local_government), []) if local_government else []
    if not town_options:
        town_options = ["Select Local Government"]
    town = st.selectbox("Town / City", town_options, key=f"town_{state}_{local_government}")

    with st.form("report_form"):
        c1, c2 = st.columns([2,1])
        with c1:
            st.markdown("<div class='field-section'>", unsafe_allow_html=True)
            reporter_name = st.text_input("Your name", placeholder="Full name")
            reporter_age = st.number_input("Your age", min_value=0, max_value=120, value=30)
            reporter_contact = st.text_input("Contact phone or WhatsApp")
            reporter_email = st.text_input("Your email (optional)")
            location = st.text_input("Location (address or description)")
            category = st.selectbox(
                "Category",
                [
                    "Flooding",
                    "Power Outage",
                    "Water Supply",
                    "Road Damage",
                    "Waste Management",
                    "Public Safety",
                    "Theft",
                    "Robbery",
                    "Burglary",
                    "Assault",
                    "Kidnapping",
                    "Homicide",
                    "Road Traffic Accident",
                    "Cultism",
                ],
            )
            description = st.text_area("Describe the situation", height=150)
            image = st.file_uploader("Upload image (optional)", type=["png", "jpg", "jpeg"])
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(
                """
                <div class='field-section'>
                    <h3>Preview & Actions</h3>
                    <p class='section-note'>Provide accurate details to help classification and response.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
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
            "Country": country,
            "State": state,
            "LocalGovernment": local_government,
            "Town": town,
        }

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


def location_status_page():
    st.markdown("<div class='status-heading'>Get location crime status</div>", unsafe_allow_html=True)
    st.write(
        "Enter a location using data from the report dataset to see the most common incident categories and their relative frequency."
    )

    reports = load_reports()
    valid_reports = reports[reports["Country"] != ""]

    if valid_reports.empty:
        st.warning("No location data is available yet. Submit reports or update the dataset with Country, State, LocalGovernment, and Town fields.")
        return

# Place selectors outside the form so town options react immediately
    country = st.selectbox("Country", [NIGERIA_COUNTRY])
    state = st.selectbox("State", NIGERIA_STATES)
    local_gov = st.selectbox("Local Government", NIGERIA_STATE_LGAS.get(state, []))
    town_options = NIGERIA_LGA_TOWNS.get((state, local_gov), []) if local_gov else []
    if not town_options:
        town_options = ["Select Local Government"]
    town = st.selectbox("Town / City", town_options, key=f"loc_town_{state}_{local_gov}")
    submit = st.button("Show location crime status")

    if not submit:
        return

    filtered = valid_reports[
        (valid_reports["Country"] == country)
        & (valid_reports["State"] == state)
        & (valid_reports["LocalGovernment"] == local_gov)
        & (valid_reports["Town"] == town)
    ]

    if filtered.empty:
        st.warning(
            "No reports were found for that exact location. Try a broader location or update the dataset with more location details."
        )
        return

    category_counts = filtered["Category"].value_counts()
    severity_counts = filtered["Severity"].value_counts()

    severity_colors = {
        "Critical": "#dc2626",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low": "#16a34a",
        "Unknown": "#6b7280",
    }

    severity_cards = [
        f"<div class='severity-card {severity.lower()}'><div>{severity}</div><span>{count}</span></div>"
        for severity, count in severity_counts.items()
    ]
    st.markdown(
        f"<div class='severity-card-row'>{''.join(severity_cards)}</div>",
        unsafe_allow_html=True,
    )

    category_df = category_counts.reset_index()
    category_df.columns = ["Category", "Count"]
    fig_category = px.bar(
        category_df,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={"Count": "Reports", "Category": "Incident type"},
    )
    fig_category.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-45,
        margin=dict(l=0, r=0, t=30, b=30),
    )

    severity_df = severity_counts.reset_index()
    severity_df.columns = ["Severity", "Count"]
    fig_severity = px.bar(
        severity_df,
        x="Severity",
        y="Count",
        color="Severity",
        color_discrete_map=severity_colors,
        category_orders={"Severity": ["Critical", "High", "Medium", "Low", "Unknown"]},
        labels={"Count": "Reports", "Severity": "Severity level"},
    )
    fig_severity.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=30),
    )

    st.markdown("<div class='plotly-graph'><h4>Incident frequency by category</h4></div>", unsafe_allow_html=True)
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown("<div class='plotly-graph'><h4>Severity level distribution</h4></div>", unsafe_allow_html=True)
    st.plotly_chart(fig_severity, use_container_width=True)

    top_category = category_counts.idxmax()
    top_count = int(category_counts.max())
    lowest_category = category_counts.idxmin()
    lowest_count = int(category_counts.min())
    total_reports = len(filtered)

    st.markdown(
        f"**Summary for {town}, {local_gov}, {state}, {country}:**"
    )
    st.write(f"- Total reports in this location: **{total_reports}**")
    st.write(
        f"- The most common incident type is **{top_category}** with **{top_count}** report(s)."
    )
    st.write(
        f"- The least common incident type is **{lowest_category}** with **{lowest_count}** report(s)."
    )

    if "Critical" in severity_counts.index:
        st.write(
            f"- There are **{int(severity_counts['Critical'])}** critical reports in this area."
        )

    st.markdown("---")
    st.subheader("Location incident details")
    st.dataframe(
        filtered[
            ["DateTime", "Category", "Severity", "Location", "ReporterName", "ReporterContact"]
        ].sort_values(by="DateTime", ascending=False),
        use_container_width=True,
    )


def build_ui():
    apply_styles()
    reports = load_reports()
    total_reports = len(reports)
    abia_reports = len(reports[reports["State"] == "Abia"])
    categories = reports["Category"].value_counts()
    top_category = categories.index[0] if not categories.empty else "None"

    st.markdown(
        """
        <div class='section-header'>
            <h1>Epoch Citizen</h1>
            <p>Submit incident reports and explore local safety trends across Nigerian communities.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Use the cards below to file a report or lookup location crime status with our dataset. The form is interactive and updates instantly for Abia local governments and towns."
    )

    st.markdown(
        f"""
        <div class='summary-card'>
            <div>
                <strong>Total Reports</strong><br />
                <span>{total_reports}</span>
            </div>
            <div>
                <strong>Abia Reports</strong><br />
                <span>{abia_reports}</span>
            </div>
            <div>
                <strong>Top category</strong><br />
                <span>{top_category}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    card1 = st.columns(1)[0]
    card1.markdown(
        """
        <div class='metric-card'>
            <h3>Report quickly</h3>
            <p>Submit incidents across any town or local government with location-aware dropdowns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if "section" not in st.session_state:
        st.session_state.section = "file_report"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("File a report", key="btn_file_report"):
            st.session_state.section = "file_report"
    with col2:
        if st.button("Get location crime status", key="btn_location_status"):
            st.session_state.section = "location_status"

    st.markdown("---")

    if st.session_state.section == "location_status":
        location_status_page()
    else:
        file_report_page()


if __name__ == "__main__":
    build_ui()
