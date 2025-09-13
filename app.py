import streamlit as st
import random
import subprocess
import json
from difflib import SequenceMatcher

# --- Utility Functions ---
def similarity(a, b):
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def is_correct(guess, answer, threshold=0.75):
    return similarity(guess, answer) >= threshold

def get_puzzle_from_gemini(category="general"):
    """
    Calls Gemini CLI to fetch a new emoji puzzle in JSON.
    User can pick category: movies, phrases, songs, animals, etc.
    """
    prompt = f"You are an Emoji Puzzle Master. Generate ONE emoji puzzle in JSON format with keys 'puzzle' and 'answer'. Category: {category}."
    try:
        result = subprocess.run(
            ["gemini", "prompt", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        text = result.stdout.strip()
        return json.loads(text)
    except Exception as e:
        # Fallback to static puzzle if Gemini fails
        return random.choice([
            {"puzzle": "🦁👑", "answer": "The Lion King"},
            {"puzzle": "🎈🏠", "answer": "Up"},
            {"puzzle": "🐠🔍", "answer": "Finding Nemo"},
        ])

def new_puzzle():
    """Fetch puzzle (Gemini or fallback) and reset state."""
    category = st.session_state.get("category", "general")
    st.session_state.puzzle_data = get_puzzle_from_gemini(category)
    st.session_state.show_answer = False
    st.session_state.guess = ""  # auto-clear input

# --- Modern CSS ---
def get_css(theme):
    base_css = """
    .puzzle-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .puzzle-emoji {
        font-size: 4em;
        line-height: 1.4;
    }
    .score-box {
        font-size: 1.1em;
        font-weight: 600;
        text-align: right;
        margin-bottom: 10px;
    }
    """
    if theme == "Movies Night":
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #2c3e50, #4ca1af);
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
        }
        """
    elif theme == "Space Adventure":
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top, #0f2027, #203a43, #2c5364);
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #0f2027;
        }
        """
    else:  # Default
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #1f1c2c;
        }
        """

# --- App Start ---
st.sidebar.title("⚙️ Settings")

# Theme
theme = st.sidebar.selectbox("🎨 Theme", ["Default", "Movies Night", "Space Adventure"])

# Category for puzzles
category = st.sidebar.selectbox("📂 Category", ["general", "movies", "phrases", "songs", "animals", "food"])
st.session_state.category = category

st.markdown(f"<style>{get_css(theme)}</style>", unsafe_allow_html=True)

st.title("🎮 Emoji Puzzle Master")

# --- Session State ---
if "puzzle_data" not in st.session_state:
    st.session_state.win_count = 0
    st.session_state.goal = 5
    new_puzzle()

# --- Win Screen ---
if st.session_state.win_count >= st.session_state.goal:
    st.success("🏆 Congratulations! You’ve completed the challenge! 🎊")
    st.balloons()
    if st.button("Play Again"):
        st.session_state.win_count = 0
        new_puzzle()
    st.stop()

# --- Score ---
st.markdown(f"<div class='score-box'>Score: {st.session_state.win_count}/{st.session_state.goal}</div>", unsafe_allow_html=True)
st.progress(st.session_state.win_count / st.session_state.goal)

# --- Puzzle Card ---
st.markdown("<div class='puzzle-card'>", unsafe_allow_html=True)
st.subheader(f"Category: {st.session_state.category.capitalize()}")
st.markdown(f"<div class='puzzle-emoji'>{st.session_state.puzzle_data['puzzle']}</div>", unsafe_allow_html=True)

# --- Input ---
guess = st.text_input("Your Guess:", key="guess", placeholder="Type your guess here...")

# --- Buttons ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Submit"):
        if is_correct(guess, st.session_state.puzzle_data["answer"]):
            st.success("✅ Correct! 🎉")
            st.toast("🔥 Great job!")
            st.session_state.win_count += 1
            new_puzzle()
        else:
            st.error("❌ Not quite. Try again!")
with col2:
    if st.button("Show Answer"):
        st.session_state.show_answer = True
with col3:
    st.button("Skip", on_click=new_puzzle)

# --- Show Answer ---
if st.session_state.get("show_answer", False):
    st.info(f"The answer is: **{st.session_state.puzzle_data['answer']}**")

st.markdown("</div>", unsafe_allow_html=True)
