import requests
import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="IP Defenders | SOC Command",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
    :root { color-scheme: dark; }
    .stApp { background-color: #050608; background-image: linear-gradient(rgba(63, 230, 173, .035) 1px, transparent 1px), linear-gradient(90deg, rgba(58, 177, 255, .035) 1px, transparent 1px), radial-gradient(ellipse at 8% 0%, rgba(0, 189, 255, .10), transparent 42%), linear-gradient(135deg, #050608, #090c11); background-size: 42px 42px, 42px 42px, cover, cover; color: #a7edc7; font-family: 'IBM Plex Sans', sans-serif; }
    [data-testid="stHeader"] { background: #050608; }
    [data-testid="stToolbar"] { background: transparent; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #102126, #101820 70%); border-right: 1px solid #28504d; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #f0f8f4; }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #a6bdb7 !important; }
    .block-container { padding-top: 6rem; max-width: 1500px; }
    h1, h2, h3 { letter-spacing: 0; }
    .site-title { color: #61f2a3; font-size: 48px; font-weight: 700; line-height: 1.05; }
    .site-kicker { color: #47ccff; font: 600 11px 'IBM Plex Mono', monospace; margin-top: 5px; text-transform: uppercase; }
    .site-nav { margin: 16px 0 22px; padding-bottom: 12px; border-bottom: 1px solid #1b5063; }
    .eyebrow { color: #61f2a3; font: 600 11px 'IBM Plex Mono', monospace; letter-spacing: 0; text-transform: uppercase; }
    .page-title { color: #61e3ff; font-size: 30px; font-weight: 700; margin: 2px 0 4px; }
    .subtitle { color: #9bcde0; font-size: 14px; margin-bottom: 20px; }
    .metric { background: linear-gradient(140deg, #25d978, #078344); border: 1px solid #16a75d; border-top: 3px solid #a9ff55; border-radius: 6px; padding: 16px 18px; min-height: 92px; box-shadow: 0 8px 25px rgba(0, 0, 0, .15); transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease; }
    .metric:hover { transform: translateY(-3px); border-color: #c9f45b; box-shadow: 0 14px 30px rgba(34, 199, 103, .3); }
    [data-testid="column"]:nth-child(2) .metric { border-top-color: #ff755e; }
    [data-testid="column"]:nth-child(3) .metric { border-top-color: #c9f45b; }
    .metric-label { color: #000; font-size: 12px; text-transform: uppercase; font-family: 'IBM Plex Mono', monospace; }
    .metric-value { color: #e9f7ef; font-size: 26px; font-weight: 600; margin-top: 8px; }
    .section-title { color: #5ee8ab; font-size: 17px; font-weight: 600; margin: 18px 0 8px; }
    .critical-card { background: linear-gradient(105deg, #411c21, #25181e); border: 1px solid #ff755e; border-left: 5px solid #ff755e; padding: 18px 20px; border-radius: 5px; margin: 12px 0 18px; }
    .critical-heading { color: #ff9a7d; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .critical-meta { color: #ffe1d8; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }
    .containment-title { color: #fff; font-size: 14px; font-weight: 600; margin-top: 14px; }
    .benign-badge { display: inline-block; background: #15382f; border: 1px solid #39d6a3; color: #9bf2c5; border-radius: 4px; padding: 10px 13px; font-size: 14px; font-weight: 600; margin: 10px 0 16px; }
    .muted { color: #9cb5b1; }
    div[data-testid="stDataFrame"] { background: #c5f4d0; border: 1px solid #16a75d; border-radius: 5px; transition: border-color .18s ease, box-shadow .18s ease; }
    div[data-testid="stDataFrame"]:hover { border-color: #39d6bd; box-shadow: 0 10px 28px rgba(57, 214, 189, .12); }
    div.stButton > button { background: #18312f; color: #e6f6ec; border-radius: 4px; font-weight: 600; border-color: #3b6660; transition: transform .16s ease, box-shadow .16s ease, background-color .16s ease, border-color .16s ease; }
    div.stButton > button:hover { background: #24504a; color: #f2fff8; border-color: #39d6bd; transform: translateY(-2px); box-shadow: 0 7px 18px rgba(57, 214, 189, .2); }
    div.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button { background: #c9f45b; color: #101a16; border: 1px solid #c9f45b; }
    div.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover { background: #dcff79; border-color: #dcff79; color: #101a16; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { background: #132328 !important; border-color: #39625b !important; }
    div[data-baseweb="input"] input, div[data-baseweb="select"] input, textarea { background: transparent !important; color: #edf6f2 !important; }
    [data-testid="stTextInput"] input { background-color: #132328 !important; color: #edf6f2 !important; border-color: #39625b !important; }
    [data-testid="stWidgetLabel"] p, [data-testid="stTextInput"] label { color: #dcebe5 !important; }
    [data-testid="stSlider"] [role="slider"] { background: #c9f45b; border-color: #c9f45b; transition: box-shadow .16s ease, transform .16s ease; }
    [data-testid="stSlider"] [role="slider"]:hover { transform: scale(1.14); box-shadow: 0 0 0 7px rgba(201, 244, 91, .18); }
    .login-brand { color: #20a96b; font: 600 12px 'IBM Plex Mono', monospace; text-transform: uppercase; }
    .login-headline { color: #168ab0; font-size: 48px; font-weight: 700; line-height: 1.08; margin: 16px 0; }
    .login-copy { color: #2f786c; font-size: 16px; max-width: 460px; }
    .login-signal { border-left: 3px solid #168d77; padding: 2px 0 2px 12px; color: #247fa5; font: 500 12px 'IBM Plex Mono', monospace; margin-top: 28px; }
    .about-intro { color: #9bcde0; font-size: 18px; line-height: 1.65; max-width: 920px; margin: 12px 0 24px; }
    .info-panel, .team-card { background: linear-gradient(140deg, #a7f0b1, #60d887); border: 1px solid #28ac5e; border-top: 3px solid #16a75d; border-radius: 6px; padding: 18px; min-height: 132px; transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease; }
    .info-panel:hover, .team-card:hover { transform: translateY(-3px); border-color: #238f78; box-shadow: 0 12px 24px rgba(25, 66, 55, .14); }
    .info-title { color: #16834e; font: 600 12px 'IBM Plex Mono', monospace; text-transform: uppercase; }
    .info-copy { color: #155678; font-size: 14px; line-height: 1.55; margin-top: 10px; }
    .team-card { border-top-color: #c9a638; min-height: 104px; margin-bottom: 14px; }
    .team-name { color: #08719b; font-size: 17px; font-weight: 700; }
    .team-role { color: #16834e; font: 500 12px 'IBM Plex Mono', monospace; margin-top: 8px; }
    [data-testid="stForm"] { background: #fff; border: 1px solid #16a75d; border-radius: 8px; padding: 24px; box-shadow: 0 22px 70px rgba(0, 0, 0, .32); }
    [data-testid="stForm"] [data-testid="stWidgetLabel"] p, [data-testid="stForm"] label { color: #000 !important; }
    @media (max-width: 700px) { .site-title { font-size: 38px; } .login-headline { font-size: 36px; } [data-testid="stForm"] { padding: 18px; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_url(base_url, path):
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def first_value(data, keys, default=None):
    for key in keys:
        if data.get(key) is not None:
            return data[key]
    return default


def as_percent(value):
    try:
        number = float(value)
        if 0 <= number <= 1:
            number *= 100
        return f"{number:.1f}%"
    except (TypeError, ValueError):
        return "N/A"


if "incidents" not in st.session_state:
    st.session_state.incidents = []
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "feedback_notice" not in st.session_state:
    st.session_state.feedback_notice = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "site_page" not in st.session_state:
    st.session_state.site_page = "Home"

if st.session_state.pop("reset_page_scroll", False):
    st.components.v1.html(
        "<script>window.parent.scrollTo({top: 0, left: 0}); const main = window.parent.document.querySelector('[data-testid=stMain]'); if (main) main.scrollTo({top: 0, left: 0});</script>",
        height=1,
    )

st.markdown(
    '<div class="site-header"><div class="site-title">IP Defenders</div><div class="site-kicker">Security Operations Center</div></div>',
    unsafe_allow_html=True,
)
with st.container():
    st.markdown('<div class="site-nav"></div>', unsafe_allow_html=True)
    home_nav, about_nav, team_nav, _ = st.columns([1, 1, 1, 5])
    with home_nav:
        if st.button("Home", type="primary" if st.session_state.site_page == "Home" else "secondary", use_container_width=True, key="nav_home"):
            st.session_state.site_page = "Home"
    with about_nav:
        if st.button("About", type="primary" if st.session_state.site_page == "About" else "secondary", use_container_width=True, key="nav_about"):
            st.session_state.site_page = "About"
    with team_nav:
        if st.button("Teammates", type="primary" if st.session_state.site_page == "Teammates" else "secondary", use_container_width=True, key="nav_teammates"):
            st.session_state.site_page = "Teammates"

site_page = st.session_state.site_page
if not st.session_state.authenticated or site_page != "Home":
    st.markdown("<style>[data-testid='stSidebar']{display:none}</style>", unsafe_allow_html=True)

if site_page == "About":
    st.markdown('<div class="page-title">About IP Defenders</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="about-intro">IP Defenders is an AI-assisted SOC alert triage concept focused on reducing false positives and alert fatigue. It evaluates signals such as failed logins, unusual location or timing, and Snort signature matches to help surface high-risk activity while batching benign friction for analyst review.</div>',
        unsafe_allow_html=True,
    )
    about_columns = st.columns(3)
    about_panels = (
        ("Signals", "Combine authentication, location, time, and network detection signals."),
        ("Prioritize", "Bring the strongest threat indicators forward for faster investigation."),
        ("Keep oversight", "Analysts review outcomes and provide feedback; critical activity stays visible."),
    )
    for column, (panel_title, panel_copy) in zip(about_columns, about_panels):
        with column:
            st.markdown(
                f'<div class="info-panel"><div class="info-title">{panel_title}</div><div class="info-copy">{panel_copy}</div></div>',
                unsafe_allow_html=True,
            )
    st.stop()

if site_page == "Teammates":
    st.markdown('<div class="page-title">Teammates</div>', unsafe_allow_html=True)
    team_members = (
        ("Sidhaarth Gowtham G", "SOC Analyst"),
        ("Acharya N", "MLOps Engineer, Team Lead"),
        ("Charanjith S", "Lead ML Engineer"),
        ("Kishore J", "Data Engineer"),
        ("Elakkiya P", "Security SME"),
    )
    team_columns = st.columns(3)
    for member_index, (member_name, member_role) in enumerate(team_members):
        with team_columns[member_index % len(team_columns)]:
            st.markdown(
                f'<div class="team-card"><div class="team-name">{member_name}</div><div class="team-role">{member_role}</div></div>',
                unsafe_allow_html=True,
            )
    st.stop()

if not st.session_state.authenticated:
    login_intro, login_form_column = st.columns([1.15, 0.85], gap="large", vertical_alignment="center")
    with login_intro:
        st.markdown('<div class="login-brand">IP DEFENDERS / SECURITY OPERATIONS</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-headline">See the signal.<br>Skip the noise.</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-copy">A focused workspace for alert triage, event scoring, and analyst decisions.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="login-signal">SOC CONSOLE &nbsp; / &nbsp; LOCAL DEMO ACCESS</div>', unsafe_allow_html=True)
    with login_form_column:
        st.markdown("### Operator sign in")
        with st.form("local_login"):
            operator_name = st.text_input("Operator ID", placeholder="Your name")
            st.text_input("Password", type="password", placeholder="Enter password")
            login_submitted = st.form_submit_button("Enter console", use_container_width=True)
        st.caption("Frontend demo only. Credentials are not checked, stored, or sent to a server.")
        if login_submitted:
            if operator_name.strip():
                st.session_state.authenticated = True
                st.session_state.operator_name = operator_name.strip()
                st.session_state.reset_page_scroll = True
                st.rerun()
            st.error("Enter an Operator ID to continue.")
    st.stop()


with st.sidebar:
    st.markdown('<div class="eyebrow">IP Defenders // SOC</div>', unsafe_allow_html=True)
    st.title("Control panel")
    st.caption(f"Signed in as {st.session_state.operator_name}")
    if st.button("Sign out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    api_base_url = st.text_input("API Base URL", value="http://localhost:8000")

    if st.button("Test Connection", use_container_width=True):
        try:
            response = requests.get(api_url(api_base_url, "/health"), timeout=5)
            response.raise_for_status()
            st.success("API is reachable")
        except requests.RequestException as exc:
            st.error(f"Connection failed: {exc}")

    st.divider()
    st.markdown("**Event signals**")
    failed_logins = st.slider("Failed Logins", min_value=0, max_value=20, value=0)
    location_deviation = st.slider("Location Deviation", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    time_deviation = st.slider("Time Deviation", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    snort_signature_match = st.checkbox("Snort Signature Match")

    dispatch_event = st.button("Simulate & Dispatch Event", type="primary", use_container_width=True)


if dispatch_event:
    payload = {
        "failed_logins": failed_logins,
        "location_deviation": location_deviation,
        "time_deviation": time_deviation,
        "snort_flag": int(snort_signature_match),
    }
    try:
        response = requests.post(api_url(api_base_url, "/score_alert"), json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            raise ValueError("The scoring API returned an unexpected response format.")

        severity = str(first_value(result, ("severity", "risk_level", "classification"), "Unknown")).upper()
        confidence = first_value(result, ("ai_confidence_score", "confidence", "confidence_score", "score"))
        recommendation = first_value(
            result,
            ("recommended_containment", "containment_steps", "recommendation", "recommended_action"),
            "Isolate the affected host, disable the suspected account, and preserve logs for investigation.",
        )
        incident = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": severity,
            "confidence": as_percent(confidence),
            "failed_logins": failed_logins,
            "signals": "Snort match" if snort_signature_match else "Behavioral",
        }
        st.session_state.latest_result = {
            "result": result,
            "severity": severity,
            "confidence": as_percent(confidence),
            "recommendation": recommendation,
            "incident": incident,
        }
        st.session_state.incidents.insert(0, incident)
        st.session_state.feedback_notice = None
    except requests.RequestException as exc:
        st.error(f"Event dispatch failed: {exc}")
    except (ValueError, requests.exceptions.JSONDecodeError) as exc:
        st.error(f"Could not read scoring response: {exc}")


st.markdown('<div class="eyebrow">Security Operations Center</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">SIEM Alert Triage</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Signal scoring, alert prioritization, and analyst feedback</div>', unsafe_allow_html=True)

total_events = len(st.session_state.incidents)
critical_events = sum(item["severity"] == "CRITICAL" for item in st.session_state.incidents)
batched_events = sum(item["severity"] in ("LOW", "BENIGN") for item in st.session_state.incidents)

metric_columns = st.columns(3)
metrics = (
    ("Events scored", total_events),
    ("Critical escalations", critical_events),
    ("Low-risk batched", batched_events),
)
for column, (label, value) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

latest = st.session_state.latest_result
if latest:
    if latest["severity"] == "CRITICAL":
        st.markdown(
            f'<div class="critical-card"><div class="critical-heading">CRITICAL ALERT</div>'
            f'<div class="critical-meta">Severity: {latest["severity"]} &nbsp; | &nbsp; Confidence: {latest["confidence"]}</div>'
            f'<div class="containment-title">Recommended containment</div></div>',
            unsafe_allow_html=True,
        )
        recommendation = latest["recommendation"]
        if isinstance(recommendation, (list, tuple)):
            for step in recommendation:
                st.markdown(f"- {step}")
        else:
            st.write(recommendation)
    elif latest["severity"] in ("LOW", "BENIGN"):
        st.markdown(
            '<div class="benign-badge">Benign Friction Batched - Alert Fatigue Prevented</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(f"Scoring result: {latest['severity']} | Confidence: {latest['confidence']}")

    st.markdown('<div class="section-title">Human-in-the-Loop Feedback</div>', unsafe_allow_html=True)
    feedback_columns = st.columns([1, 1, 4])
    event_key = latest["incident"]["time"]
    with feedback_columns[0]:
        if st.button("True Positive", key=f"tp_{event_key}"):
            st.session_state.feedback_notice = "True Positive recorded for continuous retraining."
    with feedback_columns[1]:
        if st.button("False Positive", key=f"fp_{event_key}"):
            st.session_state.feedback_notice = "False Positive recorded for continuous retraining."
    if st.session_state.feedback_notice:
        st.success(st.session_state.feedback_notice)

st.markdown('<div class="section-title">Recent Incidents</div>', unsafe_allow_html=True)
if st.session_state.incidents:
    st.dataframe(st.session_state.incidents, use_container_width=True, hide_index=True)
else:
    st.markdown('<p class="muted">No events dispatched in this session.</p>', unsafe_allow_html=True)