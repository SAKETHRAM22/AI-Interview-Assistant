"""Visual system for the AI Interview Studio Streamlit application."""


def inject_styles(st) -> None:
    """Apply the app's navy SaaS interface and responsive component styles."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root { --navy:#071426; --navy-2:#0d203b; --ink:#10213d; --muted:#6d7e96; --blue:#5278ff; --cyan:#48d6f0; --line:#dfe7f2; --paper:#ffffff; }
        html, body, [class*="css"] { font-family:Manrope,sans-serif; }
        .stApp { background:radial-gradient(circle at 89% 4%,#dae8ff 0,transparent 24rem),radial-gradient(circle at 7% 37%,#e9f8ff 0,transparent 23rem),#f8fbff; color:var(--ink); }
        #MainMenu, footer { visibility:hidden; }
        .block-container { max-width:1240px; padding:2.4rem 2.2rem 4.5rem; }
        [data-testid="stSidebar"] { background:linear-gradient(160deg,#071426,#0b1f3c); border-right:1px solid #193150; }
        [data-testid="stSidebar"] * { color:#f0f6ff !important; }
        [data-testid="stSidebar"] .stRadio label { padding:.38rem .15rem; font-size:.82rem; font-weight:700; }
        .brand { display:flex; align-items:center; gap:11px; margin:5px 0 28px; }
        .brand-mark { display:grid; place-items:center; width:38px; height:38px; border-radius:12px; color:white!important; font-size:12px; font-weight:800; background:linear-gradient(135deg,#6686ff,#45d5ed); box-shadow:0 8px 18px #0005; }
        .brand-title { font-weight:800; letter-spacing:-.45px; font-size:15px; }
        .brand-subtitle,.side-label { color:#9db3d6!important; font-size:10px; letter-spacing:.12em; text-transform:uppercase; }
        .side-label { margin:25px 0 9px; font-weight:800; }
        .system-card { display:flex; gap:9px; align-items:flex-start; padding:9px 0; border-bottom:1px solid #ffffff12; }
        .system-icon { color:#6bcdf5!important; width:17px; text-align:center; padding-top:1px; }
        .system-card b { display:block; font-size:11px; }
        .system-card small { display:block; color:#a7b9d6!important; font-size:10px; line-height:1.4; overflow-wrap:anywhere; }
        .ready-badge { display:inline-block; margin:18px 0 9px; padding:6px 9px; border:1px solid #3dd6a866; color:#73f0c7!important; border-radius:999px; font-family:'DM Mono',monospace; font-size:9px; letter-spacing:.07em; background:#21b77d18; }
        [data-testid="stSidebar"] .stButton button { border:1px solid #ffffff22; background:#ffffff0d; border-radius:10px; font-size:11px; margin-top:4px; }
        [data-testid="stSidebar"] .stButton button:hover { border-color:#69b6ff; background:#ffffff1a; transform:none; }
        .page-kicker,.eyebrow { color:#426cff; font-size:10px; font-weight:800; letter-spacing:.14em; }
        .page-title { font-size:2rem; letter-spacing:-.055em; margin:.4rem 0 1.2rem; }
        .hero { padding:2rem 0 .5rem; }
        .hero h1 { max-width:700px; margin:.55rem 0 .95rem; font-size:clamp(2.6rem,5vw,4.7rem); line-height:1.02; letter-spacing:-.075em; }
        .hero h1 span { background:linear-gradient(100deg,#385ee3,#34bddd); -webkit-background-clip:text; color:transparent; }
        .hero p { max-width:620px; color:var(--muted); font-size:1.03rem; line-height:1.75; }
        [data-testid="stImage"] img { border-radius:24px; box-shadow:0 25px 55px #183a6e24; border:1px solid #c5d7f2; }
        .section-title { margin:2.5rem 0 1rem; font-size:1.23rem; font-weight:800; letter-spacing:-.035em; }
        .feature-card { height:100%; min-height:175px; padding:1.25rem; border-radius:18px; border:1px solid transparent; background:linear-gradient(#fff,#fff) padding-box,linear-gradient(140deg,#d5e2ff,#eff2ff,#aeeefa) border-box; box-shadow:0 12px 28px #1c47810c; transition:transform .2s ease,box-shadow .2s ease; }
        .feature-card:hover { transform:translateY(-4px); box-shadow:0 19px 34px #1c478120; }
        .feature-icon { display:grid; place-items:center; width:37px; height:37px; border-radius:11px; color:#3156cb; background:#eaf0ff; font-size:18px; }
        .feature-card h3 { margin:14px 0 6px; font-size:.95rem; letter-spacing:-.02em; }
        .feature-card p { margin:0; color:var(--muted); font-size:.78rem; line-height:1.55; }
        .stButton button { min-height:2.55rem; border:1px solid #d9e3f2; border-radius:11px; color:#25456f; font-family:Manrope,sans-serif; font-size:.78rem; font-weight:800; background:#fff; transition:all .18s ease; }
        .stButton button:hover { color:#2249d1; border-color:#83a7f4; transform:translateY(-1px); box-shadow:0 8px 16px #537ed71c; }
        .stButton button[kind="primary"] { color:white; border:0; background:linear-gradient(100deg,#3b5ee3,#3778ed); box-shadow:0 9px 19px #315edb35; }
        .stButton button[kind="primary"]:hover { color:white; background:linear-gradient(100deg,#3156dc,#246deb); }
        [data-testid="stChatInput"] { border-radius:15px; border:1px solid #d8e3f0; box-shadow:0 9px 28px #1b416413; }
        [data-testid="stChatInput"] textarea { font-family:Manrope,sans-serif!important; }
        [data-testid="stChatMessage"] { border-radius:16px; }
        div[data-testid="stForm"] { border:1px solid #dce6f3; border-radius:17px; padding:1.2rem; background:#ffffffca; box-shadow:0 10px 25px #173b690a; }
        .interview-topline { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:1rem; }
        .interview-topline span { color:#3d5c84; border:1px solid #d4e0f2; border-radius:99px; padding:5px 9px; background:#fff; font-size:10px; font-weight:800; }
        .feedback-header { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding-bottom:1rem; border-bottom:1px solid #e5edf7; margin-bottom:.85rem; }
        .feedback-header span { color:#5a78da; font-size:10px; font-weight:800; letter-spacing:.1em; }
        .feedback-header h3 { margin:.17rem 0 0; color:#122647; font-size:1.9rem; letter-spacing:-.07em; }
        .feedback-header h3 small { font-size:.8rem; color:#71829a; letter-spacing:0; }
        .verdict { padding:7px 10px; border-radius:9px; background:#e8f0ff; color:#3157c2; font-size:11px; font-weight:800; }
        .feedback-block { margin-top:1rem; }
        .feedback-block h4 { color:#233b60; font-size:.83rem; margin:0 0 .2rem; }
        .footer { padding-top:4rem; text-align:center; color:#8492a6; font-size:10px; line-height:1.7; }
        .footer strong { color:#526c93; }
        @media (max-width:700px) { .block-container {padding:1.4rem 1rem 3rem;} .page-title {font-size:1.65rem;} .hero {padding-top:1rem;} }
        </style>
        """,
        unsafe_allow_html=True,
    )
