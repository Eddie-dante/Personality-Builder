# app.py - AuraRise Complete Application
import streamlit as st
import random
import datetime
import time
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import hashlib
import requests
from urllib.request import urlopen

# Page configuration
st.set_page_config(
    page_title="AuraRise - Level Up Your Life",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for amazing vibes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        transition: all 0.3s ease;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    .title-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
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
    
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 25px;
        color: rgba(255,255,255,0.25);
        font-size: 13px;
        font-style: italic;
        z-index: 1000;
        pointer-events: none;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(168,85,247,0.3);
    }
    
    .aura-card {
        background: rgba(20,20,40,0.8);
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(10px);
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
    
    .chat-message {
        padding: 12px 18px;
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
    
    .maze-container {
        display: inline-block;
        border: 3px solid rgba(168,85,247,0.5);
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 0 40px rgba(168,85,247,0.2);
    }
    
    .maze-cell {
        width: 45px;
        height: 45px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 22px;
        transition: all 0.2s;
        border-radius: 3px;
        margin: 1px;
    }
    
    .maze-wall {
        background: linear-gradient(135deg, #2a2a3e, #1a1a2e);
    }
    
    .maze-path {
        background: rgba(0,0,0,0.3);
    }
    
    .maze-player {
        background: linear-gradient(135deg, #00c6ff, #0099cc);
        box-shadow: 0 0 25px rgba(0,198,255,0.6);
        animation: playerPulse 1s ease-in-out infinite;
        border-radius: 8px;
    }
    
    .maze-goal {
        background: linear-gradient(135deg, #f5a623, #ffd700);
        animation: goalGlow 1.5s ease-in-out infinite;
        border-radius: 8px;
    }
    
    @keyframes playerPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    @keyframes goalGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(245,166,35,0.5); }
        50% { box-shadow: 0 0 50px rgba(245,166,35,0.9); }
    }
    
    .progress-bar {
        height: 12px;
        border-radius: 6px;
        background: rgba(255,255,255,0.08);
        overflow: hidden;
        margin: 5px 0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(90deg, var(--color), #fff);
    }
    
    .stat-card {
        background: rgba(20,20,40,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
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
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }
    
    .achievement-card.unlocked {
        border-color: rgba(245,166,35,0.5);
        box-shadow: 0 0 30px rgba(245,166,35,0.2);
    }
    
    .quest-card {
        background: rgba(20,20,40,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
    }
    
    .quest-card:hover {
        border-color: rgba(0,198,255,0.3);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    
    .glow-button {
        background: linear-gradient(135deg, #00c6ff, #a855f7);
        border: none;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 30px;
        color: #fff;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(0,198,255,0.4);
        transition: all 0.3s;
    }
    
    .glow-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,198,255,0.6);
    }
    
    .neon-text {
        text-shadow: 0 0 10px rgba(0,198,255,0.5), 0 0 20px rgba(0,198,255,0.3);
    }
    
    .user-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .online-dot {
        width: 10px;
        height: 10px;
        background: #4ade80;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: onlinePulse 2s infinite;
    }
    
    @keyframes onlinePulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.5); }
        50% { box-shadow: 0 0 0 8px rgba(74,222,128,0); }
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
        'current_chat_user': 'Edwin'
    }

# Aura definitions with rich descriptions
AURAS = [
    {'id': 'focus', 'name': 'Focus', 'icon': '🎯', 'color': '#ff6b6b', 'desc': 'Laser-sharp concentration for deep work'},
    {'id': 'creativity', 'name': 'Creativity', 'icon': '🎨', 'color': '#f06595', 'desc': 'Unleash imagination and innovation'},
    {'id': 'discipline', 'name': 'Discipline', 'icon': '🧘', 'color': '#748ffc', 'desc': 'Consistent self-control and habits'},
    {'id': 'vitality', 'name': 'Vitality', 'icon': '⚡', 'color': '#ffd43b', 'desc': 'Radiant physical energy and health'},
    {'id': 'empathy', 'name': 'Empathy', 'icon': '🤝', 'color': '#ff8787', 'desc': 'Deep emotional connection'},
    {'id': 'resilience', 'name': 'Resilience', 'icon': '🛡️', 'color': '#20c997', 'desc': 'Bounce back stronger'},
    {'id': 'courage', 'name': 'Courage', 'icon': '🦁', 'color': '#ff922b', 'desc': 'Face fears boldly'},
    {'id': 'mindfulness', 'name': 'Mindfulness', 'icon': '🧘‍♀️', 'color': '#63e6be', 'desc': 'Live in the present moment'},
]

# Wallpaper collection based on aura moods
WALLPAPERS = {
    'default': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80',
    'focus': 'https://images.unsplash.com/photo-1518655048521-f130df041f66?w=1920&q=80',
    'creativity': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920&q=80',
    'vitality': 'https://images.unsplash.com/photo-1534258936925-c58bed479fcb?w=1920&q=80',
    'courage': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1920&q=80',
    'mindfulness': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80',
    'discipline': 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1920&q=80',
    'balance': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80',
    'adventure': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80',
    'empathy': 'https://images.unsplash.com/photo-1474552226712-ac0f0961a954?w=1920&q=80',
    'resilience': 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1920&q=80',
    'leadership': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1920&q=80',
}

# Helper functions
def get_wallpaper():
    """Get current wallpaper based on user selection"""
    wp = st.session_state.app_data['user'].get('wallpaper', 'default')
    return WALLPAPERS.get(wp, WALLPAPERS['default'])

def set_background():
    """Apply dynamic background with wallpaper filter"""
    wallpaper = get_wallpaper()
    aura_colors = []
    for aura_id in st.session_state.app_data['selected_auras'][:3]:
        aura = next((a for a in AURAS if a['id'] == aura_id), None)
        if aura:
            aura_colors.append(aura['color'])
    
    if not aura_colors:
        aura_colors = ['rgba(0,198,255,0.3)', 'rgba(168,85,247,0.3)']
    
    color_overlay = ', '.join(aura_colors)
    
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, {color_overlay}), url('{wallpaper}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: -1;
        }}
    </style>
    """, unsafe_allow_html=True)

def add_watermark():
    """Add 'by WeGEM (Edwin)' watermark to all pages"""
    st.markdown(
        '<div class="watermark">by WeGEM (Edwin) 🦾</div>',
        unsafe_allow_html=True
    )

def calc_aura_score():
    """Calculate total aura score"""
    return sum(st.session_state.app_data['aura_stats'].values())

def add_xp(amount, aura_id=None):
    """Add XP and handle level ups"""
    data = st.session_state.app_data
    data['user']['xp'] += amount
    
    if aura_id and aura_id in data['aura_stats']:
        data['aura_stats'][aura_id] += amount // 8
    
    # Check level up
    leveled_up = False
    while data['user']['xp'] >= data['user']['xp_to_next']:
        data['user']['xp'] -= data['user']['xp_to_next']
        data['user']['level'] += 1
        data['user']['xp_to_next'] = int(data['user']['xp_to_next'] * 1.45)
        data['user']['aura_coins'] += data['user']['level'] * 18
        leveled_up = True
    
    if leveled_up:
        st.balloons()
        st.success(f"🎉 Level Up! You're now Level {data['user']['level']}!")
    
    # Update streak
    today = datetime.date.today().isoformat()
    if data['user']['last_active'] != today:
        if data['user']['last_active']:
            last = datetime.date.fromisoformat(data['user']['last_active'])
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            if last == yesterday:
                data['user']['streak'] += 1
                if data['user']['streak'] % 7 == 0:
                    data['user']['aura_coins'] += 50
                    st.success(f"🔥 {data['user']['streak']}-day streak! Bonus +50 coins!")
            else:
                data['user']['streak'] = 1
        else:
            data['user']['streak'] = 1
        data['user']['last_active'] = today
    
    # Add to history
    data['aura_history'].append({
        'date': today,
        'score': calc_aura_score()
    })
    
    # Check achievements
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
            st.toast(f"🏆 Achievement Unlocked: {ach['name']}!")

def generate_daily_quests():
    """Generate daily quests if needed"""
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

# Maze generation with improved algorithm
def generate_maze(size=11):
    """Generate a solvable maze using recursive backtracking"""
    if size % 2 == 0:
        size += 1
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Create path
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
    
    # Place goal
    grid[size-2][size-2] = 2
    
    # Ensure path to goal
    if grid[size-3][size-2] == 1 and grid[size-2][size-3] == 1:
        grid[size-3][size-2] = 0
    if grid[size-2][size-3] == 1:
        grid[size-2][size-3] = 0
    
    return grid

# Initialize maze
if 'maze' not in st.session_state:
    st.session_state.maze = generate_maze(11)
    st.session_state.player_pos = [1, 1]
    st.session_state.maze_size = 11

def render_maze_html(grid, player_pos):
    """Render maze as HTML with styling"""
    html = '<div class="maze-container">'
    for r in range(len(grid)):
        html += '<div style="display: flex; justify-content: center;">'
        for c in range(len(grid[0])):
            cell_class = 'maze-wall'
            content = ''
            
            if grid[r][c] == 0:
                cell_class = 'maze-path'
                content = ''
            elif grid[r][c] == 2:
                cell_class = 'maze-goal'
                content = '🏁'
            
            if r == player_pos[0] and c == player_pos[1]:
                cell_class = 'maze-player'
                content = '🦾'
            
            html += f'<div class="maze-cell {cell_class}">{content}</div>'
        html += '</div>'
    html += '</div>'
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
    
    # Check win condition
    if maze[st.session_state.player_pos[0]][st.session_state.player_pos[1]] == 2:
        st.session_state.app_data['total_mazes'] += 1
        coins_earned = random.randint(20, 50)
        st.session_state.app_data['user']['aura_coins'] += coins_earned
        aura = st.session_state.app_data['selected_auras'][0] if st.session_state.app_data['selected_auras'] else None
        add_xp(40, aura)
        check_achievements()
        st.success(f"🧩 Maze completed! +40 XP +{coins_earned} coins!")
        st.balloons()
        st.session_state.maze = generate_maze(st.session_state.maze_size)
        st.session_state.player_pos = [1, 1]
        st.rerun()

def show_home():
    """Home page with dashboard"""
    st.markdown('<h1 class="title-text">AuraRise</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color: #888; font-size: 1.1rem;">Shape your energy. Master discipline, confidence, and more. 🦾</p>', unsafe_allow_html=True)
    
    data = st.session_state.app_data
    
    # Aura selection if none selected
    if not data['selected_auras']:
        st.markdown("### 🌟 Select Your Auras to Begin")
        st.markdown("*Choose the energies you want to cultivate*")
        
        cols = st.columns(4)
        for i, aura in enumerate(AURAS):
            with cols[i % 4]:
                selected = aura['id'] in data['selected_auras']
                st.markdown(f"""
                <div class="aura-card {'selected' if selected else ''}">
                    <div style="font-size: 3rem;">{aura['icon']}</div>
                    <h4>{aura['name']}</h4>
                    <small style="color: #888;">{aura['desc']}</small>
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
            st.success(f"✨ {len(data['selected_auras'])} auras selected! Your journey begins now!")
            if st.button("🚀 Start Your Journey", use_container_width=True, type="primary"):
                st.rerun()
        return
    
    # Dashboard view
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Aura Score
        score = calc_aura_score()
        tier = '🌟 Legend' if score >= 250 else '✨ Master' if score >= 100 else '🔮 Adept' if score >= 50 else '🌱 Novice'
        
        st.markdown(f"""
        <div style="text-align: center; padding: 30px;">
            <div style="font-size: 5rem; font-weight: 900; background: linear-gradient(135deg, #00c6ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;" class="neon-text">
                {score}
            </div>
            <div style="font-size: 1.2rem; margin-top: -10px;">⚡ Aura Score</div>
            <div class="user-badge" style="background: rgba(255,255,255,0.1); margin-top: 10px;">{tier}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # XP Progress
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
        
        # Aura stats
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
        # Stats cards
        st.markdown("### 📈 Stats")
        
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">{data['user']['avatar']}</div>
            <h4>Level {data['user']['level']}</h4>
            <p>🪙 {data['user']['aura_coins']} coins</p>
            <p>🔥 {data['user']['streak']} day streak</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 10px;">
            <div style="font-size: 2rem;">🎯</div>
            <h4>{data['total_quests']}</h4>
            <p>Quests Completed</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card" style="margin-top: 10px;">
            <div style="font-size: 2rem;">🧩</div>
            <h4>{data['total_mazes']}</h4>
            <p>Mazes Solved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🎯 View Quests", use_container_width=True):
            st.session_state.nav = "Quests"
            st.rerun()
    with c2:
        if st.button("🧩 Play Maze", use_container_width=True):
            st.session_state.nav = "Maze"
            st.rerun()
    with c3:
        if st.button("💬 Open Chat", use_container_width=True):
            st.session_state.nav = "Chat"
            st.rerun()
    with c4:
        if st.button("🎨 Wallpapers", use_container_width=True):
            st.session_state.nav = "Wallpaper"
            st.rerun()

def show_quests():
    """Quests page"""
    st.markdown("## 🎯 Quest Board")
    
    data = st.session_state.app_data
    generate_daily_quests()
    
    # Tabs for different quest types
    tab1, tab2, tab3 = st.tabs(["📅 Daily Quests", "📋 Active Quests", "✅ Completed"])
    
    with tab1:
        st.markdown("### Today's Daily Quests")
        st.markdown("*Complete these before the day ends!*")
        
        for quest in data['daily_quests']:
            if not quest['completed']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    aura = next((a for a in AURAS if a['id'] == quest['aura']), None)
                    st.markdown(f"**{aura['icon'] if aura else '📌'} {quest['title']}**")
                with col2:
                    st.markdown(f"<span style='color: #f5a623;'>+{quest['xp']} XP</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("✅ Complete", key=f"daily_{quest['id']}", use_container_width=True):
                        quest['completed'] = True
                        data['total_quests'] += 1
                        add_xp(quest['xp'], quest['aura'])
                        st.success(f"✅ Quest completed! +{quest['xp']} XP")
                        st.rerun()
            else:
                st.markdown(f"~~{quest['title']}~~ ✅")
    
    with tab2:
        st.markdown("### Active Quests")
        
        # Add quest form
        with st.expander("➕ Create New Quest", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                quest_title = st.text_input("Quest Title", placeholder="e.g., Read for 30 minutes")
            with col2:
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
                st.success("Quest created successfully!")
                st.rerun()
        
        # Active quests list
        active_quests = [q for q in data['quests'] if not q['completed']]
        if active_quests:
            for quest in active_quests:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    aura = next((a for a in AURAS if a['id'] == quest['aura']), None)
                    st.markdown(f"**{aura['icon'] if aura else '📌'} {quest['title']}**")
                with col2:
                    st.markdown(f"<span style='color: #f5a623;'>+{quest['xp']} XP</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("✅", key=f"complete_{quest['id']}", help="Complete quest"):
                        quest['completed'] = True
                        data['total_quests'] += 1
                        add_xp(quest['xp'], quest['aura'])
                        st.success(f"✅ Quest completed! +{quest['xp']} XP")
                        st.rerun()
                with col4:
                    if st.button("🗑️", key=f"delete_{quest['id']}", help="Delete quest"):
                        data['quests'].remove(quest)
                        st.rerun()
        else:
            st.info("No active quests. Create one above!")
    
    with tab3:
        st.markdown("### Completed Quests")
        completed_quests = [q for q in data['quests'] if q['completed']] + [q for q in data['daily_quests'] if q['completed']]
        if completed_quests:
            for quest in completed_quests[-20:]:
                st.markdown(f"✅ {quest['title']} - *+{quest['xp']} XP*")
            st.markdown(f"*Total quests completed: {data['total_quests']}*")
        else:
            st.info("No completed quests yet. Complete some quests!")

def show_journal():
    """Journal page"""
    st.markdown("## 📖 Reflective Journal")
    st.markdown("*Document your journey and track your growth*")
    
    data = st.session_state.app_data
    
    # Journal entry form
    with st.expander("✍️ Write New Entry", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            mood = st.selectbox("Current Mood", ["😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "💪 Motivated", "🧘 Peaceful"])
        with col2:
            tags = st.multiselect("Tags", ["Gratitude", "Learning", "Challenge", "Success", "Reflection", "Goal"])
        
        entry_title = st.text_input("Title (optional)", placeholder="Today's reflection...")
        entry_text = st.text_area("Your thoughts", height=150, placeholder="What did you learn today? What are you grateful for? What challenges did you face?")
        
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
                st.success("📝 Journal entry saved! +15 XP")
                st.rerun()
    
    # Journal entries display
    st.markdown("### 📚 Your Entries")
    
    if data['journal']:
        # Search and filter
        search = st.text_input("🔍 Search entries", placeholder="Search by keyword...")
        
        entries = data['journal'][::-1]  # Most recent first
        if search:
            entries = [e for e in entries if search.lower() in e.get('content', '').lower() or search.lower() in e.get('title', '').lower()]
        
        for entry in entries[:20]:
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 4px solid {'#4ade80' if 'Great' in entry.get('mood','') else '#a855f7' if 'Motivated' in entry.get('mood','') else '#f5a623'};">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <strong>{entry.get('title', 'Untitled')}</strong>
                        <small style="color: #888;">📅 {entry['date']} · {entry.get('time', '')} · {entry.get('mood', '')}</small>
                    </div>
                    <p>{entry['content'][:200]}{'...' if len(entry['content']) > 200 else ''}</p>
                    <div style="margin-top: 10px;">
                        {''.join([f'<span style="background: rgba(255,255,255,0.1); padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin-right: 5px;">{tag}</span>' for tag in entry.get('tags', [])])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📖 No journal entries yet. Start writing to track your journey!")

def show_achievements():
    """Achievements page"""
    st.markdown("## 🏆 Achievements")
    
    data = st.session_state.app_data
    check_achievements()
    
    unlocked_count = sum(1 for a in data['achievements'] if a['unlocked'])
    total_count = len(data['achievements'])
    
    st.markdown(f"### Progress: {unlocked_count}/{total_count} Unlocked")
    
    # Progress bar for achievements
    progress_pct = (unlocked_count / total_count * 100) if total_count > 0 else 0
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
                <div style="font-size: 3rem;">{ach['icon']}</div>
                <h4>{ach['name']}</h4>
                <small style="color: #888;">{ach['desc']}</small>
                <div style="margin-top: 10px;">
                    {'✅ Unlocked!' if ach['unlocked'] else '🔒 Locked'}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_maze():
    """Maze game page"""
    st.markdown("## 🧩 The Aura Maze")
    st.markdown("*Navigate through the maze to reach the goal! Use buttons or keyboard arrows.*")
    
    data = st.session_state.app_data
    
    # Maze controls and info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Mazes completed: {data['total_mazes']}** | Use arrow keys or buttons to move")
    with col2:
        maze_size = st.selectbox("Size", [7, 9, 11, 13], index=1)
        if maze_size != st.session_state.maze_size:
            st.session_state.maze_size = maze_size
            st.session_state.maze = generate_maze(maze_size)
            st.session_state.player_pos = [1, 1]
            st.rerun()
    
    # Direction controls
    st.markdown("### 🕹️ Controls")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        st.write("")
    with col2:
        if st.button("⬆️ Up", use_container_width=True, key="maze_up"):
            move_player('up')
            st.rerun()
    with col3:
        st.write("")
    with col4:
        if st.button("🔄 Reset", use_container_width=True, key="maze_reset"):
            st.session_state.maze = generate_maze(st.session_state.maze_size)
            st.session_state.player_pos = [1, 1]
            st.rerun()
    with col5:
        st.write("")
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        st.write("")
    with col2:
        if st.button("⬅️ Left", use_container_width=True, key="maze_left"):
            move_player('left')
            st.rerun()
    with col3:
        if st.button("⬇️ Down", use_container_width=True, key="maze_down"):
            move_player('down')
            st.rerun()
    with col4:
        if st.button("➡️ Right", use_container_width=True, key="maze_right"):
            move_player('right')
            st.rerun()
    with col5:
        st.write("")
    
    # Render maze
    st.markdown("### 🗺️ Maze Map")
    st.markdown(render_maze_html(st.session_state.maze, st.session_state.player_pos), unsafe_allow_html=True)
    
    # Keyboard controls info
    st.markdown("""
    <div style="text-align: center; color: #888; margin-top: 20px;">
        <small>💡 Tip: Use arrow keys on your keyboard for faster navigation!</small>
    </div>
    """, unsafe_allow_html=True)

def show_chat():
    """Community chat page"""
    st.markdown("## 💬 AuraRise Community")
    st.markdown("*Connect with fellow aura masters*")
    
    data = st.session_state.app_data
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🟢 Online Members")
        
        for user in data['online_users']:
            is_selected = data['current_chat_user'] == user['name']
            st.markdown(f"""
            <div style="background: rgba(255,255,255,{'0.1' if is_selected else '0.05'}); 
                        padding: 15px; 
                        border-radius: 15px; 
                        margin: 5px 0;
                        cursor: pointer;
                        border: {'2px solid #00c6ff' if is_selected else '1px solid rgba(255,255,255,0.1)'};"
                 onclick="this.querySelector('button').click()">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div>
                        <span class="online-dot"></span>
                        <span style="font-size: 1.5rem;">{user['avatar']}</span>
                    </div>
                    <div>
                        <strong>{user['name']}</strong>
                        <br><small style="color: #888;">{user['bio']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Chat with {user['name']}", key=f"select_{user['name']}", use_container_width=True):
                data['current_chat_user'] = user['name']
                st.rerun()
    
    with col2:
        if data['current_chat_user']:
            current_user = next((u for u in data['online_users'] if u['name'] == data['current_chat_user']), None)
            
            st.markdown(f"### 💬 Chatting with {current_user['avatar']} {data['current_chat_user']}")
            
            # Chat messages
            chat_container = st.container(height=400)
            with chat_container:
                chat_messages = [m for m in data['chat_messages'] 
                               if (m['from'] == 'You' and m['to'] == data['current_chat_user']) or 
                                  (m['to'] == 'You' and m['from'] == data['current_chat_user'])]
                
                for msg in chat_messages[-50:]:
                    is_sent = msg['from'] == 'You'
                    st.markdown(f"""
                    <div style="display: flex; justify-content: {'flex-end' if is_sent else 'flex-start'}; margin: 8px 0;">
                        <div class="chat-message {'sent' if is_sent else 'received'}">
                            <small style="color: {'#000' if is_sent else '#888'};">
                                {msg['from']} · {msg['time']}
                            </small>
                            <p style="margin: 5px 0 0 0;">{msg['text']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Message input
            with st.form(f"chat_form_{data['current_chat_user']}", clear_on_submit=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    message = st.text_input("Type your message...", key=f"msg_{data['current_chat_user']}", label_visibility="collapsed")
                with col2:
                    send = st.form_submit_button("📤 Send", use_container_width=True)
                
                if send and message:
                    # Add user message
                    data['chat_messages'].append({
                        'from': 'You',
                        'to': data['current_chat_user'],
                        'text': message,
                        'time': datetime.datetime.now().strftime("%H:%M")
                    })
                    
                    # Simulate auto-response
                    responses = [
                        "That's awesome! Keep it up! 🎉",
                        "I totally agree with you! 💯",
                        "Great progress on your journey! 🌟",
                        "You're doing amazing work! 💪",
                        "Let's level up together! 🚀",
                        "Thanks for sharing that! 📝",
                        "I'm inspired by your dedication! ✨",
                        "What aura are you focusing on today? 🎯",
                    ]
                    
                    time.sleep(1)
                    data['chat_messages'].append({
                        'from': data['current_chat_user'],
                        'to': 'You',
                        'text': random.choice(responses),
                        'time': datetime.datetime.now().strftime("%H:%M")
                    })
                    st.rerun()
        else:
            st.info("👈 Select a member from the left panel to start chatting!")

def show_shop():
    """Shop page"""
    st.markdown("## 🛒 Aura Shop")
    st.markdown("*Spend your hard-earned coins on cool rewards!*")
    
    data = st.session_state.app_data
    st.markdown(f"### 🪙 Balance: **{data['user']['aura_coins']}** coins")
    
    items = [
        {'name': 'Wizard', 'icon': '🧙', 'cost': 150, 'desc': 'Mystical wisdom'},
        {'name': 'Superhero', 'icon': '🦸', 'cost': 200, 'desc': 'Heroic courage'},
        {'name': 'Star', 'icon': '🌟', 'cost': 180, 'desc': 'Shining bright'},
        {'name': 'Phoenix', 'icon': '🐦‍🔥', 'cost': 250, 'desc': 'Rise from ashes'},
        {'name': 'Dragon', 'icon': '🐉', 'cost': 300, 'desc': 'Powerful focus'},
        {'name': 'Ninja', 'icon': '🥷', 'cost': 220, 'desc': 'Silent discipline'},
        {'name': 'Astronaut', 'icon': '🧑‍🚀', 'cost': 280, 'desc': 'Explore new frontiers'},
        {'name': 'Artist', 'icon': '👨‍🎨', 'cost': 160, 'desc': 'Creative genius'},
    ]
    
    cols = st.columns(4)
    for i, item in enumerate(items):
        with cols[i % 4]:
            owned = item['icon'] in data['user']['unlocked_avatars']
            is_current = data['user']['avatar'] == item['icon']
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); 
                        padding: 20px; 
                        border-radius: 15px; 
                        text-align: center;
                        border: {'2px solid #f5a623' if is_current else '1px solid rgba(255,255,255,0.1)'};">
                <div style="font-size: 3rem;">{item['icon']}</div>
                <h4>{item['name']}</h4>
                <small style="color: #888;">{item['desc']}</small>
                <p style="margin-top: 10px;">
                    {'✅ Current' if is_current else '✅ Owned' if owned else f'🪙 {item["cost"]}'}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if not owned:
                if st.button(f"Buy {item['name']}", key=f"buy_{item['name']}", use_container_width=True):
                    if data['user']['aura_coins'] >= item['cost']:
                        data['user']['aura_coins'] -= item['cost']
                        data['user']['unlocked_avatars'].append(item['icon'])
                        data['user']['avatar'] = item['icon']
                        st.success(f"🎉 Purchased {item['name']} avatar!")
                        st.rerun()
                    else:
                        st.error("Not enough coins! Complete quests to earn more.")
            elif not is_current:
                if st.button(f"Equip {item['name']}", key=f"equip_{item['name']}", use_container_width=True):
                    data['user']['avatar'] = item['icon']
                    st.success(f"✅ Equipped {item['name']} avatar!")
                    st.rerun()

def show_wallpaper_selector():
    """Wallpaper selection page"""
    st.markdown("## 🎨 Choose Your Wallpaper")
    st.markdown("*Select a wallpaper that matches your aura's mood*")
    
    data = st.session_state.app_data
    current_wp = data['user'].get('wallpaper', 'default')
    
    # Group wallpapers by category
    categories = {
        '🎯 Focus & Discipline': ['focus', 'discipline'],
        '🎨 Creativity & Expression': ['creativity', 'adventure'],
        '⚡ Energy & Vitality': ['vitality', 'courage'],
        '🧘 Mindfulness & Balance': ['mindfulness', 'balance'],
        '🤝 Connection & Empathy': ['empathy', 'resilience'],
        '👑 Leadership & Growth': ['leadership', 'default'],
    }
    
    for category, wp_list in categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(4)
        for i, wp_name in enumerate(wp_list):
            with cols[i % 4]:
                wp_url = WALLPAPERS.get(wp_name, WALLPAPERS['default'])
                is_selected = current_wp == wp_name
                
                st.markdown(f"""
                <div style="position: relative; margin: 10px 0;">
                    <img src="{wp_url}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 15px; 
                         border: {'3px solid #00c6ff' if is_selected else '1px solid rgba(255,255,255,0.2)'};">
                    <div style="position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); 
                              padding: 5px 10px; border-radius: 10px; font-size: 0.8rem;">
                        {wp_name.capitalize()}
                    </div>
                    {'✅ Selected' if is_selected else ''}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {wp_name}", key=f"wp_{wp_name}", use_container_width=True):
                    data['user']['wallpaper'] = wp_name
                    st.success(f"🎨 Wallpaper set to {wp_name}!")
                    st.rerun()

# Main app
def main():
    """Main application"""
    # Apply dynamic background
    set_background()
    
    # Add watermark
    add_watermark()
    
    # Check and generate daily quests
    if st.session_state.app_data['selected_auras']:
        generate_daily_quests()
        check_achievements()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem;">🦾</div>
            <h1 style="font-family: 'Orbitron', sans-serif; background: linear-gradient(135deg, #00c6ff, #a855f7); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                AuraRise
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        data = st.session_state.app_data
        
        # User info
        if data['selected_auras']:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 2rem;">{data['user']['avatar']}</div>
                <strong>Level {data['user']['level']}</strong>
                <br><small>🪙 {data['user']['aura_coins']} | 🔥 {data['user']['streak']}d</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        nav_options = {
            "🏠 Home": "Home",
            "🎯 Quests": "Quests", 
            "📖 Journal": "Journal",
            "🏆 Achievements": "Achievements",
            "🧩 Maze": "Maze",
            "💬 Chat": "Chat",
            "🛒 Shop": "Shop",
            "🎨 Wallpaper": "Wallpaper"
        }
        
        selected_nav = st.radio("", list(nav_options.keys()), label_visibility="collapsed")
        current_page = nav_options[selected_nav]
        
        st.divider()
        
        # Online users preview
        st.markdown("### 🟢 Online")
        for user in data['online_users'][:5]:
            st.markdown(f"""
            <div style="padding: 5px 0; display: flex; align-items: center; gap: 8px;">
                <span class="online-dot"></span>
                <span>{user['avatar']} {user['name']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Route to selected page
    if current_page == "Home":
        show_home()
    elif current_page == "Quests":
        show_quests()
    elif current_page == "Journal":
        show_journal()
    elif current_page == "Achievements":
        show_achievements()
    elif current_page == "Maze":
        show_maze()
    elif current_page == "Chat":
        show_chat()
    elif current_page == "Shop":
        show_shop()
    elif current_page == "Wallpaper":
        show_wallpaper_selector()

if __name__ == "__main__":
    main()
