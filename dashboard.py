import streamlit as st
import pandas as pd
from pathlib import Path

# --- CSV LOADING FUNCTION ---
@st.cache_data(ttl=5)
def load_data():
    csv_path = Path(__file__).parent / "value_bets.csv"
    
    if not csv_path.exists():
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()
        
    return pd.read_csv(csv_path)

# --- SESSION STATE TO TRACK TOP BET ---
if "last_top_bet" not in st.session_state:
    st.session_state.last_top_bet = None

# --- MAIN APP ---
st.title("⚽ Value Bets Dashboard")

# Sidebar slider filter
min_edge = st.sidebar.slider("Minimum edge %", 0.0, 0.5, 0.05)

# --- LOAD DATA ---
results_df = load_data()

if not results_df.empty:
    # Filter bets by minimum edge
    filtered_df = results_df[results_df["best_edge"] >= min_edge]

    # Highlight high edges
    def highlight_high_edges(row):
        color = "background-color: #b6fcd5" if row["best_edge"] > 0.1 else ""
        return [color] * len(row)

    st.subheader(f"Showing bets with edge ≥ {min_edge*100:.1f}%")
    st.dataframe(filtered_df.style.apply(highlight_high_edges, axis=1))

    # --- TOP BET ALERT ---
    top_bet = filtered_df.iloc[0]
    # Check if top bet has changed
    if st.session_state.last_top_bet != top_bet["match"]:
        st.session_state.last_top_bet = top_bet["match"]
        st.balloons()  # fun popup effect
        st.success(f"🔥 NEW TOP BET: {top_bet['match']} with edge {top_bet['best_edge']:.2f}")
    else:
        st.info(f"Top bet: {top_bet['match']} with edge {top_bet['best_edge']:.2f}")
else:
    st.warning("No data available.")