# app.py
import streamlit as st
import random

st.set_page_config(page_title="Guess The Number", page_icon="🎯", layout="centered")

# --------------------------------------------------------------------------
# STYLING
# --------------------------------------------------------------------------
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f6d365, #fda085, #f5576c, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding-top: 10px;
    }

    .subtitle {
        text-align: center;
        color: #c7c7d9;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }

    .card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 25px 30px;
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }

    .stat-row {
        display: flex;
        justify-content: space-around;
        text-align: center;
    }

    .stat-box {
        flex: 1;
    }

    .stat-num {
        font-size: 1.8rem;
        font-weight: 700;
        color: #fda085;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #a9a9c0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .hint-banner {
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 14px;
        border-radius: 14px;
        margin: 10px 0 20px 0;
        animation: fadein 0.4s ease;
    }

    .hint-low { background: rgba(79, 172, 254, 0.18); color: #4facfe; border: 1px solid rgba(79,172,254,0.4);}
    .hint-high { background: rgba(245, 87, 108, 0.18); color: #f5576c; border: 1px solid rgba(245,87,108,0.4);}
    .hint-hot { background: rgba(253, 160, 133, 0.2); color: #fda085; border: 1px solid rgba(253,160,133,0.5);}

    @keyframes fadein {
        from {opacity: 0; transform: translateY(-6px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .chip {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .chip-low { background: rgba(79, 172, 254, 0.2); color: #4facfe; }
    .chip-high { background: rgba(245, 87, 108, 0.2); color: #f5576c; }
    .chip-win { background: rgba(89, 245, 154, 0.25); color: #59f59a; }

    .stButton button {
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(90deg, #f5576c, #fda085);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        transition: transform 0.15s ease;
    }
    .stButton button:hover {
        transform: scale(1.03);
        color: white;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# GAME STATE
# --------------------------------------------------------------------------
DIFFICULTIES = {
    "Easy 🌱  (1–50, 10 tries)": (1, 50, 10),
    "Medium 🔥  (1–100, 8 tries)": (1, 100, 8),
    "Hard 💀  (1–200, 7 tries)": (1, 200, 7),
}


def start_new_game(min_v, max_v, max_attempts):
    st.session_state.number = random.randint(min_v, max_v)
    st.session_state.min_v = min_v
    st.session_state.max_v = max_v
    st.session_state.max_attempts = max_attempts
    st.session_state.count = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.won = False


if "number" not in st.session_state:
    min_v, max_v, max_attempts = DIFFICULTIES["Medium 🔥  (1–100, 8 tries)"]
    start_new_game(min_v, max_v, max_attempts)

# --------------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Game Settings")
    choice = st.radio("Choose difficulty", list(DIFFICULTIES.keys()), index=1)

    if st.button("🔄 Start New Game", use_container_width=True):
        min_v, max_v, max_attempts = DIFFICULTIES[choice]
        start_new_game(min_v, max_v, max_attempts)
        st.rerun()

    st.markdown("---")
    st.caption("Pick a difficulty, then guess the secret number before you run out of tries. Closer guesses turn the hint 🔥 hot!")

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown('<div class="title">🎯 Guess The Number</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">I\'m thinking of a number between '
    f'<b>{st.session_state.min_v}</b> and <b>{st.session_state.max_v}</b>...</div>',
    unsafe_allow_html=True
)

attempts_left = st.session_state.max_attempts - st.session_state.count

# --------------------------------------------------------------------------
# STATS CARD
# --------------------------------------------------------------------------
st.markdown(f"""
<div class="card">
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-num">{st.session_state.count}</div>
            <div class="stat-label">Guesses Made</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{max(attempts_left, 0)}</div>
            <div class="stat-label">Tries Left</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{st.session_state.max_attempts}</div>
            <div class="stat-label">Max Tries</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(min(st.session_state.count / st.session_state.max_attempts, 1.0))

# --------------------------------------------------------------------------
# GAME LOGIC
# --------------------------------------------------------------------------
if not st.session_state.game_over:
    col1, col2 = st.columns([3, 1])

    with col1:
        guess = st.number_input(
            "Your guess",
            min_value=st.session_state.min_v,
            max_value=st.session_state.max_v,
            step=1,
            key=f"guess_{st.session_state.count}",
            label_visibility="collapsed",
        )

    with col2:
        submitted = st.button("Guess! 🚀", use_container_width=True)

    if submitted:
        st.session_state.count += 1
        number = st.session_state.number

        if guess == number:
            st.session_state.won = True
            st.session_state.game_over = True
            st.session_state.history.append((guess, "win"))
        else:
            st.session_state.history.append((guess, "low" if guess < number else "high"))
            if st.session_state.count >= st.session_state.max_attempts:
                st.session_state.game_over = True

        st.rerun()

else:
    # show a final disabled-looking summary instead of input
    st.info("Game finished — start a new game from the sidebar to play again.")

# --------------------------------------------------------------------------
# HINT BANNER (based on last guess)
# --------------------------------------------------------------------------
if st.session_state.history and not st.session_state.game_over:
    last_guess, status = st.session_state.history[-1]
    distance = abs(last_guess - st.session_state.number)
    span = st.session_state.max_v - st.session_state.min_v
    closeness = 1 - (distance / span)

    if closeness > 0.93:
        st.markdown('<div class="hint-banner hint-hot">🔥 Super close! You\'re burning hot!</div>', unsafe_allow_html=True)
    elif status == "low":
        st.markdown('<div class="hint-banner hint-low">⬆️ Too low — guess higher!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint-banner hint-high">⬇️ Too high — guess lower!</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# GUESS HISTORY
# --------------------------------------------------------------------------
if st.session_state.history:
    st.markdown("**Guess history**")
    chips_html = ""
    for g, status in st.session_state.history:
        if status == "win":
            chips_html += f'<span class="chip chip-win">{g} 🎯</span>'
        elif status == "low":
            chips_html += f'<span class="chip chip-low">{g} ⬆️</span>'
        else:
            chips_html += f'<span class="chip chip-high">{g} ⬇️</span>'
    st.markdown(chips_html, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# END OF GAME
# --------------------------------------------------------------------------
if st.session_state.game_over:
    st.markdown("---")
    if st.session_state.won:
        st.balloons()
        st.success(f"🎉 You won, man! It took you **{st.session_state.count}** guess(es) to find **{st.session_state.number}**.")
    else:
        st.balloons()
        st.error(f"💥 Out of tries! The number was **{st.session_state.number}**. Better luck next round!")

    if st.button("🔁 Play Again", use_container_width=True):
        min_v, max_v, max_attempts = DIFFICULTIES[choice]
        start_new_game(min_v, max_v, max_attempts)
        st.rerun()