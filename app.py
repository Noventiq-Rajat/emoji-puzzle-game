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
    /* Puzzle Card */
    # .puzzle-card {
    #     background: rgba(255, 255, 255, 0.15);
    #     border-radius: 20px;
    #     padding: 30px;
    #     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    #     backdrop-filter: blur(10px);
    #     border: 1px solid rgba(255, 255, 255, 0.2);
    #     text-align: center;
    #     margin-top: 20px;
    #     transition: transform 0.2s ease-in-out;
    # }
    # .puzzle-card:hover {
    #     transform: scale(1.02);
    # }

    /* Sidebar text fix */
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox span {
        color: white !important;
    }

    /* Button styles */
    .stButton button {
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        color: white !important;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: scale(1.05);
    }
    #submit_btn button {background-color: #4CAF50 !important;}  /* Green */
    #answer_btn button {background-color: #FFC107 !important;}  /* Yellow */
    #skip_btn button {background-color: #F44336 !important;}    /* Red */
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
    else:  # Default purple theme
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

# --- Puzzle card wrapper (everything goes inside now) ---
st.markdown("<div class='puzzle-card'>", unsafe_allow_html=True)

# --- Score ---
goal = 5
st.markdown(
    f"<div style='text-align: right; font-size:1.1em;'>Score: {st.session_state.win_count}/{goal}</div>",
    unsafe_allow_html=True
)
st.progress(st.session_state.win_count / goal)

# --- Puzzle ---
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
    if st.button("Submit", key="submit_btn"):
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
    if st.button("Show Answer", key="answer_btn"):
        st.session_state.show_answer = True

with col3:
    if st.button("Skip", key="skip_btn"):
        new_puzzle(category if category != "Any" else None)
        st.experimental_rerun()

# --- Show answer ---
if st.session_state.get("show_answer", False):
    st.info(f"The answer is: **{st.session_state.puzzle_data['answer']}**")

st.markdown("</div>", unsafe_allow_html=True)
