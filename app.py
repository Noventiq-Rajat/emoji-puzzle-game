import streamlit as st
import random
from difflib import SequenceMatcher


# --- Realtime Puzzle Generation (simulated) ---
# A larger, more diverse list of puzzles to simulate realtime generation.
realtime_puzzles = [
    # Movies
    {"puzzle": "🕷️👨‍🦱➡️️🕷️👨", "answer": "Spider-Man: Into the Spider-Verse", "category": "Movies"},
    {"puzzle": "🚗💨😡", "answer": "Fast & Furious", "category": "Movies"},
    {"puzzle": "🧙‍♂️💍⛰️", "answer": "The Lord of the Rings", "category": "Movies"},
    {"puzzle": "🧑‍🚀🌌⭐", "answer": "Interstellar", "category": "Movies"},
    {"puzzle": "🤠🚀", "answer": "Toy Story", "category": "Movies"},
    {"puzzle": "🏴‍☠️🌊💎", "answer": "Pirates of the Caribbean", "category": "Movies"},
    {"puzzle": "🦁👑", "answer": "The Lion King", "category": "Movies"},
    {"puzzle": "🎈🏠", "answer": "Up", "category": "Movies"},
    {"puzzle": "🐠🔍", "answer": "Finding Nemo", "category": "Movies"},
    {"puzzle": "👨‍🍳🐀", "answer": "Ratatouille", "category": "Movies"},
    {"puzzle": "🤖❤️🤖", "answer": "WALL-E", "category": "Movies"},
    {"puzzle": "🕷️👨", "answer": "Spider-Man", "category": "Movies"},
    # Phrases
    {"puzzle": "🍎➡️️🌳", "answer": "The apple doesn't fall far from the tree", "category": "Phrases"},
    {"puzzle": "🐦➡️️🗣️", "answer": "A little bird told me", "category": "Phrases"},
    {"puzzle": "💰🗣️", "answer": "Money talks", "category": "Phrases"},
    {"puzzle": "🔥+💧", "answer": "Opposites attract", "category": "Phrases"},
    {"puzzle": "🕰️✈️", "answer": "Time flies", "category": "Phrases"},
    {"puzzle": "🤔🐱💀", "answer": "Curiosity killed the cat", "category": "Phrases"},
]

def generate_realtime_puzzle(category=None):
    """Generates a new puzzle, simulating a realtime API call."""
    if category and category != "Any":
        filtered_puzzles = [p for p in realtime_puzzles if p["category"] == category]
        if filtered_puzzles:
            return random.choice(filtered_puzzles)
    return random.choice(realtime_puzzles)


# --- CSS Themes ---
def get_css(theme):
    base_css = """
    /* Sidebar text fix */
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox span {
    }

    /* Button styles */
    .stButton button {
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: scale(1.05);
    }
    #submit_btn .stButton button {background-color: #4CAF50 !important;}  /* Green */
    #answer_btn .stButton button {background-color: #FFC107 !important;}  /* Yellow */
    #skip_btn .stButton button {background-color: #F44336 !important;}    /* Red */
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
    """Select new puzzle by category using realtime generation"""
    st.session_state.puzzle_data = generate_realtime_puzzle(category)
    st.session_state.show_answer = False
    # The line below is removed to prevent the error. The trade-off is that the input box is not cleared.
    # st.session_state.guess = ""


# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.selectbox("🎨 Theme", ["Default", "Movies Night", "Space Adventure"])
category = st.sidebar.selectbox("📂 Category", ["Any", "Movies", "Phrases"])

# --- Handle Category Change ---
if "selected_category" not in st.session_state:
    st.session_state.selected_category = category

if st.session_state.selected_category != category:
    st.session_state.selected_category = category
    new_puzzle(category if category != "Any" else None)
    st.experimental_rerun()


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
    new_puzzle(category if category != "Any" else None)

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
    st.markdown("<div id='submit_btn'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div id='answer_btn'>", unsafe_allow_html=True)
    if st.button("Show Answer"):
        st.session_state.show_answer = True
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div id='skip_btn'>", unsafe_allow_html=True)
    if st.button("Skip"):
        new_puzzle(category if category != "Any" else None)
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Show answer ---
if st.session_state.get("show_answer", False):
    st.info(f"The answer is: **{st.session_state.puzzle_data['answer']}**")

st.markdown("</div>", unsafe_allow_html=True)
