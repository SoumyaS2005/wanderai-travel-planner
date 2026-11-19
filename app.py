
import streamlit as st
from agent import plan_trip

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="WanderAI | Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
    .stApp {
        background: #f7f9fc;
        color: #172b4d;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 1050px;
        padding: 2rem 2rem 3rem;
    }

    /* Navigation */
    .brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #12345a;
        padding-bottom: 1.5rem;
    }

    .brand span {
        color: #078b83;
    }

    /* Hero */
    .hero {
        background: linear-gradient(120deg, #12345a, #087e8b);
        padding: 2.3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(1.8rem, 4vw, 2.7rem);
        line-height: 1.2;
        margin: 0 0 0.8rem 0;
        letter-spacing: -1px;
    }

    .hero p {
        color: #e5f5f7 !important;
        font-size: 1.05rem;
        margin: 0;
        line-height: 1.7;
    }

    .hero-tag {
        display: inline-block;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 30px;
        padding: 0.35rem 0.8rem;
        font-size: 0.82rem;
        margin-bottom: 1rem;
        color: white;
    }

    /* Section headings */
    h2, h3 {
        color: #12345a !important;
    }

    .section-subtitle {
        color: #64748b;
        margin-top: -0.6rem;
        margin-bottom: 1.3rem;
        font-size: 0.95rem;
    }

    /* Form card */
    [data-testid="stForm"] {
        background: #ffffff;
        padding: 1.6rem;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        box-shadow: 0 5px 20px rgba(25, 50, 80, 0.04);
    }

    /* Readable form labels */
    [data-testid="stWidgetLabel"] p {
        color: #243b53 !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
    }

    /* Input fields */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #172b4d !important;
        -webkit-text-fill-color: #172b4d !important;
        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* Primary button */
    div.stFormSubmitButton > button {
        background: #087e8b !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        min-height: 3rem;
        font-weight: 700;
        transition: background 0.2s ease;
    }

    div.stFormSubmitButton > button:hover {
        background: #066570 !important;
        color: white !important;
    }

    /* Results */
    .result-note {
        background: #e9f7f5;
        border-left: 4px solid #078b83;
        padding: 0.9rem 1rem;
        border-radius: 7px;
        color: #245b59;
        margin: 0.8rem 0 1.4rem;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
        padding-top: 1.3rem;
        text-align: center;
        color: #64748b;
        font-size: 0.88rem;
    }

    /* Mobile spacing */
    @media (max-width: 640px) {
        .main .block-container {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 1.5rem;
            border-radius: 14px;
        }

        [data-testid="stForm"] {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# NAVIGATION / BRAND
# =====================================

st.markdown(
    '<div class="brand">✈️ Wander<span>AI</span></div>',
    unsafe_allow_html=True
)

# =====================================
# HERO SECTION
# =====================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">YOUR PERSONAL AI TRAVEL ASSISTANT</div>
    <h1>Your next adventure starts here.</h1>
    <p>
        Tell us where you want to go, set your budget,
        and discover a trip tailored to you.
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================
# TRIP FORM
# =====================================

st.subheader("Plan your trip")
st.markdown(
    '<div class="section-subtitle">'
    'Personalize your journey in a few simple steps.'
    '</div>',
    unsafe_allow_html=True
)

with st.form("travel_form"):
    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Goa, Manali, Jaipur"
        )

        days = st.number_input(
            "Duration (days)",
            min_value=1,
            max_value=60,
            value=3,
            step=1
        )

    with col2:
        budget = st.number_input(
            "Total budget (₹)",
            min_value=1,
            value=8000,
            step=500
        )

        interests = st.text_input(
            "Interests",
            placeholder="e.g. food, beaches, nature"
        )

    submitted = st.form_submit_button(
        "✦  Create my travel plan",
        use_container_width=True
    )

# =====================================
# GENERATE THE ITINERARY
# =====================================

if submitted:
    if not destination.strip():
        st.error("Please enter your destination.")
    else:
        with st.spinner(
            "Preparing your personalized travel plan..."
        ):
            try:
                itinerary = plan_trip(
                    destination=destination.strip(),
                    days=int(days),
                    budget=float(budget),
                    interests=interests.strip()
                    or "General sightseeing and local food"
                )

                st.session_state["itinerary"] = itinerary
                st.session_state["destination"] = destination.strip()

            except Exception as error:
                st.error("We couldn't create your travel plan.")
                st.caption(f"Details: {error}")

# =====================================
# DISPLAY RESULTS
# =====================================

if "itinerary" in st.session_state:
    st.divider()

    destination_name = st.session_state.get(
        "destination", "your destination"
    )

    st.subheader(f"Your itinerary: {destination_name}")

    st.markdown("""
    <div class="result-note">
        Travel suggestions are AI-generated. Prices,
        opening hours and availability have not been
        independently verified.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(st.session_state["itinerary"])

    if st.button("Plan another trip"):
        st.session_state.pop("itinerary", None)
        st.session_state.pop("destination", None)
        st.rerun()

# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class="footer">
    WanderAI &nbsp;·&nbsp; Built with Python and Gemini AI
</div>
""", unsafe_allow_html=True)
