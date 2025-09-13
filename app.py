import streamlit as st
import random
from difflib import SequenceMatcher


# --- Puzzles ---
puzzles = [
    {"puzzle": "🦁👑", "answer": "The Lion King", "category": "Movies"},
    {"puzzle": "🎈🏠", "answer": "Up", "category": "Movies"},
    {"puzzle": "🐠🔍", "answer": "Finding Nemo", "category": "Movies"},
    {"puzzle": "🕰️✈️", "answer": "Time flies", "category": "Phrases"},
    {"puzzle": "🤔🐱💀", "answer": "Curiosity killed the cat", "category": "Phrases"},
    {"puzzle": "👨‍🍳🐀", "answer": "Ratatouille", "category": "Movies"},
    {"puzzle": "🤖❤️🤖", "answer": "WALL-E", "category": "Movies"},
    {"puzzle": "🕷️👨", "answer": "Spider-Man", "category": "Movies"},
]

# --- CSS Themes ---
def get_css(theme):
    base_css = """
    .puzzle-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        text-align: center;
        margin-top: 20px;
    }
    input {
        border-radius: 10px !important;
        padding: 10px !important;
    }
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] button {
        color: white !important;
    }
    """
    if theme == "Movies Night":
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
        }
        [data-testid="stSidebar"] {
            background: #1e3c72;
        }
        """
    elif theme == "Space Adventure":
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #000428, #004e92);
            color: white;
        }
        [data-testid="stSidebar"] {
            background: #000428;
        }
        """
    else:  # Default modern purple
        return base_css + """
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #3a1c71, #d76d77, #ffaf7b);
            color: white;
        }
        [data-testid="stSidebar"] {
            background: #3a1c71;
        }
        """

# --- Helpers ---
def is_correct(guess, answer):
    """Fuzzy matching for flexible answers"""
    return SequenceMatcher(None, guess.lower().strip(), answer.lower().strip()).ratio() > 0.8

def new_puzzle(category=None):
    """Select new puzzle by category"""
    if category:
        filtered = [p for p in puzzles if p["category"].lower() == category.lower()]
        if filtered:
            st.session_state.puzzle_data = random.choice(filtered)
            return
    st.session_state.puzzle_data = random.choice(puzzles)
    st.session_state.show_answer = False
    st.session_state.guess = ""

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.selectbox("🎨 Theme", ["Default", "Movies Night", "Space Adventure"])
category = st.sidebar.selectbox("📂 Category", ["Any", "Movies", "Phrases"])

# --- Apply CSS ---
st.markdown(f"<style>{get_css(theme)}</style>", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    """
    <h1 style='text-align: center; color: white; font-size: 2.8em; margin-bottom: 10px;'>
        🎮 Emoji Puzzle Master
    </h1>
    """,
    unsafe_allow_html=True
)

# --- Init state ---
if "puzzle_data" not in st.session_state:
    st.session_state.win_count = 0
    st.session_state.streak = 0
    new_puzzle(category=None)

# --- Score ---
goal = 5
st.markdown(f"<div style='text-align: right; font-size:1.1em;'>Score: {st.session_state.win_count}/{goal}</div>", unsafe_allow_html=True)
st.progress(st.session_state.win_count / goal)

# --- Puzzle card ---
st.markdown("<div class='puzzle-card'>", unsafe_allow_html=True)
st.subheader(f"Category: {st.session_state.puzzle_data.get('category','Unknown')}")

st.markdown(
    f"<h1 style='font-size: 4.5em; margin: 20px 0;'>{st.session_state.puzzle_data['puzzle']}</h1>",
    unsafe_allow_html=True
)

# --- User input ---
guess = st.text_input("Your Guess:", key="guess", placeholder="Type your guess here...")

# --- Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit"):
        if is_correct(guess, st.session_state.puzzle_data["answer"]):
            st.success("✅ Correct! 🎉")
            st.balloons()
            st.session_state.win_count += 1
            st.session_state.streak += 1
            if st.session_state.win_count >= goal:
                st.success("🏆 You’ve completed the game! 🎊")
                if st.button("Play Again"):
                    st.session_state.win_count = 0
                    st.session_state.streak = 0
                    new_puzzle(category if category != "Any" else None)
                    st.experimental_rerun()
            else:
                new_puzzle(category if category != "Any" else None)
                st.experimental_rerun()
        else:
            st.error("❌ Incorrect. Try again!")
            st.session_state.streak = 0

with col2:
    if st.button("Show Answer"):
        st.session_state.show_answer = True

with col3:
    if st.button("Skip"):
        new_puzzle(category if category != "Any" else None)
        st.experimental_rerun()

# --- Show answer ---
if st.session_state.get("show_answer", False):
    st.info(f"The answer is: **{st.session_state.puzzle_data['answer']}**")

st.markdown("</div>", unsafe_allow_html=True)
