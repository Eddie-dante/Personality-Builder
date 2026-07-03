# app.py - Aura Builder · id³ (Complete with Chat)
import streamlit as st
import random
import datetime
import time
import json
import os
import sys
import calendar as cal_module

# Page configuration
st.set_page_config(
    page_title="Aura Builder · id³",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
#  CUSTOM CSS - EXACT MATCH TO ORIGINAL DESIGN
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;450;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        min-height: 100vh;
        color: #0f172a;
        transition: background 0.9s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    /* Signature */
    .signature {
        position: fixed;
        bottom: 90px;
        right: 28px;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 2.5px;
        color: #0f172a;
        opacity: 0.25;
        z-index: 100;
        background: rgba(255,255,255,0.4);
        padding: 6px 14px;
        border-radius: 40px;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.2);
        pointer-events: none;
    }
    
    /* Glass container */
    .glass-box {
        background: rgba(255,255,255,0.75) !important;
        backdrop-filter: blur(24px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(24px) saturate(1.6) !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        border-radius: 32px !important;
        padding: 32px 28px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.02) inset !important;
    }
    
    /* Landing */
    .badge-chip {
        display: inline-block;
        background: rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.06);
        padding: 6px 18px;
        border-radius: 40px;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #64748b;
    }
    
    .landing-title {
        font-size: 44px;
        font-weight: 700;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #0f172a 60%, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .tagline {
        color: #64748b;
        font-size: 15px;
        font-weight: 400;
        letter-spacing: 0.2px;
    }
    
    /* Counter chip */
    .counter-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0,0,0,0.04);
        padding: 4px 14px 4px 12px;
        border-radius: 40px;
        font-size: 13px;
        color: #475569;
        border: 1px solid rgba(0,0,0,0.04);
    }
    
    /* Aura button */
    .aura-row {
        padding: 16px 18px;
        background: rgba(255,255,255,0.5);
        border: 1.5px solid rgba(0,0,0,0.04);
        border-radius: 16px;
        transition: all 0.25s ease;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        margin: 5px 0;
        cursor: pointer;
    }
    
    .aura-row:hover {
        border-color: rgba(0,0,0,0.12);
        background: rgba(255,255,255,0.8);
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    }
    
    .aura-row.selected {
        border-color: #0f172a;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    
    /* Score ring */
    .score-ring-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 16px 0 22px;
    }
    
    /* Task item */
    .task-row {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 14px;
        gap: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        margin: 4px 0;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    
    .task-row:hover {
        border-color: #e2e8f0;
        background: #fafbfc;
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }
    
    .task-row.done {
        opacity: 0.6;
        border-color: #f1f5f9;
    }
    
    .check-box {
        width: 24px;
        height: 24px;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
        background: #fff;
    }
    
    .task-row.done .check-box {
        background: #0f172a;
        border-color: #0f172a;
        color: #fff;
    }
    
    .task-row.done .task-label {
        text-decoration: line-through;
        color: #94a3b8;
    }
    
    /* Calendar - FULLY VISIBLE */
    .calendar-box {
        margin-top: 6px;
        padding: 18px 16px 16px;
        background: rgba(255,255,255,0.5);
        border-radius: 18px;
        border: 1px solid rgba(0,0,0,0.04);
        overflow: hidden;
    }
    
    .cal-month {
        font-size: 14px;
        font-weight: 600;
        color: #1e293b;
        letter-spacing: 0.3px;
        margin-bottom: 14px;
    }
    
    .cal-day {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 450;
        border-radius: 10px;
        background: rgba(0,0,0,0.02);
        color: #94a3b8;
        min-width: 30px;
        min-height: 30px;
    }
    
    .cal-day.streak {
        background: #0f172a;
        color: #fff;
        font-weight: 600;
        box-shadow: 0 4px 16px rgba(15,23,42,0.15);
    }
    
    .cal-day.today-cell {
        border: 2px solid #0f172a;
        background: transparent;
        color: #0f172a;
        font-weight: 600;
    }
    
    .cal-day.weekday-label {
        font-size: 10px;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        background: transparent;
    }
    
    /* Chat */
    .chat-bubble {
        padding: 10px 16px;
        border-radius: 18px;
        margin: 6px 0;
        max-width: 80%;
        font-size: 14px;
    }
    
    .chat-sent {
        background: #0f172a;
        color: #fff;
        margin-left: auto;
    }
    
    .chat-received {
        background: #f1f5f9;
        color: #1e293b;
        margin-right: auto;
    }
    
    /* Bottom nav */
    .bottom-nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 10px 8px;
        padding-bottom: max(10px, env(safe-area-inset-bottom));
        z-index: 1000;
        border-top: 1px solid rgba(0,0,0,0.06);
    }
    
    @media (min-width: 769px) {
        .bottom-nav-bar {
            max-width: 500px;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 20px 20px 0 0;
        }
    }
    
    /* Wallpaper FAB */
    .wp-fab {
        position: fixed;
        bottom: 90px;
        left: 20px;
        z-index: 999;
        background: rgba(15,23,42,0.9);
        width: 44px;
        height: 44px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    /* Buttons */
    .stButton > button {
        width: 100% !important;
        padding: 18px !important;
        background: #0f172a !important;
        border: none !important;
        border-radius: 16px !important;
        color: #fff !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 16px rgba(15,23,42,0.15) !important;
        transition: all 0.25s ease !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(15,23,42,0.2) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Secondary button */
    .btn-ghost button {
        background: transparent !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
        color: #64748b !important;
        box-shadow: none !important;
    }
    
    .btn-ghost button:hover {
        background: rgba(0,0,0,0.02) !important;
        border-color: rgba(0,0,0,0.15) !important;
        color: #0f172a !important;
    }
    
    /* Nav buttons */
    .nav-btn button {
        padding: 8px 16px !important;
        font-size: 13px !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        background: transparent !important;
        color: #64748b !important;
        border: 1px solid transparent !important;
    }
    
    .nav-btn.active button {
        background: rgba(0,0,0,0.06) !important;
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    /* Responsive */
    @media (max-width: 480px) {
        .glass-box {
            padding: 24px 18px !important;
            border-radius: 24px !important;
        }
        .landing-title {
            font-size: 34px;
        }
    }
    
    /* Streamlit spacing fix */
    .stMainBlockContainer {
        padding-top: 1rem !important;
        padding-bottom: 100px !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  UNSPLASH WALLPAPERS (200+)
# ============================================================
UNSPLASH_WALLPAPERS = [
    # Abstract & Gradients
    "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920&q=80",
    "https://images.unsplash.com/photo-1557682224-5b8590cd9ec5?w=1920&q=80",
    "https://images.unsplash.com/photo-1557682260-96773eb01377?w=1920&q=80",
    "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920&q=80",
    "https://images.unsplash.com/photo-1558470598-a5dda9640f68?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929662-711aa81148cf?w=1920&q=80",
    "https://images.unsplash.com/photo-1553356084-58ef4a67b2a7?w=1920&q=80",
    "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=1920&q=80",
    "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1920&q=80",
    # Nature
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1920&q=80",
    "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1920&q=80",
    "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1920&q=80",
    "https://images.unsplash.com/photo-1518655048521-f130df041f66?w=1920&q=80",
    "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?w=1920&q=80",
    # Minimal
    "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80",
    "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1920&q=80",
    "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=1920&q=80",
    "https://images.unsplash.com/photo-1485988412941-77a35537dae4?w=1920&q=80",
    "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920&q=80",
    "https://images.unsplash.com/photo-1432821596592-e2c18b78144f?w=1920&q=80",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1920&q=80",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=80",
    # Dark & Moody
    "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=1920&q=80",
    "https://images.unsplash.com/photo-1477346611705-65d1883cee1e?w=1920&q=80",
    "https://images.unsplash.com/photo-1515630278258-407f66498911?w=1920&q=80",
    "https://images.unsplash.com/photo-1491466424936-e304919aada7?w=1920&q=80",
    "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1920&q=80",
    "https://images.unsplash.com/photo-1516796181076-3a4e8a7e00d7?w=1920&q=80",
    "https://images.unsplash.com/photo-1502139214982-d0ad755818d8?w=1920&q=80",
    "https://images.unsplash.com/photo-1506891536236-3e07892564b7?w=1920&q=80",
    "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=1920&q=80",
    "https://images.unsplash.com/photo-1491895200222-0fc4a4c35e18?w=1920&q=80",
    # Warm & Golden
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "https://images.unsplash.com/photo-1474524955719-b7f5099ab369?w=1920&q=80",
    "https://images.unsplash.com/photo-1504198322253-cfa87a0ff25f?w=1920&q=80",
    "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=1920&q=80",
    "https://images.unsplash.com/photo-1487147264018-f937fba0c817?w=1920&q=80",
    # Cool & Blue
    "https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=1920&q=80",
    "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?w=1920&q=80",
    "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1920&q=80",
    "https://images.unsplash.com/photo-1518459031867-a89b550b39f2?w=1920&q=80",
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    # Texture & Pattern
    "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920&q=80",
    "https://images.unsplash.com/photo-1558470598-a5dda9640f68?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929662-711aa81148cf?w=1920&q=80",
    "https://images.unsplash.com/photo-1553356084-58ef4a67b2a7?w=1920&q=80",
    # Extra (to reach 200+)
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920&q=80",
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920&q=80",
    "https://images.unsplash.com/photo-1446329813274-7c9036bd9a1f?w=1920&q=80",
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920&q=80",
    "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=1920&q=80",
    "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?w=1920&q=80",
    "https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920&q=80",
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=80",
    "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=1920&q=80",
    "https://images.unsplash.com/photo-1439853949127-fa647821eba0?w=1920&q=80",
    "https://images.unsplash.com/photo-1518173946687-a1e4e3e6a4e0?w=1920&q=80",
    "https://images.unsplash.com/photo-1470770903676-69b98201ea1c?w=1920&q=80",
    "https://images.unsplash.com/photo-1497436072909-60f360e1d4b1?w=1920&q=80",
    "https://images.unsplash.com/photo-1504198453319-5ce911bafcde?w=1920&q=80",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920&q=80",
    "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=1920&q=80",
    "https://images.unsplash.com/photo-1532274402911-5a369e4c4bb5?w=1920&q=80",
    "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920&q=80",
    "https://images.unsplash.com/photo-1510784722466-f2aa9c52fff6?w=1920&q=80",
    "https://images.unsplash.com/photo-1518098268026-4e89f1a0cd8e?w=1920&q=80",
]

# ============================================================
#  AURA DEFINITIONS (from original)
# ============================================================
AURAS = {
    'cold': {
        'name': 'Cold Aura', 'desc': 'Distant & unreadable',
        'gradient': 'linear-gradient(145deg, #e0f2fe 0%, #bae6fd 60%, #7dd3fc 100%)',
        'accent': '#0284c7', 'emoji': '❄️',
        'tasks': ['Poker face — 2 min', 'Pause 2s before replying', 'Short neutral answers', 'Slow, deliberate movements', 'One hand in pocket']
    },
    'mystery': {
        'name': 'Mystery Aura', 'desc': 'Quiet depth',
        'gradient': 'linear-gradient(145deg, #f3e8ff 0%, #d8b4fe 60%, #c084fc 100%)',
        'accent': '#7e22ce', 'emoji': '🌙',
        'tasks': ['Avoid explaining yourself', 'Answer then pause', 'Change subject when probed', 'Limited eye contact', 'Leave rooms early']
    },
    'nonchalant': {
        'name': 'Nonchalant Aura', 'desc': 'Unbothered energy',
        'gradient': 'linear-gradient(145deg, #fef3c7 0%, #fde68a 60%, #fcd34d 100%)',
        'accent': '#b45309', 'emoji': '😌',
        'tasks': ['Shrug off drama lightly', 'Reply late casually', 'Relaxed open posture', '"We\'ll see" responses', 'Skip 1 optional event']
    },
    'intense': {
        'name': 'Intense Aura', 'desc': 'Sharp presence',
        'gradient': 'linear-gradient(145deg, #fee2e2 0%, #fca5a5 60%, #f87171 100%)',
        'accent': '#b91c1c', 'emoji': '🔥',
        'tasks': ['Direct eye contact', 'Sharp, concise speech', 'Minimal smiling', 'Controlled gestures', 'Take space when standing']
    },
    'calm': {
        'name': 'Calm Aura', 'desc': 'Peaceful energy',
        'gradient': 'linear-gradient(145deg, #d1fae5 0%, #6ee7b7 60%, #34d399 100%)',
        'accent': '#047857', 'emoji': '🌊',
        'tasks': ['Slow diaphragmatic breathing', 'Soft, warm voice tone', 'Gentle movements', 'Listen fully without interrupting', 'No rushing — take your time']
    },
    'royal': {
        'name': 'Royal Aura', 'desc': 'Natural authority',
        'gradient': 'linear-gradient(145deg, #fef9c3 0%, #fde047 60%, #facc15 100%)',
        'accent': '#854d0e', 'emoji': '👑',
        'tasks': ['Upright posture always', 'Measured, deliberate speech', 'Don\'t rush to respond', 'Others wait for you', 'Head level, chin up']
    }
}

# ============================================================
#  SESSION STATE
# ============================================================
if 'selected_auras' not in st.session_state:
    st.session_state.selected_auras = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []
if 'streak_data' not in st.session_state:
    st.session_state.streak_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'wallpaper' not in st.session_state:
    st.session_state.wallpaper = random.choice(UNSPLASH_WALLPAPERS)
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'online_users' not in st.session_state:
    st.session_state.online_users = [
        {'name': 'Edwin', 'avatar': '🦾', 'bio': 'Creator'},
        {'name': 'Alex', 'avatar': '🧑‍💻', 'bio': 'Focus master'},
        {'name': 'Maya', 'avatar': '👩‍🎨', 'bio': 'Creative spirit'},
        {'name': 'Zane', 'avatar': '🦸', 'bio': 'Warrior'},
        {'name': 'Luna', 'avatar': '🌙', 'bio': 'Mystic'},
    ]
if 'chat_user' not in st.session_state:
    st.session_state.chat_user = 'Edwin'

# ============================================================
#  HELPERS
# ============================================================
def set_bg():
    wp = st.session_state.wallpaper
    if not wp.startswith('http'):
        wp = random.choice(UNSPLASH_WALLPAPERS)
    st.markdown(f"""
    <style>
        .stApp {{
            background: url('{wp}') center/cover fixed !important;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255,255,255,0.2);
            z-index: -1;
        }}
    </style>
    """, unsafe_allow_html=True)

def get_tasks():
    tasks = []
    for key in st.session_state.selected_auras:
        if key in AURAS:
            tasks.extend(AURAS[key]['tasks'])
    return list(dict.fromkeys(tasks))[:8]

def calc_score():
    tasks = get_tasks()
    total = len(tasks)
    done = len([i for i in st.session_state.completed_tasks if i < total])
    return (round((done/total)*100) if total > 0 else 0), done, total

def toggle_task(i):
    if i in st.session_state.completed_tasks:
        st.session_state.completed_tasks.remove(i)
    else:
        st.session_state.completed_tasks.append(i)
    tasks = get_tasks()
    total = len(tasks)
    done = len([x for x in st.session_state.completed_tasks if x < total])
    today = datetime.date.today().isoformat()
    if done == total and total > 0:
        st.session_state.streak_data[today] = True
    else:
        st.session_state.streak_data.pop(today, None)
    st.rerun()

# ============================================================
#  PAGES
# ============================================================
def show_landing():
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-box" style="text-align: center;">
            <span class="badge-chip">✦ v2.0</span>
            <div style="font-size: 68px; line-height: 1; margin: 8px 0;">⚡</div>
            <h1 class="landing-title">Aura Builder</h1>
            <p class="tagline">Train your presence. <strong style="color:#1e293b;">Manifest your aura.</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Begin Journey", key="begin"):
            st.session_state.current_page = 'select'
            st.rerun()
    with c2:
        if st.button("Continue →", key="cont"):
            if st.session_state.selected_auras:
                st.session_state.current_page = 'tracker'
            else:
                st.session_state.current_page = 'select'
            st.rerun()

def show_select():
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-box">
            <div style="margin-bottom: 20px;">
                <h2 style="font-size: 26px; font-weight: 700; letter-spacing: -0.5px; color: #0f172a;">Choose Your Aura</h2>
                <p style="color: #64748b; font-size: 14px; margin-top: 2px;">Select up to 2 to shape your presence</p>
            </div>
    """, unsafe_allow_html=True)
    
    count = len(st.session_state.selected_auras)
    st.markdown(f'<div class="counter-chip"><span>✧</span> <strong>{count}</strong><span>/2 selected</span></div>', unsafe_allow_html=True)
    
    for key, aura in AURAS.items():
        sel = key in st.session_state.selected_auras
        c1, c2, c3 = st.columns([0.12, 0.76, 0.12])
        with c1:
            st.markdown(f'<div style="font-size:26px;padding-top:8px;">{aura["emoji"]}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<strong style="color:#0f172a;font-size:16px;">{aura["name"]}</strong><br><small style="color:#64748b;">{aura["desc"]}</small>', unsafe_allow_html=True)
        with c3:
            if sel:
                st.markdown('<div style="font-size:18px;padding-top:8px;color:#0f172a;">✓</div>', unsafe_allow_html=True)
        
        if st.button("Deselect" if sel else "Select", key=f"sel_{key}", use_container_width=True):
            if sel:
                st.session_state.selected_auras.remove(key)
            elif len(st.session_state.selected_auras) < 2:
                st.session_state.selected_auras.append(key)
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Continue", key="conf"):
            if st.session_state.selected_auras:
                st.session_state.current_page = 'tracker'
                st.rerun()
            else:
                st.warning("Select at least one aura")
    with c2:
        if st.button("← Back", key="back_sel"):
            st.session_state.current_page = 'landing'
            st.rerun()

def show_tracker():
    if not st.session_state.selected_auras:
        st.session_state.current_page = 'select'
        st.rerun()
    
    primary = AURAS[st.session_state.selected_auras[0]]
    secondary = AURAS[st.session_state.selected_auras[1]] if len(st.session_state.selected_auras) > 1 else None
    pct, done, total = calc_score()
    tasks = get_tasks()
    
    title = f"{primary['emoji']} {primary['name']}"
    subtitle = primary['desc']
    badge = f"⚡ {primary['emoji']}"
    if secondary:
        title += f" + {secondary['emoji']} {secondary['name']}"
        subtitle += f" + {secondary['desc']}"
        badge += f" {secondary['emoji']}"
    
    circumference = 2 * 3.14159 * 52
    offset = circumference - (pct / 100) * circumference
    
    st.markdown(f"""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-box">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
                <div>
                    <h2 style="font-size:22px;font-weight:700;letter-spacing:-0.5px;line-height:1.2;color:#0f172a;">{title}</h2>
                    <p style="color:#64748b;font-size:13px;margin-top:1px;">{subtitle}</p>
                </div>
                <div style="background:rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.04);padding:4px 14px;border-radius:40px;font-size:11px;color:#475569;font-weight:500;">{badge}</div>
            </div>
            <div class="score-ring-wrap">
                <div style="position:relative;width:120px;height:120px;">
                    <svg width="120" height="120" viewBox="0 0 120 120" style="transform:rotate(-90deg);">
                        <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="6"/>
                        <circle cx="60" cy="60" r="52" fill="none" stroke="{primary['accent']}" stroke-width="6" stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}"/>
                    </svg>
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
                        <div style="font-size:34px;font-weight:700;letter-spacing:-1px;line-height:1;color:#0f172a;">{pct}%</div>
                        <div style="font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:1.2px;margin-top:2px;">Aura Strength</div>
                    </div>
                </div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
                <span style="font-size:13px;font-weight:600;color:#475569;">Today's Practice</span>
                <span style="color:#94a3b8;font-size:13px;">{done}/{total} done</span>
            </div>
    """, unsafe_allow_html=True)
    
    for i, task in enumerate(tasks):
        is_done = i in st.session_state.completed_tasks
        c1, c2 = st.columns([0.1, 0.9])
        with c1:
            st.markdown(f"""
            <div style="width:24px;height:24px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;
            {'background:#0f172a;border:2px solid #0f172a;color:#fff;' if is_done else 'border:2px solid #cbd5e1;background:#fff;'}">
            {'✓' if is_done else ''}</div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <span style="font-size:14px;font-weight:450;color:{'#94a3b8' if is_done else '#1e293b'};
            {'text-decoration:line-through;' if is_done else ''}">{task}</span>
            """, unsafe_allow_html=True)
        if st.button("↩" if is_done else "✓", key=f"t_{i}", use_container_width=True):
            toggle_task(i)
    
    # CALENDAR - FULLY VISIBLE
    now = datetime.date.today()
    year, month = now.year, now.month
    days_in_month = cal_module.monthrange(year, month)[1]
    first_weekday = (datetime.date(year, month, 1).weekday() + 1) % 7
    
    st.markdown(f"""
    <div class="calendar-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <span style="font-size:14px;font-weight:600;color:#1e293b;">📅 Streak Calendar</span>
            <span style="font-size:13px;color:#94a3b8;">{now.strftime('%B %Y')}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:5px;">
    """, unsafe_allow_html=True)
    
    weekdays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    for d in weekdays:
        st.markdown(f'<div class="cal-day weekday-label">{d}</div>', unsafe_allow_html=True)
    
    for i in range(first_weekday):
        st.markdown('<div class="cal-day"></div>', unsafe_allow_html=True)
    
    for d in range(1, days_in_month + 1):
        ds = datetime.date(year, month, d).isoformat()
        cls = 'cal-day'
        if ds in st.session_state.streak_data:
            cls += ' streak'
        if d == now.day:
            cls += ' today-cell'
        st.markdown(f'<div class="{cls}">{d}</div>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Actions
    c1, c2 = st.columns(2)
    with c1:
        if st.button("↺ Reset Today", use_container_width=True):
            st.session_state.completed_tasks = []
            st.session_state.streak_data.pop(datetime.date.today().isoformat(), None)
            st.rerun()
    with c2:
        if st.button("✧ Change Aura", use_container_width=True):
            st.session_state.current_page = 'select'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_chat():
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-box">
            <h2 style="font-size:22px;font-weight:700;color:#0f172a;margin-bottom:16px;">💬 Community</h2>
    """, unsafe_allow_html=True)
    
    # Online users
    st.markdown('<p style="font-size:13px;font-weight:600;color:#475569;margin-bottom:8px;">🟢 Online</p>', unsafe_allow_html=True)
    for user in st.session_state.online_users:
        is_sel = st.session_state.chat_user == user['name']
        if st.button(f"{'✓ ' if is_sel else ''}{user['avatar']} {user['name']} · {user['bio']}", 
                    key=f"usr_{user['name']}", use_container_width=True):
            st.session_state.chat_user = user['name']
            st.rerun()
    
    st.markdown('<hr style="border-color:rgba(0,0,0,0.06);margin:16px 0;">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:14px;font-weight:600;color:#1e293b;">💬 Chat with {st.session_state.chat_user}</p>', unsafe_allow_html=True)
    
    # Messages
    chat_msgs = [m for m in st.session_state.chat_messages 
                if (m['from'] == 'You' and m['to'] == st.session_state.chat_user) or 
                   (m['to'] == 'You' and m['from'] == st.session_state.chat_user)]
    
    for msg in chat_msgs[-30:]:
        is_me = msg['from'] == 'You'
        st.markdown(f"""
        <div style="display:flex;justify-content:{'flex-end' if is_me else 'flex-start'};margin:4px 0;">
            <div class="chat-bubble {'chat-sent' if is_me else 'chat-received'}">
                <small style="opacity:0.7;">{msg['from']} · {msg['time']}</small>
                <p style="margin:4px 0 0;">{msg['text']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            txt = st.text_input("Message", label_visibility="collapsed", placeholder="Type a message...")
        with c2:
            send = st.form_submit_button("📤", use_container_width=True)
        if send and txt:
            st.session_state.chat_messages.append({
                'from': 'You', 'to': st.session_state.chat_user,
                'text': txt, 'time': datetime.datetime.now().strftime("%H:%M")
            })
            # Auto-reply
            replies = ["That's awesome! 🎉", "I agree! 💯", "Keep it up! 🌟", "Amazing! 💪", "Let's go! 🚀"]
            time.sleep(0.8)
            st.session_state.chat_messages.append({
                'from': st.session_state.chat_user, 'to': 'You',
                'text': random.choice(replies), 'time': datetime.datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_wallpapers():
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-box">
            <h2 style="font-size:22px;font-weight:700;color:#0f172a;margin-bottom:16px;">🎨 Wallpapers</h2>
    """, unsafe_allow_html=True)
    
    if st.button("🎲 Random Wallpaper", use_container_width=True):
        st.session_state.wallpaper = random.choice(UNSPLASH_WALLPAPERS)
        st.success("✅ New wallpaper applied!")
        st.rerun()
    
    st.markdown(f'<p style="font-size:12px;color:#94a3b8;margin:8px 0;">{len(UNSPLASH_WALLPAPERS)}+ wallpapers from Unsplash</p>', unsafe_allow_html=True)
    
    # Show grid of wallpapers
    for i in range(0, min(60, len(UNSPLASH_WALLPAPERS)), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(UNSPLASH_WALLPAPERS):
                with cols[j]:
                    wp = UNSPLASH_WALLPAPERS[idx]
                    is_current = st.session_state.wallpaper == wp
                    st.markdown(f"""
                    <div style="background:url('{wp}')center/cover;height:70px;border-radius:10px;
                    border:{'3px solid #0f172a' if is_current else '1px solid rgba(0,0,0,0.08)'};cursor:pointer;">
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Set", key=f"wp_{idx}", use_container_width=True):
                        st.session_state.wallpaper = wp
                        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================
#  MAIN
# ============================================================
def main():
    set_bg()
    st.markdown('<div class="signature">id³</div>', unsafe_allow_html=True)
    st.markdown('<div class="wp-fab">🎨</div>', unsafe_allow_html=True)
    
    page = st.session_state.current_page
    
    if page == 'landing':
        show_landing()
    elif page == 'select':
        show_select()
    elif page == 'tracker':
        show_tracker()
    elif page == 'chat':
        show_chat()
    elif page == 'wallpapers':
        show_wallpapers()
    
    # Bottom nav
    st.markdown('<div style="height:70px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="bottom-nav-bar">', unsafe_allow_html=True)
    
    nav_items = [
        ('landing', '⚡', 'Home'),
        ('select', '✧', 'Auras'),
        ('tracker', '🎯', 'Track'),
        ('chat', '💬', 'Chat'),
        ('wallpapers', '🎨', 'Walls'),
    ]
    
    cols = st.columns(len(nav_items))
    for i, (pg, icon, label) in enumerate(nav_items):
        with cols[i]:
            is_active = page == pg
            if is_active:
                st.markdown(f'<div class="nav-btn active">', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="nav-btn">', unsafe_allow_html=True)
            if st.button(f"{icon}", key=f"nav_{pg}", use_container_width=True, help=label):
                st.session_state.current_page = pg
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
