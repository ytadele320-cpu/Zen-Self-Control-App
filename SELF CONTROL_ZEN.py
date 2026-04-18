import streamlit as st
import json
import os
import platform
import random
import time
import base64
from datetime import datetime


# --- NEW: HELPER FUNCTION FOR BACKGROUND IMAGE ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Try to load the background; if it fails, it uses a dark fallback color
try:
    bin_str = get_base64_of_bin_file('TIME.jpg')
    bg_style = f'url("data:image/jpg;base64,{bin_str}")'
except FileNotFoundError:
    bg_style = "linear-gradient(#2c3e50, #000000)"  # Fallback if image is missing

# 1. CORE CONFIGURATION
st.set_page_config(
    page_title="Zen Self Control | Focus & Flow",
    page_icon="⏳",  # Switched to emoji for stability, change back to "hourglass.jpg" if file exists
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ZEN THEMING WITH DYNAMIC BACKGROUND
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), 
                    {bg_style}; 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
    }}
    .zen-panel {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }}
    .timer-display {{
        font-size: 4.5rem;
        font-weight: 300;
        text-align: center;
        color: white;
        font-family: 'Georgia', serif;
        margin: 25px 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
    }}
    .stats-card {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        backdrop-filter: blur(10px);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .task-item {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid rgba(102, 126, 234, 0.8);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        color: white;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }}
    .zen-quote {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        font-style: italic;
        font-size: 1.3rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }}
    .stButton>button {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.7), rgba(118, 75, 162, 0.7));
        backdrop-filter: blur(10px);
        color: white;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 500;
        padding: 12px 25px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }}
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
    }}
    h1, h2, h3 {{ 
        color: white; 
        font-family: 'Georgia', serif;
        font-weight: 300;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }}
    .hourglass-animation {{
        animation: float 6s ease-in-out infinite;
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
</style>
""", unsafe_allow_html=True)


# 3. DATA PERSISTENCE FUNCTIONS
def save_data():
    data_to_save = {
        'sessions_completed': st.session_state.sessions_completed,
        'total_focus_time': st.session_state.total_focus_time,
        'tasks': st.session_state.tasks,
        'blocked_sites': st.session_state.blocked_sites,
        'achievements': st.session_state.achievements,
        'work_duration': st.session_state.work_duration,
        'break_duration': st.session_state.break_duration,
        'focus_mode_active': st.session_state.focus_mode_active,
        'sound_enabled': st.session_state.sound_enabled,
        'quote_index': st.session_state.quote_index
    }
    try:
        with open('zen_control_data.json', 'w') as f:
            json.dump(data_to_save, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")


def load_data():
    try:
        if os.path.exists('zen_control_data.json'):
            with open('zen_control_data.json', 'r') as f:
                loaded_data = json.load(f)
            for key, value in loaded_data.items():
                if key in st.session_state:
                    st.session_state[key] = value
            return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return False


# 4. SESSION STATE INITIALIZATION
def init_session_state():
    defaults = {
        'timer_running': False,
        'timer_seconds': 25 * 60,
        'work_duration': 25 * 60,
        'break_duration': 5 * 60,
        'is_work_session': True,
        'sessions_completed': 0,
        'total_focus_time': 0,
        'tasks': [],
        'blocked_sites': ['facebook.com', 'twitter.com', 'instagram.com', 'youtube.com', 'reddit.com'],
        'achievements': [],
        'sound_enabled': True,
        'focus_mode_active': False,
        'quote_index': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    load_data()


init_session_state()

# 5. ZEN QUOTES
zen_quotes = [
    "Time is the most valuable thing a person can spend. - Theophrastus",
    "In the midst of movement and chaos, keep stillness inside you. - Deepak Chopra",
    "The present moment is the only time over which we have dominion. - Thích Nhât Hành",
    "The bad news is time flies. The good news is you're the pilot. - Michael Altshuler",
    "Time is a created thing. To say 'I don't have time,' is like saying, 'I don't want to.' - Lao Tzu"
]

current_quote = zen_quotes[st.session_state.quote_index]


# 6. HELPER FUNCTIONS
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def add_task(title, priority="medium"):
    task = {
        'id': len(st.session_state.tasks) + 1,
        'title': title,
        'priority': priority,
        'completed': False,
        'pomodoros_completed': 0
    }
    st.session_state.tasks.append(task)
    save_data()


def update_timer():
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        st.session_state.timer_seconds -= 1
        st.session_state.total_focus_time += 1
        time.sleep(1)
        st.rerun()
    elif st.session_state.timer_seconds == 0:
        st.session_state.timer_running = False
        st.session_state.sessions_completed += 1
        st.session_state.is_work_session = not st.session_state.is_work_session
        st.session_state.timer_seconds = st.session_state.work_duration if st.session_state.is_work_session else st.session_state.break_duration
        save_data()
        st.rerun()


# 7. ZEN SETTINGS SIDEBAR
with st.sidebar:
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.header("Zen Settings")
    
    # Focus Mode Toggle
    st.subheader("Focus Mode")
    if st.button("Activate Zen Focus" if not st.session_state.focus_mode_active else "Deactivate Zen Focus"):
        st.session_state.focus_mode_active = not st.session_state.focus_mode_active
        if st.session_state.focus_mode_active:
            st.success("Zen Focus Mode activated!")
        else:
            st.success("Zen Focus Mode deactivated!")
        save_data()
        st.rerun()
    
    # Timer settings
    st.subheader("Timer Settings")
    work_minutes = st.slider("Work Duration (min)", 5, 60, st.session_state.work_duration // 60)
    break_minutes = st.slider("Break Duration (min)", 1, 30, st.session_state.break_duration // 60)
    
    st.session_state.work_duration = work_minutes * 60
    st.session_state.break_duration = break_minutes * 60
    
    # Ambient Sound Settings
    st.subheader("Ambient Sounds")
    if st.button("Toggle Birds Sound"):
        st.session_state.sound_enabled = not st.session_state.sound_enabled
        sound_status = "activated" if st.session_state.sound_enabled else "deactivated"
        st.info(f"Birds Whispering {sound_status}")
        save_data()
    
    sound_status = "Active" if st.session_state.sound_enabled else "Inactive"
    st.info(f"Birds Whispering: {sound_status}")
    
    # New quote button
    st.subheader("Daily Inspiration")
    if st.button("New Zen Quote"):
        st.session_state.quote_index = (st.session_state.quote_index + 1) % len(zen_quotes)
        save_data()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 8. LAYOUT
st.title("Zen Self Control")

st.markdown(f"""
<div class="zen-quote hourglass-animation">
    <div style="font-size: 2rem; margin-bottom: 15px;">⏳</div>
    {current_quote}
</div>
""", unsafe_allow_html=True)

# Focus Mode Indicator
if st.session_state.focus_mode_active:
    st.markdown("""
    <div class="focus-mode-zen">
        <div style="font-size: 2rem; margin-bottom: 10px;">🧘</div>
        ZEN FOCUS MODE ACTIVE - Deep concentration enabled
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    session_type = "Deep Work Session" if st.session_state.is_work_session else "Mindful Break"
    st.subheader(session_type)
    st.markdown(f"<div class='timer-display'>{format_time(st.session_state.timer_seconds)}</div>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    if c1.button("Start"): st.session_state.timer_running = True; st.rerun()
    if c2.button("Pause"): st.session_state.timer_running = False; st.rerun()
    if c3.button("Reset"):
        st.session_state.timer_running = False
        st.session_state.timer_seconds = st.session_state.work_duration if st.session_state.is_work_session else st.session_state.break_duration
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Task Management
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.header("Mindful Tasks")
    new_t = st.text_input("What are you focusing on?")
    if st.button("Add Task") and new_t:
        add_task(new_t)
        st.rerun()

    for t in st.session_state.tasks:
        if not t['completed']:
            st.markdown(f"**{t['title']}** (Poms: {t['pomodoros_completed']})")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.header("Zen Stats")
    st.metric("Sessions Done", st.session_state.sessions_completed)
    st.metric("Total Seconds", st.session_state.total_focus_time)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Distraction Blocker
    st.markdown('<div class="zen-panel">', unsafe_allow_html=True)
    st.header("Distraction Blocker")
    
    st.subheader("Blocked Sites")
    for site in st.session_state.blocked_sites:
        st.error(f"blocked: {site}")
    
    with st.expander("Add Site to Block"):
        new_site = st.text_input("Website (e.g., reddit.com)")
        if st.button("Block Site") and new_site:
            if new_site not in st.session_state.blocked_sites:
                st.session_state.blocked_sites.append(new_site)
                save_data()
                st.success(f"{new_site} added to block list")
                st.rerun()
    
    with st.expander("Remove Site from Block"):
        if st.session_state.blocked_sites:
            site_to_remove = st.selectbox("Select site", st.session_state.blocked_sites)
            if st.button("Unblock Site"):
                st.session_state.blocked_sites.remove(site_to_remove)
                save_data()
                st.success(f"{site_to_remove} removed from block list")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.timer_running:
    update_timer()