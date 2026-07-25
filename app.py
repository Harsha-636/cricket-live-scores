import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="CricLive — Live Cricket Scores", page_icon="🏏", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0f1420 100%); }

.hero-header {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    padding: 1.5rem; border-radius: 16px; margin-bottom: 1rem; color: white;
}
.hero-header h1 { font-size: 1.8rem; font-weight: 800; margin: 0; }
.hero-header p { font-size: 0.85rem; opacity: 0.9; margin: 4px 0 0; }

.match-card {
    background: #161d2e; border: 1px solid #232d42; border-radius: 16px;
    padding: 16px; margin-bottom: 12px;
}
.match-card.live { border-left: 4px solid #ef4444; }
.match-card.upcoming { border-left: 4px solid #eab308; }
.match-card.completed { border-left: 4px solid #5b6b85; }

.live-badge { color: #ef4444; font-weight: 700; font-size: 0.75rem; }
.upcoming-badge { color: #eab308; font-weight: 700; font-size: 0.75rem; }
.completed-badge { color: #94a3b8; font-weight: 700; font-size: 0.75rem; }
.match-type { background: #1c2438; color: #94a3b8; font-size: 0.65rem; font-weight: 700;
    padding: 2px 8px; border-radius: 6px; text-transform: uppercase; display: inline-block; }

.team-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; }
.team-name { font-weight: 600; color: #f1f5f9; }
.team-score { font-weight: 700; color: #f1f5f9; }
.match-status { color: #94a3b8; font-size: 0.82rem; margin-top: 8px; padding-top: 8px; border-top: 1px solid #232d42; }
.match-venue { color: #5b6b85; font-size: 0.72rem; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

MOCK_MATCHES = [
    {"id": "1", "name": "India vs Australia", "status": "India won by 6 wickets", "matchStarted": True, "matchEnded": True,
     "teams": ["India", "Australia"], "score": [
        {"r": 287, "w": 6, "o": 48.4}, {"r": 291, "w": 4, "o": 47.2}],
     "venue": "Wankhede Stadium, Mumbai", "matchType": "ODI"},
    {"id": "2", "name": "England vs New Zealand", "status": "Live", "matchStarted": True, "matchEnded": False,
     "teams": ["England", "New Zealand"], "score": [{"r": 156, "w": 3, "o": 22.3}],
     "venue": "Lord's, London", "matchType": "T20"},
    {"id": "3", "name": "Pakistan vs South Africa", "status": "Match starts in 2 hours", "matchStarted": False, "matchEnded": False,
     "teams": ["Pakistan", "South Africa"], "score": [],
     "venue": "Gaddafi Stadium, Lahore", "matchType": "Test"},
    {"id": "4", "name": "Sri Lanka vs Bangladesh", "status": "Sri Lanka won by 34 runs", "matchStarted": True, "matchEnded": True,
     "teams": ["Sri Lanka", "Bangladesh"], "score": [
        {"r": 245, "w": 8, "o": 50}, {"r": 211, "w": 10, "o": 46.2}],
     "venue": "R Premadasa Stadium, Colombo", "matchType": "ODI"},
    {"id": "5", "name": "West Indies vs Afghanistan", "status": "Live", "matchStarted": True, "matchEnded": False,
     "teams": ["West Indies", "Afghanistan"], "score": [{"r": 89, "w": 2, "o": 12.4}],
     "venue": "Kensington Oval, Barbados", "matchType": "T20"},
    {"id": "6", "name": "India vs England", "status": "Match starts tomorrow", "matchStarted": False, "matchEnded": False,
     "teams": ["India", "England"], "score": [],
     "venue": "Eden Gardens, Kolkata", "matchType": "ODI"},
]

st.markdown("""
<div class="hero-header">
    <h1>🏏 CricLive — Live Cricket Scores</h1>
    <p>Live scores, match updates & schedules</p>
</div>
""", unsafe_allow_html=True)

live = [m for m in MOCK_MATCHES if m["matchStarted"] and not m["matchEnded"]]
upcoming = [m for m in MOCK_MATCHES if not m["matchStarted"]]
completed = [m for m in MOCK_MATCHES if m["matchEnded"]]

col1, col2, col3 = st.columns(3)
col1.metric("🔴 Live", len(live))
col2.metric("⏰ Upcoming", len(upcoming))
col3.metric("✅ Completed", len(completed))

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["All Matches", "🔴 Live", "Upcoming", "Completed"])

def render_match(m):
    is_live = m["matchStarted"] and not m["matchEnded"]
    is_upcoming = not m["matchStarted"]
    card_class = "live" if is_live else ("upcoming" if is_upcoming else "completed")
    badge = '<span class="live-badge">🔴 LIVE</span>' if is_live else ('<span class="upcoming-badge">⏰ UPCOMING</span>' if is_upcoming else '<span class="completed-badge">✓ COMPLETED</span>')

    teams_html = ""
    for i, team in enumerate(m["teams"]):
        score = m["score"][i] if i < len(m["score"]) else None
        score_text = f'{score["r"]}/{score["w"]} <span style="color:#5b6b85;font-size:0.75rem">({score["o"]} ov)</span>' if score else '<span style="color:#5b6b85">Yet to bat</span>'
        teams_html += f'<div class="team-row"><span class="team-name">{team}</span><span class="team-score">{score_text}</span></div>'

    st.markdown(f"""
    <div class="match-card {card_class}">
        <div style="display:flex;justify-content:space-between;margin-bottom:10px">
            <span class="match-type">{m["matchType"]}</span>
            {badge}
        </div>
        {teams_html}
        <div class="match-status">📢 {m["status"]}</div>
        <div class="match-venue">📍 {m["venue"]}</div>
    </div>
    """, unsafe_allow_html=True)

with tab1:
    for m in MOCK_MATCHES:
        render_match(m)

with tab2:
    if live:
        for m in live:
            render_match(m)
    else:
        st.info("No live matches right now")

with tab3:
    for m in upcoming:
        render_match(m)

with tab4:
    for m in completed:
        render_match(m)

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#4b5563;font-size:0.78rem;padding:8px'>
    Built by <strong>Sai Harsha Vardhan Reddy Avula</strong> · Python · Streamlit · REST API ·
    <a href='https://github.com/Harsha-636/cricket-live-scores' style='color:#22c55e'>GitHub</a>
</div>
""", unsafe_allow_html=True)
