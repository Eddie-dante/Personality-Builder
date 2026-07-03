# app.py - AuraRise Complete Application with 200+ Wallpapers
import streamlit as st
import random
import datetime
import time
import json
import os
import sys
import hashlib
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Aura Builder · id³",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
#  CUSTOM CSS - GLASS MORPHISM + BRIGHT THEMES
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        min-height: 100vh;
        transition: background 0.9s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    /* Signature watermark */
    .signature {
        position: fixed;
        bottom: 90px;
        right: 24px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 2.5px;
        color: #0f172a;
        opacity: 0.3;
        z-index: 999;
        background: rgba(255, 255, 255, 0.5);
        padding: 6px 16px;
        border-radius: 40px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        pointer-events: none;
    }
    
    /* Glass container */
    .glass-container {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(24px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(24px) saturate(1.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-radius: 32px !important;
        padding: 32px 28px !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.02) inset !important;
    }
    
    /* Landing */
    .landing-badge {
        display: inline-block;
        background: rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(0, 0, 0, 0.06);
        padding: 6px 18px;
        border-radius: 40px;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 24px;
    }
    
    .landing-title {
        font-size: clamp(34px, 5vw, 44px);
        font-weight: 700;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #0f172a 60%, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .tagline {
        color: #64748b;
        font-size: 15px;
        font-weight: 400;
        margin-bottom: 36px;
        letter-spacing: 0.2px;
    }
    
    /* Aura buttons */
    .aura-btn {
        padding: 16px 18px;
        background: rgba(255, 255, 255, 0.5);
        border: 1.5px solid rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.25s ease;
        display: flex;
        align-items: center;
        gap: 14px;
        position: relative;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        margin: 6px 0;
    }
    
    .aura-btn:hover {
        border-color: rgba(0, 0, 0, 0.12);
        background: rgba(255, 255, 255, 0.8);
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
    }
    
    .aura-btn.selected {
        border-color: #0f172a;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    
    /* Score ring */
    .score-ring-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    
    .score-ring {
        position: relative;
        width: 120px;
        height: 120px;
    }
    
    .score-ring svg {
        transform: rotate(-90deg);
    }
    
    /* Tasks */
    .task-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 14px;
        cursor: pointer;
        transition: all 0.25s ease;
        gap: 14px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        margin: 6px 0;
    }
    
    .task-item:hover {
        border-color: #e2e8f0;
        background: #fafbfc;
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    }
    
    .task-item.completed {
        opacity: 0.6;
        border-color: #f1f5f9;
    }
    
    .task-item.completed .task-text {
        text-decoration: line-through;
        color: #94a3b8;
    }
    
    .task-check {
        width: 24px;
        height: 24px;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
        transition: all 0.25s ease;
        background: #fff;
    }
    
    .task-item.completed .task-check {
        background: #0f172a;
        border-color: #0f172a;
        color: #fff;
    }
    
    /* Calendar */
    .cal-day {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 450;
        border-radius: 10px;
        background: rgba(0, 0, 0, 0.02);
        color: #94a3b8;
        transition: all 0.25s ease;
    }
    
    .cal-day.active {
        background: #0f172a;
        color: #fff;
        font-weight: 600;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.15);
    }
    
    .cal-day.today {
        border: 2px solid #0f172a;
        background: transparent;
        color: #0f172a;
        font-weight: 600;
    }
    
    /* Bottom navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 8px 5px;
        padding-bottom: max(8px, env(safe-area-inset-bottom));
        z-index: 1000;
        border-top: 1px solid rgba(0, 0, 0, 0.06);
        overflow-x: auto;
    }
    
    @media (min-width: 769px) {
        .bottom-nav {
            max-width: 600px;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 20px 20px 0 0;
        }
    }
    
    /* Wallpaper button */
    .wallpaper-fab {
        position: fixed;
        bottom: 90px;
        left: 20px;
        z-index: 999;
        background: rgba(15, 23, 42, 0.9);
        border: none;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    /* Counter chip */
    .counter-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 0, 0, 0.04);
        padding: 4px 14px 4px 12px;
        border-radius: 40px;
        font-size: 13px;
        color: #475569;
        border: 1px solid rgba(0, 0, 0, 0.04);
        margin-bottom: 18px;
    }
    
    /* Responsive */
    @media (max-width: 480px) {
        .glass-container {
            padding: 24px 18px !important;
            border-radius: 24px !important;
        }
        .landing-title {
            font-size: 32px;
        }
    }
    
    /* Streamlit overrides */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0 !important;
    }
    
    .stButton > button {
        width: 100%;
        padding: 16px !important;
        background: #0f172a !important;
        border: none !important;
        border-radius: 16px !important;
        color: #fff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.15) !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(15, 23, 42, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Secondary button */
    .btn-secondary button {
        background: transparent !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        color: #64748b !important;
        box-shadow: none !important;
    }
    
    .btn-secondary button:hover {
        background: rgba(0, 0, 0, 0.02) !important;
        border-color: rgba(0, 0, 0, 0.15) !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  200+ UNSPLASH WALLPAPERS
# ============================================================
UNSPLASH_WALLPAPERS = [
    # Abstract & Gradients (30)
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
    
    # Nature & Landscapes (40)
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
    
    # Minimal & Clean (30)
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
    
    # Dark & Moody (30)
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
    
    # Warm & Golden (25)
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "https://images.unsplash.com/photo-1474524955719-b7f5099ab369?w=1920&q=80",
    "https://images.unsplash.com/photo-1504198322253-cfa87a0ff25f?w=1920&q=80",
    "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=1920&q=80",
    "https://images.unsplash.com/photo-1487147264018-f937fba0c817?w=1920&q=80",
    
    # Cool & Blue (25)
    "https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=1920&q=80",
    "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?w=1920&q=80",
    "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1920&q=80",
    "https://images.unsplash.com/photo-1518459031867-a89b550b39f2?w=1920&q=80",
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    
    # Texture & Patterns (20)
    "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920&q=80",
    "https://images.unsplash.com/photo-1558470598-a5dda9640f68?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80",
    "https://images.unsplash.com/photo-1579546929662-711aa81148cf?w=1920&q=80",
    "https://images.unsplash.com/photo-1553356084-58ef4a67b2a7?w=1920&q=80",
]

# ============================================================
#  AURA DEFINITIONS (from original code)
# ============================================================
AURAS = {
    'cold': {
        'name': 'Cold Aura',
        'desc': 'Distant & unreadable',
        'gradient': 'linear-gradient(145deg, #e0f2fe 0%, #bae6fd 60%, #7dd3fc 100%)',
        'accent': '#0284c7',
        'emoji': '❄️',
        'tasks': [
            'Poker face — 2 min',
            'Pause 2s before replying',
            'Short neutral answers',
            'Slow, deliberate movements',
            'One hand in pocket'
        ]
    },
    'mystery': {
        'name': 'Mystery Aura',
        'desc': 'Quiet depth',
        'gradient': 'linear-gradient(145deg, #f3e8ff 0%, #d8b4fe 60%, #c084fc 100%)',
        'accent': '#7e22ce',
        'emoji': '🌙',
        'tasks': [
            'Avoid explaining yourself',
            'Answer then pause',
            'Change subject when probed',
            'Limited eye contact',
            'Leave rooms early'
        ]
    },
    'nonchalant': {
        'name': 'Nonchalant Aura',
        'desc': 'Unbothered energy',
        'gradient': 'linear-gradient(145deg, #fef3c7 0%, #fde68a 60%, #fcd34d 100%)',
        'accent': '#b45309',
        'emoji': '😌',
        'tasks': [
            'Shrug off drama lightly',
            'Reply late casually',
            'Relaxed open posture',
            '"We\'ll see" responses',
            'Skip 1 optional event'
        ]
    },
    'intense': {
        'name': 'Intense Aura',
        'desc': 'Sharp presence',
        'gradient': 'linear-gradient(145deg, #fee2e2 0%, #fca5a5 60%, #f87171 100%)',
        'accent': '#b91c1c',
        'emoji': '🔥',
        'tasks': [
            'Direct eye contact',
            'Sharp, concise speech',
            'Minimal smiling',
            'Controlled gestures',
            'Take space when standing'
        ]
    },
    'calm': {
        'name': 'Calm Aura',
        'desc': 'Peaceful energy',
        'gradient': 'linear-gradient(145deg, #d1fae5 0%, #6ee7b7 60%, #34d399 100%)',
        'accent': '#047857',
        'emoji': '🌊',
        'tasks': [
            'Slow diaphragmatic breathing',
            'Soft, warm voice tone',
            'Gentle movements',
            'Listen fully without interrupting',
            'No rushing — take your time'
        ]
    },
    'royal': {
        'name': 'Royal Aura',
        'desc': 'Natural authority',
        'gradient': 'linear-gradient(145deg, #fef9c3 0%, #fde047 60%, #facc15 100%)',
        'accent': '#854d0e',
        'emoji': '👑',
        'tasks': [
            'Upright posture always',
            'Measured, deliberate speech',
            'Don\'t rush to respond',
            'Others wait for you',
            'Head level, chin up'
        ]
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
if 'wallpaper_index' not in st.session_state:
    st.session_state.wallpaper_index = 0

# ============================================================
#  HELPERS
# ============================================================
def get_task_list():
    """Get combined task list from selected auras"""
    if not st.session_state.selected_auras:
        return []
    
    all_tasks = []
    for aura_key in st.session_state.selected_auras:
        if aura_key in AURAS:
            all_tasks.extend(AURAS[aura_key]['tasks'])
    
    unique = list(dict.fromkeys(all_tasks))
    return unique[:8]

def set_background():
    """Set wallpaper background"""
    wallpaper = st.session_state.wallpaper
    if not wallpaper.startswith('http'):
        wallpaper = random.choice(UNSPLASH_WALLPAPERS)
    
    st.markdown(f"""
    <style>
        .stApp {{
            background: url('{wallpaper}') center/cover fixed !important;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.3);
            z-index: -1;
        }}
    </style>
    """, unsafe_allow_html=True)

def add_signature():
    """Add id³ signature"""
    st.markdown('<div class="signature">id³</div>', unsafe_allow_html=True)

def add_wallpaper_button():
    """Add floating wallpaper button"""
    st.markdown("""
    <div class="wallpaper-fab" title="Change Wallpaper">🎨</div>
    """, unsafe_allow_html=True)

def show_page(page_name):
    """Navigate to a page"""
    st.session_state.current_page = page_name
    st.rerun()

# ============================================================
#  PAGES
# ============================================================
def show_landing():
    """Landing page"""
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-container" style="text-align: center;">
            <span class="landing-badge">✦ v2.0</span>
            <div style="font-size: 68px; line-height: 1; margin-bottom: 8px;">⚡</div>
            <h1 class="landing-title">Aura Builder</h1>
            <p class="tagline">Train your presence. <strong>Manifest your aura.</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Begin Journey", key="begin_btn", use_container_width=True):
            show_page('select')
    with col2:
        if st.button("Continue →", key="continue_btn", use_container_width=True):
            if st.session_state.selected_auras:
                show_page('tracker')
            else:
                show_page('select')

def show_select():
    """Aura selection page"""
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-container">
            <div style="margin-bottom: 20px;">
                <h2 style="font-size: 26px; font-weight: 700; letter-spacing: -0.5px; color: #0f172a;">Choose Your Aura</h2>
                <p style="color: #64748b; font-size: 14px; margin-top: 2px;">Select up to 2 to shape your presence</p>
            </div>
    """, unsafe_allow_html=True)
    
    # Counter chip
    selected_count = len(st.session_state.selected_auras)
    st.markdown(f"""
        <div class="counter-chip">
            <span>✧</span> <strong>{selected_count}</strong><span>/2 selected</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Aura buttons
    for aura_key, aura in AURAS.items():
        is_selected = aura_key in st.session_state.selected_auras
        col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
        with col1:
            st.markdown(f"<div style='font-size: 26px; padding-top: 12px;'>{aura['emoji']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="padding: 8px 0;">
                <strong style="color: #0f172a; font-size: 16px;">{aura['name']}</strong><br>
                <small style="color: #64748b;">{aura['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if is_selected:
                st.markdown("<div style='font-size: 18px; padding-top: 14px; color: #0f172a;'>✓</div>", unsafe_allow_html=True)
        
        if st.button("Select" if not is_selected else "Deselect", 
                    key=f"aura_{aura_key}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"):
            toggle_aura(aura_key)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Continue", key="confirm_auras", use_container_width=True):
            if st.session_state.selected_auras:
                show_page('tracker')
            else:
                st.warning("Select at least one aura")
    with col2:
        if st.button("← Back", key="back_landing", use_container_width=True):
            show_page('landing')

def toggle_aura(key):
    """Toggle aura selection"""
    if key in st.session_state.selected_auras:
        st.session_state.selected_auras.remove(key)
    elif len(st.session_state.selected_auras) < 2:
        st.session_state.selected_auras.append(key)
    st.rerun()

def show_tracker():
    """Main tracker page"""
    if not st.session_state.selected_auras:
        show_page('select')
        return
    
    primary_aura = AURAS.get(st.session_state.selected_auras[0])
    secondary_aura = AURAS.get(st.session_state.selected_auras[1]) if len(st.session_state.selected_auras) > 1 else None
    
    st.markdown("""
    <div style="max-width: 460px; margin: 0 auto;">
        <div class="glass-container">
    """, unsafe_allow_html=True)
    
    # Header
    if secondary_aura:
        title = f"{primary_aura['emoji']} {primary_aura['name']} + {secondary_aura['emoji']} {secondary_aura['name']}"
        subtitle = f"{primary_aura['desc']} + {secondary_aura['desc']}"
        badge = f"⚡ {primary_aura['emoji']} {secondary_aura['emoji']}"
    else:
        title = f"{primary_aura['emoji']} {primary_aura['name']}"
        subtitle = primary_aura['desc']
        badge = f"⚡ {primary_aura['emoji']}"
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
        <div>
            <h2 style="font-size: 22px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.2; color: #0f172a;">{title}</h2>
            <p style="color: #64748b; font-size: 13px; margin-top: 1px;">{subtitle}</p>
        </div>
        <div style="background: rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.04); padding: 4px 14px; border-radius: 40px; font-size: 11px; color: #475569; font-weight: 500;">{badge}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Score ring
    tasks = get_task_list()
    total = len(tasks)
    done = len([i for i in st.session_state.completed_tasks if i < total])
    pct = round((done / total) * 100) if total > 0 else 0
    
    circumference = 2 * 3.14159 * 52
    offset = circumference - (pct / 100) * circumference
    
    st.markdown(f"""
    <div class="score-ring-container">
        <div class="score-ring">
            <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="6"/>
                <circle cx="60" cy="60" r="52" fill="none" stroke="{primary_aura['accent']}" stroke-width="6" 
                        stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 34px; font-weight: 700; letter-spacing: -1px; line-height: 1; color: #0f172a;">{pct}%</div>
                <div style="font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 2px;">Aura Strength</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tasks
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <span style="font-size: 13px; font-weight: 600; color: #475569;">Today's Practice</span>
        <span style="color: #94a3b8; font-size: 13px;">{done}/{total} done</span>
    </div>
    """, unsafe_allow_html=True)
    
    for i, task in enumerate(tasks):
        is_completed = i in st.session_state.completed_tasks
        col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
        with col1:
            st.markdown(f"""
            <div class="task-check" style="{'background: #0f172a; border-color: #0f172a; color: #fff;' if is_completed else ''}">
                {'✓' if is_completed else ''}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="padding: 8px 0;">
                <span class="task-text" style="{'text-decoration: line-through; color: #94a3b8;' if is_completed else 'color: #1e293b;'}">
                    {task}
                </span>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if st.button("✓" if not is_completed else "↩", key=f"task_{i}", use_container_width=True):
                toggle_task(i)
    
    # Calendar
    st.markdown("### 📅 Streak Calendar")
    render_calendar()
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Reset Today", use_container_width=True, key="reset_day"):
            st.session_state.completed_tasks = []
            today = datetime.date.today().isoformat()
            if today in st.session_state.streak_data:
                del st.session_state.streak_data[today]
            st.rerun()
    with col2:
        if st.button("✧ Change Aura", use_container_width=True, key="change_aura"):
            show_page('select')
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def toggle_task(i):
    """Toggle task completion"""
    if i in st.session_state.completed_tasks:
        st.session_state.completed_tasks.remove(i)
    else:
        st.session_state.completed_tasks.append(i)
    
    tasks = get_task_list()
    total = len(tasks)
    done = len([x for x in st.session_state.completed_tasks if x < total])
    today = datetime.date.today().isoformat()
    
    if done == total and total > 0:
        st.session_state.streak_data[today] = True
    else:
        if today in st.session_state.streak_data:
            del st.session_state.streak_data[today]
    
    st.rerun()

def render_calendar():
    """Render streak calendar"""
    now = datetime.date.today()
    year = now.year
    month = now.month
    
    st.markdown(f"**{now.strftime('%B %Y')}**")
    
    days_in_month = (datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)).day if month < 12 else 31
    first_day = datetime.date(year, month, 1).weekday()
    first_day = (first_day + 1) % 7  # Adjust to Sunday start
    
    weekdays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    cols = st.columns(7)
    for i, day in enumerate(weekdays):
        with cols[i]:
            st.markdown(f"<small style='color: #94a3b8;'>{day}</small>", unsafe_allow_html=True)
    
    cols = st.columns(7)
    day_count = 0
    
    for i in range(first_day):
        with cols[i]:
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    for d in range(1, days_in_month + 1):
        col_idx = (first_day + d - 1) % 7
        date_str = datetime.date(year, month, d).isoformat()
        is_active = date_str in st.session_state.streak_data
        is_today = d == now.day and month == now.month and year == now.year
        
        with cols[col_idx]:
            if is_active:
                st.markdown(f"""
                <div class="cal-day active" style="background: {'#0f172a' if not st.session_state.selected_auras else AURAS.get(st.session_state.selected_auras[0], {}).get('accent', '#0f172a')}; color: #fff; border-radius: 10px; padding: 4px; text-align: center;">
                    {d}
                </div>
                """, unsafe_allow_html=True)
            elif is_today:
                st.markdown(f"""
                <div class="cal-day today" style="border: 2px solid #0f172a; border-radius: 10px; padding: 4px; text-align: center;">
                    {d}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="cal-day" style="border-radius: 10px; padding: 4px; text-align: center; color: #94a3b8;">
                    {d}
                </div>
                """, unsafe_allow_html=True)

def show_wallpaper_selector():
    """Wallpaper selection page"""
    st.markdown("## 🎨 Choose Your Wallpaper")
    st.markdown(f"*{len(UNSPLASH_WALLPAPERS)}+ stunning wallpapers from Unsplash*")
    
    # Categories
    categories = {
        "Abstract & Gradients": list(range(0, 10)),
        "Nature & Landscapes": list(range(10, 20)),
        "Minimal & Clean": list(range(20, 30)),
        "Dark & Moody": list(range(30, 40)),
        "Warm & Golden": list(range(40, 45)),
        "Cool & Blue": list(range(45, 50)),
    }
    
    for cat_name, indices in categories.items():
        st.markdown(f"### {cat_name}")
        cols = st.columns(5)
        for i, idx in enumerate(indices[:5]):
            with cols[i]:
                if idx < len(UNSPLASH_WALLPAPERS):
                    wp_url = UNSPLASH_WALLPAPERS[idx]
                    st.markdown(f"""
                    <div style="background: url('{wp_url}') center/cover; 
                              height: 80px; border-radius: 12px; cursor: pointer;
                              border: {'3px solid #0f172a' if st.session_state.wallpaper == wp_url else '1px solid rgba(0,0,0,0.1)'};">
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Select", key=f"wp_{idx}", use_container_width=True):
                        st.session_state.wallpaper = wp_url
                        st.session_state.wallpaper_index = idx
                        st.success("✅ Wallpaper updated!")
                        st.rerun()
    
    # Random button
    if st.button("🎲 Random Wallpaper", use_container_width=True):
        st.session_state.wallpaper = random.choice(UNSPLASH_WALLPAPERS)
        st.success("✅ Random wallpaper applied!")
        st.rerun()
    
    # Pagination
    st.markdown(f"**Showing {min(30, len(UNSPLASH_WALLPAPERS))} of {len(UNSPLASH_WALLPAPERS)} wallpapers**")
    
    # Show all in a grid
    with st.expander("📸 Browse All Wallpapers"):
        cols = st.columns(6)
        for i, wp_url in enumerate(UNSPLASH_WALLPAPERS):
            with cols[i % 6]:
                st.markdown(f"""
                <div style="background: url('{wp_url}') center/cover; 
                          height: 60px; border-radius: 8px; margin: 2px 0;
                          border: {'2px solid #0f172a' if st.session_state.wallpaper == wp_url else '1px solid rgba(0,0,0,0.05)'};">
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Set", key=f"all_wp_{i}", use_container_width=True):
                    st.session_state.wallpaper = wp_url
                    st.session_state.wallpaper_index = i
                    st.rerun()

# ============================================================
#  BOTTOM NAVIGATION
# ============================================================
def render_bottom_nav():
    """Render bottom navigation bar"""
    current = st.session_state.current_page
    
    nav_items = [
        ('landing', '⚡', 'Home'),
        ('select', '✧', 'Auras'),
        ('tracker', '🎯', 'Tracker'),
        ('wallpaper', '🎨', 'Walls'),
    ]
    
    cols = st.columns(len(nav_items))
    for i, (page, icon, label) in enumerate(nav_items):
        with cols[i]:
            is_active = current == page
            if st.button(f"{icon} {label}", key=f"nav_{page}", use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.current_page = page
                st.rerun()

# ============================================================
#  MAIN
# ============================================================
def main():
    """Main application"""
    set_background()
    add_signature()
    add_wallpaper_button()
    
    current_page = st.session_state.current_page
    
    # Page content
    if current_page == 'landing':
        show_landing()
    elif current_page == 'select':
        show_select()
    elif current_page == 'tracker':
        show_tracker()
    elif current_page == 'wallpaper':
        show_wallpaper_selector()
    
    # Padding for bottom nav
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    
    # Bottom navigation
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    render_bottom_nav()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
