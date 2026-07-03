# app.py - AuraRise Complete Application (Python 3.14 Compatible)
import streamlit as st
import random
import datetime
import time
import json
import os
import sys
import hashlib
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="AuraRise - Level Up Your Life",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for amazing vibes - FULLY RESPONSIVE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Responsive title */
    .title-text {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 900;
        background: linear-gradient(135deg, #00c6ff, #a855f7, #f5a623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.3); }
    }
    
    /* Watermark - visible on all pages */
    .watermark {
        position: fixed;
        bottom: 80px;
        right: 20px;
        color: rgba(255,255,255,0.3);
        font-size: clamp(10px, 1.5vw, 13px);
        font-style: italic;
        z-index: 999;
        pointer-events: none;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(168,85,247,0.3);
        background: rgba(0,0,0,0.3);
        padding: 5px 15px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
    }
    
    /* Wallpaper button - fixed position */
    .wallpaper-fab {
        position: fixed;
        bottom: 80px;
        left: 20px;
        z-index: 999;
        background: linear-gradient(135deg, #a855f7, #00c6ff);
        border: none;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(168,85,247,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
        animation: float 3s ease-in-out infinite;
    }
    
    .wallpaper-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(168,85,247,0.6);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Aura cards - responsive grid */
    .aura-card {
        background: rgba(20,20,40,0.8);
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: clamp(15px, 2vw, 25px);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(10px);
        height: 100%;
    }
    
    .aura-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        border-color: rgba(0,198,255,0.5);
    }
    
    .aura-card.selected {
        border: 2px solid #00c6ff;
        box-shadow: 0 0 40px rgba(0,198,255,0.3);
        background: rgba(0,198,255,0.1);
    }
    
    /* Chat messages */
    .chat-message {
        padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 18px);
        border-radius: 20px;
        margin: 8px 0;
        max-width: 75%;
        animation: messageSlide 0.3s ease;
    }
    
    @keyframes messageSlide {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message.sent {
        background: linear-gradient(135deg, #00c6ff, #0099cc);
        margin-left: auto;
        color: #000;
        font-weight: 500;
    }
    
    .chat-message.received {
        background: rgba(255,255,255,0.1);
        margin-right: auto;
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    /* Responsive maze */
    .maze-wrapper {
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
        touch-action: none;
        user-select: none;
        -webkit-user-select: none;
    }
    
    .maze-container {
        display: inline-block;
        border: 3px solid rgba(168,85,247,0.5);
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 0 40px rgba(168,85,247,0.2);
        background: rgba(0,0,0,0.3);
        width: 100%;
    }
    
    .maze-row {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    .maze-cell {
        aspect-ratio: 1;
        width: calc(100% / var(--maze-size));
        max-width: 50px;
        max-height: 50px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255,255,255,0.08);
        font-size: clamp(14px, 2.5vw, 22px);
        transition: all 0.15s;
        border-radius: 3px;
        margin: 1px;
        cursor: pointer;
    }
    
    .maze-wall {
        background: linear-gradient(135deg, #2a2a3e, #1a1a2e);
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    .maze-path {
        background: rgba(0,0,0,0.3);
    }
    
    .maze-player {
        background: linear-gradient(135deg, #00c6ff, #0099cc);
        box-shadow: 0 0 25px rgba(0,198,255,0.6);
        animation: playerPulse 1s ease-in-out infinite;
        border-radius: 8px;
        z-index: 10;
    }
    
    .maze-goal {
        background: linear-gradient(135deg, #f5a623, #ffd700);
        animation: goalGlow 1.5s ease-in-out infinite;
        border-radius: 8px;
    }
    
    @keyframes playerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes goalGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(245,166,35,0.5); }
        50% { box-shadow: 0 0 35px rgba(245,166,35,0.9); }
    }
    
    /* Progress bars */
    .progress-bar {
        height: clamp(8px, 1.5vw, 12px);
        border-radius: 6px;
        background: rgba(255,255,255,0.08);
        overflow: hidden;
        margin: 5px 0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Cards */
    .stat-card {
        background: rgba(20,20,40,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: clamp(15px, 2vw, 20px);
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border-color: rgba(0,198,255,0.3);
    }
    
    .achievement-card {
        background: rgba(20,20,40,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: clamp(15px, 2vw, 25px);
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }
    
    .achievement-card.unlocked {
        border-color: rgba(245,166,35,0.5);
        box-shadow: 0 0 30px rgba(245,166,35,0.2);
    }
    
    /* Bottom Navigation - RESPONSIVE */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(12, 12, 25, 0.95);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 8px 5px;
        padding-bottom: max(8px, env(safe-area-inset-bottom));
        z-index: 1000;
        border-top: 1px solid rgba(255,255,255,0.1);
        overflow-x: auto;
        gap: 5px;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        cursor: pointer;
        color: #888;
        transition: 0.2s;
        font-size: clamp(0.6rem, 1.5vw, 0.75rem);
        font-weight: 500;
        padding: 6px 10px;
        border-radius: 12px;
        background: none;
        border: none;
        font-family: 'Poppins', sans-serif;
        white-space: nowrap;
        min-width: 50px;
        flex-shrink: 0;
    }
    
    .nav-item.active {
        color: #00c6ff;
    }
    
    .nav-item .nav-icon {
        font-size: clamp(1rem, 2.5vw, 1.4rem);
        transition: 0.2s;
    }
    
    .nav-item.active .nav-icon {
        text-shadow: 0 0 20px rgba(0,198,255,0.7);
    }
    
    /* Online dot */
    .online-dot {
        width: 8px;
        height: 8px;
        background: #4ade80;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: onlinePulse 2s infinite;
    }
    
    @keyframes onlinePulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.5); }
        50% { box-shadow: 0 0 0 6px rgba(74,222,128,0); }
    }
    
    /* Particle effects */
    .particle {
        position: fixed;
        pointer-events: none;
        z-index: 9999;
        animation: particleUp 1s ease-out forwards;
        font-size: 20px;
    }
    
    @keyframes particleUp {
        0% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
        100% { opacity: 0; transform: translateY(-150px) scale(0.3) rotate(180deg); }
    }
    
    /* Media queries for responsiveness */
    @media (max-width: 768px) {
        .maze-cell {
            max-width: 35px;
            max-height: 35px;
            font-size: 14px;
        }
        
        .desktop-only {
            display: none !important;
        }
        
        .bottom-nav {
            padding: 6px 2px;
        }
        
        .nav-item {
            padding: 4px 6px;
        }
    }
    
    @media (min-width: 769px) {
        .mobile-only {
            display: none !important;
        }
        
        .bottom-nav {
            max-width: 600px;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 20px 20px 0 0;
        }
    }
    
    @media (min-width: 1024px) {
        .bottom-nav {
            max-width: 800px;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.15);
        border-radius: 4px;
    }
    
    .user-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'app_data' not in st.session_state:
    st.session_state.app_data = {
        'phase': 'dashboard',
        'selected_auras': [],
        'aura_stats': {},
        'user': {
            'level': 1,
            'xp': 0,
            'xp_to_next': 100,
            'aura_coins': 500,
            'streak': 0,
            'last_active': None,
            'avatar': '😊',
            'unlocked_avatars': ['😊'],
            'wallpaper': 'default',
            'theme': 'default'
        },
        'quests': [],
        'daily_quests': [],
        'daily_quest_date': None,
        'achievements': [
            {'id': 'first_quest', 'name': 'First Step', 'desc': 'Complete 1 quest', 'icon': '👣', 'unlocked': False},
            {'id': 'streak3', 'name': 'Streak Starter', 'desc': '3-day streak', 'icon': '🔥', 'unlocked': False},
            {'id': 'streak7', 'name': 'Weekly Warrior', 'desc': '7-day streak', 'icon': '🔥', 'unlocked': False},
            {'id': 'quest10', 'name': 'Quest Champion', 'desc': 'Complete 10 quests', 'icon': '🏅', 'unlocked': False},
            {'id': 'maze3', 'name': 'Maze Runner', 'desc': 'Complete 3 mazes', 'icon': '🧩', 'unlocked': False},
            {'id': 'maze10', 'name': 'Maze Master', 'desc': 'Complete 10 mazes', 'icon': '🧩', 'unlocked': False},
            {'id': 'aura100', 'name': 'Aura Apprentice', 'desc': 'Reach 100 Aura Score', 'icon': '✨', 'unlocked': False},
            {'id': 'aura250', 'name': 'Aura Master', 'desc': 'Reach 250 Aura Score', 'icon': '🌟', 'unlocked': False},
        ],
        'journal': [],
        'total_quests': 0,
        'total_mazes': 0,
        'aura_history': [],
        'chat_messages': [],
        'online_users': [
            {'name': 'Edwin', 'avatar': '🦾', 'status': 'online', 'bio': 'Creator of AuraRise'},
            {'name': 'Alex', 'avatar': '🧑‍💻', 'status': 'online', 'bio': 'Focus master'},
            {'name': 'Maya', 'avatar': '👩‍🎨', 'status': 'online', 'bio': 'Creative spirit'},
            {'name': 'Zane', 'avatar': '🦸', 'status': 'online', 'bio': 'Courage warrior'},
            {'name': 'Luna', 'avatar': '🌙', 'status': 'online', 'bio': 'Intuition guide'},
        ],
        'current_chat_user': 'Edwin',
        'current_page': 'home'
    }

# Aura definitions
AURAS = [
    {'id': 'focus', 'name': 'Focus', 'icon': '🎯', 'color': '#ff6b6b', 'desc': 'Laser-sharp concentration'},
    {'id': 'creativity', 'name': 'Creativity', 'icon': '🎨', 'color': '#f06595', 'desc': 'Unleash imagination'},
    {'id': 'discipline', 'name': 'Discipline', 'icon': '🧘', 'color': '#748ffc', 'desc': 'Consistent self-control'},
    {'id': 'vitality', 'name': 'Vitality', 'icon': '⚡', 'color': '#ffd43b', 'desc': 'Radiant energy'},
    {'id': 'empathy', 'name': 'Empathy', 'icon': '🤝', 'color': '#ff8787', 'desc': 'Deep connection'},
    {'id': 'resilience', 'name': 'Resilience', 'icon': '🛡️', 'color': '#20c997', 'desc': 'Bounce back stronger'},
    {'id': 'courage', 'name': 'Courage', 'icon': '🦁', 'color': '#ff922b', 'desc': 'Face fears boldly'},
    {'id': 'mindfulness', 'name': 'Mindfulness', 'icon': '🧘‍♀️', 'color': '#63e6be', 'desc': 'Live in the now'},
]

# Wallpapers with CSS gradients
WALLPAPERS = {
    'default': 'linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0a0a1a 100%)',
    'focus': 'linear-gradient(135deg, #1a0a0a 0%, #3e1a1a 50%, #1a0a0a 100%)',
    'creativity': 'linear-gradient(135deg, #0a1a0a 0%, #1a3e1a 50%, #0a1a0a 100%)',
    'vitality': 'linear-gradient(135deg, #1a1a0a 0%, #3e3e1a 50%, #1a1a0a 100%)',
    'courage': 'linear-gradient(135deg, #1a0a1a 0%, #3e1a3e 50%, #1a0a1a 100%)',
    'mindfulness': 'linear-gradient(135deg, #0a1a1a 0%, #1a3e3e 50%, #0a1a1a 100%)',
    'discipline': 'linear-gradient(135deg, #0a0a2a 0%, #1a1a4e 50%, #0a0a2a 100%)',
    'balance': 'linear-gradient(135deg, #1a1a0a 0%, #3e3e1a 50%, #1a1a0a 100%)',
    'adventure': 'linear-gradient(135deg, #0a1a1a 0%, #1a3e3e 50%, #0a1a1a 100%)',
    'empathy': 'linear-gradient(135deg, #1a0a0a 0%, #3e1a1a 50%, #1a0a0a 100%)',
    'resilience': 'linear-gradient(135deg, #1a1a1a 0%, #3e3e3e 50%, #1a1a1a 100%)',
    'leadership': 'linear-gradient(135deg, #0a0a1a 0%, #2a2a4e 50%, #0a0a1a 100%)',
}

def get_wallpaper():
    """Get current wallpaper"""
    wp = st.session_state.app_data['user'].get('wallpaper', 'default')
    return WALLPAPERS.get(wp, WALLPAPERS['default'])

def set_background():
    """Apply dynamic background"""
    wallpaper = get_wallpaper()
    st.markdown(f"""
    <style>
        .stApp {{
            background: {wallpaper} !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def spawn_particles(emoji, count=10):
    """Spawn particle effects"""
    particles_js = ""
    for i in range(count):
        left = random.randint(20, 80)
        delay = random.random() * 0.5
        particles_js += f"""
        setTimeout(() => {{
            const p{i} = document.createElement('div');
            p{i}.className = 'particle';
            p{i}.textContent = '{emoji}';
            p{i}.style.left = '{left}%';
            p{i}.style.top = '{random.randint(30, 60)}%';
            document.body.appendChild(p{i});
            setTimeout(() => p{i}.remove(), 1000);
        }}, {int(delay * 1000)});
        """
    
    st.markdown(f"<script>{particles_js}</script>", unsafe_allow_html=True)

def add_watermark():
    """Add watermark"""
    st.markdown(
        '<div class="watermark">by WeGEM (Edwin) 🦾</div>',
        unsafe_allow_html=True
    )

def add_wallpaper_button():
    """Add floating wallpaper button"""
    st.markdown("""
    <button class="wallpaper-fab" onclick="document.getElementById('wallpaper-btn').click()" title="Change Wallpaper">
        🎨
    </button>
    <div style="display:none;">
    """, unsafe_allow_html=True)
    if st.button("🎨", key="wallpaper-btn"):
        st.session_state.app_data['current_page'] = 'wallpaper'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def calc_aura_score():
    """Calculate total aura score"""
    return sum(st.session_state.app_data['aura_stats'].values())

def add_xp(amount, aura_id=None):
    """Add XP and handle level ups"""
    data = st.session_state.app_data
    data['user']['xp'] += amount
    
    if aura_id and aura_id in data['aura_stats']:
        data['aura_stats'][aura_id] += amount // 8
    
    leveled_up = False
    while data['user']['xp'] >= data['user']['xp_to_next']:
        data['user']['xp'] -= data['user']['xp_to_next']
        data['user']['level'] += 1
        data['user']['xp_to_next'] = int(data['user']['xp_to_next'] * 1.45)
        data['user']['aura_coins'] += data['user']['level'] * 18
        leveled_up = True
    
    if leveled_up:
        st.balloons()
        spawn_particles('🎉', 20)
        st.success(f"🎉 Level Up! You're now Level {data['user']['level']}!")
    
    today = datetime.date.today().isoformat()
    if data['user']['last_active'] != today:
        if data['user']['last_active']:
            last = datetime.date.fromisoformat(data['user']['last_active'])
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            if last == yesterday:
                data['user']['streak'] += 1
                if data['user']['streak'] % 7 == 0:
                    data['user']['aura_coins'] += 50
                    spawn_particles('🔥', 15)
                    st.success(f"🔥 {data['user']['streak']}-day streak! Bonus +50 coins!")
            else:
                data['user']['streak'] = 1
        else:
            data['user']['streak'] = 1
        data['user']['last_active'] = today
    
    data['aura_history'].append({
        'date': today,
        'score': calc_aura_score()
    })
    
    check_achievements()

def check_achievements():
    """Check and unlock achievements"""
    data = st.session_state.app_data
    for ach in data['achievements']:
        if ach['unlocked']:
            continue
        
        if ach['id'] == 'first_quest' and data['total_quests'] >= 1:
            ach['unlocked'] = True
        elif ach['id'] == 'streak3' and data['user']['streak'] >= 3:
            ach['unlocked'] = True
        elif ach['id'] == 'streak7' and data['user']['streak'] >= 7:
            ach['unlocked'] = True
        elif ach['id'] == 'quest10' and data['total_quests'] >= 10:
            ach['unlocked'] = True
        elif ach['id'] == 'maze3' and data['total_mazes'] >= 3:
            ach['unlocked'] = True
        elif ach['id'] == 'maze10' and data['total_mazes'] >= 10:
            ach['unlocked'] = True
        elif ach['id'] == 'aura100' and calc_aura_score() >= 100:
            ach['unlocked'] = True
        elif ach['id'] == 'aura250' and calc_aura_score() >= 250:
            ach['unlocked'] = True
        
        if ach['unlocked']:
            data['user']['aura_coins'] += 40
            spawn_particles(ach['icon'], 10)
            st.toast(f"🏆 Achievement Unlocked: {ach['name']}!")

def generate_daily_quests():
    """Generate daily quests"""
    data = st.session_state.app_data
    today = datetime.date.today().isoformat()
    
    if data['daily_quest_date'] == today and data['daily_quests']:
        return
    
    daily_pool = [
        {'title': 'Drink 8 glasses of water', 'xp': 15, 'aura': 'vitality'},
        {'title': '10 min meditation', 'xp': 20, 'aura': 'mindfulness'},
        {'title': 'Read for 30 minutes', 'xp': 25, 'aura': 'focus'},
        {'title': 'Write in journal', 'xp': 15, 'aura': 'mindfulness'},
        {'title': 'Go for a 20 min walk', 'xp': 20, 'aura': 'vitality'},
        {'title': 'Practice a skill for 1 hour', 'xp': 35, 'aura': 'discipline'},
        {'title': 'Have a deep conversation', 'xp': 25, 'aura': 'empathy'},
        {'title': 'Try something new', 'xp': 30, 'aura': 'creativity'},
        {'title': 'Face a small fear', 'xp': 30, 'aura': 'courage'},
        {'title': 'Do a random act of kindness', 'xp': 20, 'aura': 'empathy'},
    ]
    
    selected = random.sample(daily_pool, min(3, len(daily_pool)))
    data['daily_quests'] = []
    for i, quest in enumerate(selected):
        data['daily_quests'].append({
            'id': f"daily_{today}_{i}",
            'title': quest['title'],
            'xp': quest['xp'],
            'aura': quest['aura'],
            'completed': False,
            'date': today
        })
    data['daily_quest_date'] = today

def generate_maze(size=9):
    """Generate a solvable maze"""
    if size % 2 == 0:
        size += 1
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    def carve(r, c):
        grid[r][c] = 0
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 < nr < size-1 and 0 < nc < size-1 and grid[nr][nc] == 1:
                grid[r + dr//2][c + dc//2] = 0
                carve(nr, nc)
    
    carve(1, 1)
    grid[size-2][size-2] = 2
    
    if grid[size-3][size-2] == 1 and grid[size-2][size-3] == 1:
        grid[size-3][size-2] = 0
    
    return grid

if 'maze' not in st.session_state:
    st.session_state.maze = generate_maze(9)
    st.session_state.player_pos = [1, 1]
    st.session_state.maze_size = 9
    st.session_state.last_drag = None

def render_maze_html(grid, player_pos):
    """Render maze with drag support"""
    size = len(grid)
    html = f'<div class="maze-wrapper"><div class="maze-container" style="--maze-size: {size};">'
    
    for r in range(size):
        html += '<div class="maze-row">'
        for c in range(size):
            cell_id = f"cell_{r}_{c}"
            cell_class = 'maze-wall'
            content = ''
            
            if grid[r][c] == 0:
                cell_class = 'maze-path'
            elif grid[r][c] == 2:
                cell_class = 'maze-goal'
                content = '🏁'
            
            if r == player_pos[0] and c == player_pos[1]:
                cell_class = 'maze-player'
                content = '🦾'
            
            html += f'<div class="maze-cell {cell_class}" id="{cell_id}" data-r="{r}" data-c="{c}">{content}</div>'
        html += '</div>'
    
    html += '</div></div>'
    
    # Add drag and click handling JavaScript
    html += """
    <script>
    (function() {
        const mazeContainer = document.querySelector('.maze-container');
        if (!mazeContainer) return;
        
        let isDragging = false;
        let startX = 0;
        let startY = 0;
        let lastMoveTime = 0;
        
        function sendDirection(direction) {
            const now = Date.now();
            if (now - lastMoveTime < 150) return;
            lastMoveTime = now;
            
            const input = document.getElementById('maze-direction-input');
            if (input) {
                input.value = direction;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(() => { input.value = ''; }, 100);
            }
        }
        
        // Touch events for drag
        mazeContainer.addEventListener('touchstart', function(e) {
            isDragging = true;
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            e.preventDefault();
        }, { passive: false });
        
        mazeContainer.addEventListener('touchmove', function(e) {
            if (!isDragging) return;
            e.preventDefault();
            
            const dx = e.touches[0].clientX - startX;
            const dy = e.touches[0].clientY - startY;
            const threshold = 20;
            
            if (Math.abs(dx) > threshold || Math.abs(dy) > threshold) {
                if (Math.abs(dx) > Math.abs(dy)) {
                    sendDirection(dx > 0 ? 'right' : 'left');
                } else {
                    sendDirection(dy > 0 ? 'down' : 'up');
                }
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            }
        }, { passive: false });
        
        mazeContainer.addEventListener('touchend', function() {
            isDragging = false;
        });
        
        // Mouse events for drag
        mazeContainer.addEventListener('mousedown', function(e) {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
        });
        
        mazeContainer.addEventListener('mousemove', function(e) {
            if (!isDragging) return;
            
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            const threshold = 15;
            
            if (Math.abs(dx) > threshold || Math.abs(dy) > threshold) {
                if (Math.abs(dx) > Math.abs(dy)) {
                    sendDirection(dx > 0 ? 'right' : 'left');
                } else {
                    sendDirection(dy > 0 ? 'down' : 'up');
                }
                startX = e.clientX;
                startY = e.clientY;
            }
        });
        
        mazeContainer.addEventListener('mouseup', function() {
            isDragging = false;
        });
        
        mazeContainer.addEventListener('mouseleave', function() {
            isDragging = false;
        });
        
        // Click on individual cells
        document.querySelectorAll('.maze-cell').forEach(cell => {
            cell.addEventListener('click', function() {
                const r = parseInt(this.dataset.r);
                const c = parseInt(this.dataset.c);
                const playerR = ''' + str(player_pos[0]) + ''';
                const playerC = ''' + str(player_pos[1]) + ''';
                
                const dr = r - playerR;
                const dc = c - playerC;
                
                if (Math.abs(dr) + Math.abs(dc) === 1) {
                    if (dr === -1) sendDirection('up');
                    else if (dr === 1) sendDirection('down');
                    else if (dc === -1) sendDirection('left');
                    else if (dc === 1) sendDirection('right');
                }
            });
        });
    })();
    </script>
    """
    
    return html

def move_player(direction):
    """Move player in maze"""
    r, c = st.session_state.player_pos
    maze = st.session_state.maze
    
    if direction == 'up' and r > 0 and maze[r-1][c] != 1:
        st.session_state.player_pos = [r-1, c]
    elif direction == 'down' and r < len(maze)-1 and maze[r+1][c] != 1:
        st.session_state.player_pos = [r+1, c]
    elif direction == 'left' and c > 0 and maze[r][c-1] != 1:
        st.session_state.player_pos = [r, c-1]
    elif direction == 'right' and c < len(maze[0])-1 and maze[r][c+1] != 1:
        st.session_state.player_pos = [r, c+1]
    
    if maze[st.session_state.player_pos[0]][st.session_state.player_pos[1]] == 2:
        st.session_state.app_data['total_mazes'] += 1
        coins_earned = random.randint(20, 50)
        st.session_state.app_data['user']['aura_coins'] += coins_earned
        aura = st.session_state.app_data['selected_auras'][0] if st.session_state.app_data['selected_auras'] else None
        add_xp(40, aura)
        check_achievements()
        spawn_particles('🧩', 15)
        st.success(f"🧩 Maze completed! +40 XP +{coins_earned} coins!")
        st.balloons()
        st.session_state.maze = generate_maze(st.session_state.maze_size)
        st.session_state.player_pos = [1, 1]
        st.rerun()

def show_home():
    """Home page"""
    st.markdown('<h1 class="title-text">AuraRise</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color: #888; font-size: clamp(0.9rem, 1.5vw, 1.1rem);">Shape your energy. Master discipline, confidence, and more. 🦾</p>', unsafe_allow_html=True)
    
    data = st.session_state.app_data
    
    if not data['selected_auras']:
        st.markdown("### 🌟 Select Your Auras to Begin")
        st.markdown("*Choose the energies you want to cultivate*")
        
        cols = st.columns(4)
        for i, aura in enumerate(AURAS):
            with cols[i % 4]:
                selected = aura['id'] in data['selected_auras']
                st.markdown(f"""
                <div class="aura-card {'selected' if selected else ''}">
                    <div style="font-size: clamp(2rem, 4vw, 3rem);">{aura['icon']}</div>
                    <h4 style="font-size: clamp(0.9rem, 1.5vw, 1.1rem);">{aura['name']}</h4>
                    <small style="color: #888; font-size: clamp(0.7rem, 1vw, 0.85rem);">{aura['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{'✅' if selected else 'Select'} {aura['name']}", key=f"aura_{aura['id']}", use_container_width=True):
                    if selected:
                        data['selected_auras'].remove(aura['id'])
                        if aura['id'] in data['aura_stats']:
                            del data['aura_stats'][aura['id']]
                    else:
                        data['selected_auras'].append(aura['id'])
                        data['aura_stats'][aura['id']] = random.randint(5, 20)
                    st.rerun()
        
        if data['selected_auras']:
            st.success(f"✨ {len(data['selected_auras'])} auras selected!")
            if st.button("🚀 Start Your Journey", use_container_width=True, type="primary"):
                st.rerun()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        score = calc_aura_score()
        tier = '🌟 Legend' if score >= 250 else '✨ Master' if score >= 100 else '🔮 Adept' if score >= 50 else '🌱 Novice'
        
        st.markdown(f"""
        <div style="text-align: center; padding: clamp(15px, 3vw, 30px);">
            <div style="font-size: clamp(3rem, 8vw, 5rem); font-weight: 900; background: linear-gradient(135deg, #00c6ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;" class="neon-text">
                {score}
            </div>
            <div style="font-size: clamp(1rem, 2vw, 1.2rem); margin-top: -10px;">⚡ Aura Score</div>
            <div class="user-badge" style="background: rgba(255,255,255,0.1); margin-top: 10px;">{tier}</div>
        </div>
        """, unsafe_allow_html=True)
        
        xp_pct = min(data['user']['xp'] / data['user']['xp_to_next'] * 100, 100)
        st.markdown(f"""
        <div style="margin: 20px 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>⚡ XP Progress</span>
                <span>{data['user']['xp']} / {data['user']['xp_to_next']}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {xp_pct}%; background: linear-gradient(90deg, #f5a623, #ffd700);"></div>
            </div>
            <div style="text-align: center; margin-top: 5px;">⭐ Level {data['user']['level']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Aura Progress")
        for aura_id in data['selected_auras']:
            aura = next((a for a in AURAS if a['id'] == aura_id), None)
            if aura:
                val = data['aura_stats'].get(aura_id, 0)
                pct = min(val / 50 * 100, 100)
                st.markdown(f"""
                <div style="margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>{aura['icon']} {aura['name']}</span>
                        <span style="font-weight: 600;">{val}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {pct}%; background: {aura['color']};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Stats")
        
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: clamp(1.5rem, 3vw, 2rem);">{data['user']['avatar']}</div>
            <h4>Level {data['user']['level']}</h4>
            <p>🪙 {data['user']['aura_coins']} coins</p>
            <p>🔥 {data['user']['streak']} day streak</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 10px;">
            <div style="font-size: clamp(1.5rem, 3vw, 2rem);">🎯</div>
            <h4>{data['total_quests']}</h4>
            <p>Quests Completed</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 10px;">
            <div style="font-size: clamp(1.5rem, 3vw, 2rem);">🧩</div>
            <h4>{data['total_mazes']}</h4>
            <p>Mazes Solved</p>
        </div>
        """, unsafe_allow_html=True)

def show_quests():
    """Quests page"""
    st.markdown("## 🎯 Quest Board")
    
    data = st.session_state.app_data
    generate_daily_quests()
    
    tab1, tab2, tab3 = st.tabs(["📅 Daily", "📋 Active", "✅ Done"])
    
    with tab1:
        st.markdown("### Today's Daily Quests")
        
        for quest in data['daily_quests']:
            if not quest['completed']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    aura = next((a for a in AURAS if a['id'] == quest['aura']), None)
                    st.markdown(f"**{aura['icon'] if aura else '📌'} {quest['title']}**")
                with col2:
                    st.markdown(f"<span style='color: #f5a623;'>+{quest['xp']} XP</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("✅", key=f"daily_{quest['id']}", use_container_width=True):
                        quest['completed'] = True
                        data['total_quests'] += 1
                        add_xp(quest['xp'], quest['aura'])
                        spawn_particles('✅', 8)
                        st.success(f"✅ Quest completed! +{quest['xp']} XP")
                        st.rerun()
            else:
                st.markdown(f"~~{quest['title']}~~ ✅")
    
    with tab2:
        st.markdown("### Active Quests")
        
        with st.expander("➕ Create New Quest", expanded=False):
            quest_title = st.text_input("Quest Title", placeholder="e.g., Read for 30 minutes")
            quest_aura = st.selectbox("Related Aura", [a['id'] for a in AURAS], 
                                     format_func=lambda x: next((a['icon'] + ' ' + a['name'] for a in AURAS if a['id'] == x), x))
            quest_xp = st.slider("XP Reward", 10, 100, 25)
            
            if st.button("✨ Create Quest", use_container_width=True) and quest_title:
                data['quests'].append({
                    'id': f"quest_{int(time.time())}",
                    'title': quest_title,
                    'xp': quest_xp,
                    'aura': quest_aura,
                    'completed': False,
                    'created': datetime.date.today().isoformat()
                })
                st.success("Quest created!")
                st.rerun()
        
        active_quests = [q for q in data['quests'] if not q['completed']]
        if active_quests:
            for quest in active_quests:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    aura = next((a for a in AURAS if a['id'] == quest['aura']), None)
                    st.markdown(f"**{aura['icon'] if aura else '📌'} {quest['title']}**")
                with col2:
                    st.markdown(f"<span style='color: #f5a623;'>+{quest['xp']}</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("✅", key=f"complete_{quest['id']}"):
                        quest['completed'] = True
                        data['total_quests'] += 1
                        add_xp(quest['xp'], quest['aura'])
                        spawn_particles('✅', 5)
                        st.success(f"✅ Completed! +{quest['xp']} XP")
                        st.rerun()
                with col4:
                    if st.button("🗑️", key=f"delete_{quest['id']}"):
                        data['quests'].remove(quest)
                        st.rerun()
        else:
            st.info("No active quests. Create one above!")
    
    with tab3:
        completed = [q for q in data['quests'] if q['completed']] + [q for q in data['daily_quests'] if q['completed']]
        if completed:
            for quest in completed[-20:]:
                st.markdown(f"✅ {quest['title']} - *+{quest['xp']} XP*")
        else:
            st.info("No completed quests yet.")

def show_journal():
    """Journal page"""
    st.markdown("## 📖 Reflective Journal")
    
    data = st.session_state.app_data
    
    with st.expander("✍️ Write New Entry", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            mood = st.selectbox("Mood", ["😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "💪 Motivated", "🧘 Peaceful"])
        with col2:
            tags = st.multiselect("Tags", ["Gratitude", "Learning", "Challenge", "Success", "Reflection", "Goal"])
        
        entry_title = st.text_input("Title (optional)", placeholder="Today's reflection...")
        entry_text = st.text_area("Your thoughts", height=150, placeholder="What did you learn today?")
        
        if st.button("💾 Save Entry", use_container_width=True):
            if entry_text:
                data['journal'].append({
                    'id': f"journal_{int(time.time())}",
                    'date': datetime.date.today().isoformat(),
                    'time': datetime.datetime.now().strftime("%H:%M"),
                    'title': entry_title or 'Untitled',
                    'content': entry_text,
                    'mood': mood,
                    'tags': tags
                })
                add_xp(15, 'mindfulness')
                spawn_particles('📝', 8)
                st.success("📝 Journal entry saved! +15 XP")
                st.rerun()
    
    st.markdown("### 📚 Your Entries")
    
    if data['journal']:
        search = st.text_input("🔍 Search", placeholder="Search entries...")
        entries = data['journal'][::-1]
        if search:
            entries = [e for e in entries if search.lower() in e.get('content', '').lower()]
        
        for entry in entries[:20]:
            with st.container():
                border_color = '#4ade80' if 'Great' in entry.get('mood','') else '#a855f7' if 'Motivated' in entry.get('mood','') else '#f5a623'
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <strong>{entry.get('title', 'Untitled')}</strong>
                        <small style="color: #888;">📅 {entry['date']} · {entry.get('mood', '')}</small>
                    </div>
                    <p style="font-size: 0.9rem;">{entry['content'][:200]}{'...' if len(entry['content']) > 200 else ''}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📖 No journal entries yet.")

def show_achievements():
    """Achievements page"""
    st.markdown("## 🏆 Achievements")
    
    data = st.session_state.app_data
    check_achievements()
    
    unlocked = sum(1 for a in data['achievements'] if a['unlocked'])
    total = len(data['achievements'])
    
    st.markdown(f"### Progress: {unlocked}/{total}")
    
    progress_pct = (unlocked / total * 100) if total > 0 else 0
    st.markdown(f"""
    <div class="progress-bar" style="margin: 20px 0;">
        <div class="progress-fill" style="width: {progress_pct}%; background: linear-gradient(90deg, #f5a623, #ffd700);"></div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, ach in enumerate(data['achievements']):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="achievement-card {'unlocked' if ach['unlocked'] else ''}" style="opacity: {'1' if ach['unlocked'] else '0.5'};">
                <div style="font-size: clamp(2rem, 4vw, 3rem);">{ach['icon']}</div>
                <h4 style="font-size: clamp(0.8rem, 1.5vw, 1rem);">{ach['name']}</h4>
                <small style="color: #888;">{ach['desc']}</small>
                <div style="margin-top: 10px;">{'✅ Unlocked!' if ach['unlocked'] else '🔒 Locked'}</div>
            </div>
            """, unsafe_allow_html=True)

def show_maze():
    """Maze game page with drag navigation"""
    st.markdown("## 🧩 The Aura Maze")
    st.markdown("*Drag your finger/mouse across the maze to navigate!*")
    
    data = st.session_state.app_data
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"🏆 **Mazes completed: {data['total_mazes']}**")
    with col2:
        maze_size = st.selectbox("Size", [7, 9, 11], index=1, key="maze_size_select")
        if maze_size != st.session_state.maze_size:
            st.session_state.maze_size = maze_size
            st.session_state.maze = generate_maze(maze_size)
            st.session_state.player_pos = [1, 1]
            st.rerun()
    with col3:
        if st.button("🔄 New Maze", use_container_width=True):
            st.session_state.maze = generate_maze(st.session_state.maze_size)
            st.session_state.player_pos = [1, 1]
            st.rerun()
    
    # Hidden input for JavaScript direction
    direction = st.text_input("", key="maze-direction-input", label_visibility="collapsed")
    if direction:
        move_player(direction)
        st.rerun()
    
    # Arrow buttons
    st.markdown("### 🕹️ Controls (or drag on maze)")
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
    with c1:
        st.write("")
    with c2:
        if st.button("⬆️", use_container_width=True, key="btn_up"):
            move_player('up')
            st.rerun()
    with c3:
        st.write("")
    with c4:
        if st.button("🔄", use_container_width=True, key="btn_reset"):
            st.session_state.maze = generate_maze(st.session_state.maze_size)
            st.session_state.player_pos = [1, 1]
            st.rerun()
    with c5:
        st.write("")
    
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])
    with c1:
        st.write("")
    with c2:
        if st.button("⬅️", use_container_width=True, key="btn_left"):
            move_player('left')
            st.rerun()
    with c3:
        if st.button("⬇️", use_container_width=True, key="btn_down"):
            move_player('down')
            st.rerun()
    with c4:
        if st.button("➡️", use_container_width=True, key="btn_right"):
            move_player('right')
            st.rerun()
    with c5:
        st.write("")
    
    # Render maze
    st.markdown("### 🗺️ Drag to Navigate")
    st.markdown(render_maze_html(st.session_state.maze, st.session_state.player_pos), unsafe_allow_html=True)

def show_chat():
    """Chat page"""
    st.markdown("## 💬 AuraRise Community")
    
    data = st.session_state.app_data
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🟢 Online")
        
        for user in data['online_users']:
            is_selected = data['current_chat_user'] == user['name']
            st.markdown(f"""
            <div style="background: rgba(255,255,255,{'0.1' if is_selected else '0.05'}); 
                        padding: 12px; border-radius: 12px; margin: 5px 0;
                        border: {'2px solid #00c6ff' if is_selected else '1px solid rgba(255,255,255,0.1)'};">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="online-dot"></span>
                    <span style="font-size: 1.3rem;">{user['avatar']}</span>
                    <div>
                        <strong>{user['name']}</strong>
                        <br><small style="color: #888;">{user['bio']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"💬 {user['name']}", key=f"select_{user['name']}", use_container_width=True):
                data['current_chat_user'] = user['name']
                st.rerun()
    
    with col2:
        if data['current_chat_user']:
            current_user = next((u for u in data['online_users'] if u['name'] == data['current_chat_user']), None)
            st.markdown(f"### 💬 {current_user['avatar']} {data['current_chat_user']}")
            
            chat_container = st.container(height=350)
            with chat_container:
                chat_messages = [m for m in data['chat_messages'] 
                               if (m['from'] == 'You' and m['to'] == data['current_chat_user']) or 
                                  (m['to'] == 'You' and m['from'] == data['current_chat_user'])]
                
                for msg in chat_messages[-50:]:
                    is_sent = msg['from'] == 'You'
                    st.markdown(f"""
                    <div style="display: flex; justify-content: {'flex-end' if is_sent else 'flex-start'}; margin: 6px 0;">
                        <div class="chat-message {'sent' if is_sent else 'received'}">
                            <small style="color: {'#000' if is_sent else '#888'};">
                                {msg['from']} · {msg['time']}
                            </small>
                            <p style="margin: 3px 0 0 0;">{msg['text']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with st.form(f"chat_form_{data['current_chat_user']}", clear_on_submit=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    message = st.text_input("Message...", key=f"msg_{data['current_chat_user']}", label_visibility="collapsed")
                with col2:
                    send = st.form_submit_button("📤", use_container_width=True)
                
                if send and message:
                    data['chat_messages'].append({
                        'from': 'You', 'to': data['current_chat_user'],
                        'text': message, 'time': datetime.datetime.now().strftime("%H:%M")
                    })
                    
                    responses = [
                        "That's awesome! 🎉", "I totally agree! 💯",
                        "Great progress! 🌟", "You're amazing! 💪",
                        "Let's level up! 🚀", "Thanks for sharing! 📝",
                        "So inspiring! ✨", "What's your focus today? 🎯",
                    ]
                    
                    time.sleep(0.8)
                    data['chat_messages'].append({
                        'from': data['current_chat_user'], 'to': 'You',
                        'text': random.choice(responses), 'time': datetime.datetime.now().strftime("%H:%M")
                    })
                    st.rerun()
        else:
            st.info("👈 Select a member to start chatting!")

def show_shop():
    """Shop page"""
    st.markdown("## 🛒 Aura Shop")
    
    data = st.session_state.app_data
    st.markdown(f"### 🪙 **{data['user']['aura_coins']}** coins")
    
    items = [
        {'name': 'Wizard', 'icon': '🧙', 'cost': 150, 'desc': 'Mystical wisdom'},
        {'name': 'Superhero', 'icon': '🦸', 'cost': 200, 'desc': 'Heroic courage'},
        {'name': 'Star', 'icon': '🌟', 'cost': 180, 'desc': 'Shining bright'},
        {'name': 'Phoenix', 'icon': '🐦‍🔥', 'cost': 250, 'desc': 'Rise from ashes'},
        {'name': 'Dragon', 'icon': '🐉', 'cost': 300, 'desc': 'Powerful focus'},
        {'name': 'Ninja', 'icon': '🥷', 'cost': 220, 'desc': 'Silent discipline'},
        {'name': 'Astronaut', 'icon': '🧑‍🚀', 'cost': 280, 'desc': 'Explore frontiers'},
        {'name': 'Artist', 'icon': '👨‍🎨', 'cost': 160, 'desc': 'Creative genius'},
    ]
    
    cols = st.columns(4)
    for i, item in enumerate(items):
        with cols[i % 4]:
            owned = item['icon'] in data['user']['unlocked_avatars']
            is_current = data['user']['avatar'] == item['icon']
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; text-align: center;
                        border: {'2px solid #f5a623' if is_current else '1px solid rgba(255,255,255,0.1)'};">
                <div style="font-size: 2.5rem;">{item['icon']}</div>
                <h4 style="font-size: 0.9rem;">{item['name']}</h4>
                <small style="color: #888;">{item['desc']}</small>
                <p>{'✅ Current' if is_current else '✅ Owned' if owned else f'🪙 {item["cost"]}'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not owned:
                if st.button(f"Buy", key=f"buy_{item['name']}", use_container_width=True):
                    if data['user']['aura_coins'] >= item['cost']:
                        data['user']['aura_coins'] -= item['cost']
                        data['user']['unlocked_avatars'].append(item['icon'])
                        data['user']['avatar'] = item['icon']
                        spawn_particles(item['icon'], 8)
                        st.success(f"🎉 Purchased {item['name']}!")
                        st.rerun()
                    else:
                        st.error("Not enough coins!")
            elif not is_current:
                if st.button(f"Equip", key=f"equip_{item['name']}", use_container_width=True):
                    data['user']['avatar'] = item['icon']
                    st.success(f"✅ Equipped {item['name']}!")
                    st.rerun()

def show_wallpaper_selector():
    """Wallpaper selection"""
    st.markdown("## 🎨 Choose Wallpaper")
    
    data = st.session_state.app_data
    current_wp = data['user'].get('wallpaper', 'default')
    
    categories = {
        '🎯 Focus & Discipline': ['focus', 'discipline'],
        '🎨 Creativity': ['creativity', 'adventure'],
        '⚡ Energy': ['vitality', 'courage'],
        '🧘 Mindfulness': ['mindfulness', 'balance'],
        '🤝 Connection': ['empathy', 'resilience'],
        '👑 Growth': ['leadership', 'default'],
    }
    
    for category, wp_list in categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(len(wp_list))
        for i, wp_name in enumerate(wp_list):
            with cols[i]:
                is_selected = current_wp == wp_name
                st.markdown(f"""
                <div style="background: {WALLPAPERS[wp_name]}; height: 100px; border-radius: 15px;
                          display: flex; align-items: center; justify-content: center;
                          border: {'3px solid #00c6ff' if is_selected else '1px solid rgba(255,255,255,0.2)'};
                          cursor: pointer;">
                    <span style="background: rgba(0,0,0,0.6); padding: 8px 12px; border-radius: 8px; color: white; font-size: 0.8rem;">
                        {wp_name.capitalize()}{' ✅' if is_selected else ''}
                    </span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select", key=f"wp_{wp_name}", use_container_width=True):
                    data['user']['wallpaper'] = wp_name
                    st.success(f"🎨 {wp_name} wallpaper set!")
                    st.rerun()

def render_bottom_nav():
    """Render bottom navigation bar"""
    data = st.session_state.app_data
    current = data.get('current_page', 'home')
    
    nav_items = [
        ('home', '⚡', 'Home'),
        ('quests', '🎯', 'Quests'),
        ('journal', '📖', 'Journal'),
        ('achievements', '🏆', 'Achieve'),
        ('maze', '🧩', 'Maze'),
        ('chat', '💬', 'Chat'),
        ('shop', '🛒', 'Shop'),
    ]
    
    # Use columns for bottom nav simulation with buttons
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    cols = st.columns(len(nav_items))
    
    for i, (page, icon, label) in enumerate(nav_items):
        with cols[i]:
            is_active = current == page
            if st.button(f"{icon}\n{label}", key=f"nav_{page}", use_container_width=True,
                        help=label,
                        type="primary" if is_active else "secondary"):
                data['current_page'] = page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application"""
    set_background()
    add_watermark()
    add_wallpaper_button()
    
    if st.session_state.app_data['selected_auras']:
        generate_daily_quests()
        check_achievements()
    
    # Determine current page
    current_page = st.session_state.app_data.get('current_page', 'home')
    
    # Render current page
    if current_page == 'home':
        show_home()
    elif current_page == 'quests':
        show_quests()
    elif current_page == 'journal':
        show_journal()
    elif current_page == 'achievements':
        show_achievements()
    elif current_page == 'maze':
        show_maze()
    elif current_page == 'chat':
        show_chat()
    elif current_page == 'shop':
        show_shop()
    elif current_page == 'wallpaper':
        show_wallpaper_selector()
    
    # Add padding for bottom nav
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    
    # Render bottom navigation
    render_bottom_nav()

if __name__ == "__main__":
    main()
