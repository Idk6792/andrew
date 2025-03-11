import streamlit as st
import pandas as pd

def set_page_style():
    """Set custom page styling."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Concert+One&display=swap');

        html, body, [class*="css"] {
            font-family: 'Concert One', cursive;
        }

        h1 {
            font-family: 'Concert One', cursive;
            text-align: center;
            color: #333;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #000;
        }

        .stButton button {
            font-family: 'Concert One', cursive;
            border-radius: 20px;
            transition: all 0.3s ease;
            border: 2px solid #333;
        }

        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .header-border {
            text-align: center;
            padding: 1rem;
            margin-bottom: 2rem;
        }

        .section-title {
            text-align: center;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #000;
        }

        .divider {
            text-align: center;
            margin: 1rem 0;
            color: #333;
            font-size: 16px;
        }

        .blooming-flower {
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 24px;
            animation: bloom 2s ease-in-out infinite;
        }

        @keyframes bloom {
            0% { transform: scale(0.5) rotate(-10deg); opacity: 0; }
            50% { transform: scale(1.2) rotate(10deg); opacity: 1; }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        </style>
        <div class="blooming-flower">✿</div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'team1_players' not in st.session_state:
        st.session_state.team1_players = []
    if 'team2_players' not in st.session_state:
        st.session_state.team2_players = []
    if 'team1_penalties' not in st.session_state:
        st.session_state.team1_penalties = []
    if 'team2_penalties' not in st.session_state:
        st.session_state.team2_penalties = []

def render_header():
    """Render the application header."""
    st.markdown('<div class="header-border">', unsafe_allow_html=True)
    st.markdown("# Andrew's Baddies Stomp Counter")
    st.markdown('<div class="divider">ᵔᴗᵔ ⟡ ✿ ⟡ ᵔᴗᵔ</div>', unsafe_allow_html=True)
    st.markdown("""
    1. Add player stats below
    2. View team statistics
    """)
    st.markdown('<div class="divider">﹒ʬʬ﹒⪩⪨﹒⟡﹒ᐢ..ᐢ</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_player_input():
    """Render the player input section."""
    st.markdown('<div class="section-title">Add Player Stats</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider">✿ ⟡ ✿</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        player_name = st.text_input("Name")
    with col2:
        score_before = st.number_input("Score Before", min_value=0, value=0)
    with col3:
        score_after = st.number_input("Score After", min_value=0, value=0)
    with col4:
        team = st.selectbox("Team", ["Team 1", "Team 2"])

    if st.button("Add Player"):
        if player_name and score_after >= score_before:
            new_player = {
                "Name": player_name,
                "Score Before": score_before,
                "Score After": score_after,
                "Difference": score_after - score_before
            }
            if team == "Team 1":
                st.session_state.team1_players.append(new_player)
            else:
                st.session_state.team2_players.append(new_player)
            st.success(f"Added {player_name}'s stats!")
        else:
            st.error("Please enter valid player information.")

    st.markdown('<div class="divider">﹒✿﹒⊹﹒∇﹒✸</div>', unsafe_allow_html=True)

def render_penalty_input():
    """Render the penalty input section."""
    st.markdown('<div class="section-title">Add Penalty</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider">⟡ ᐢ..ᐢ ⟡</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        penalty_name = st.text_input("Penalty Description")
    with col2:
        penalty_amount = st.number_input("Amount", min_value=0, value=0)
    with col3:
        team = st.selectbox("Select Team", ["Team 1", "Team 2"], key="penalty_team")

    if st.button("Add Penalty"):
        if penalty_name and penalty_amount > 0:
            new_penalty = {
                "Name": penalty_name,
                "Score Before": "N/A",
                "Score After": "N/A",
                "Difference": -penalty_amount
            }
            if team == "Team 1":
                st.session_state.team1_penalties.append(new_penalty)
            else:
                st.session_state.team2_penalties.append(new_penalty)
            st.success(f"Added penalty to {team}")
        else:
            st.error("Please enter valid penalty information.")

    st.markdown('<div class="divider">﹒⟢﹒❀﹒ᵔᴗᵔ﹒♡</div>', unsafe_allow_html=True)

def render_team_statistics():
    """Render team statistics."""
    if st.session_state.team1_players:
        st.markdown('<div class="section-title">Team 1</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider">⟡ ✿ ⟡</div>', unsafe_allow_html=True)
        team1_data = st.session_state.team1_players + st.session_state.team1_penalties
        if team1_data:
            team1_total = (
                sum(p['Difference'] for p in st.session_state.team1_players) +
                sum(p['Difference'] for p in st.session_state.team1_penalties)
            )
            total_row = [{
                'Name': 'TOTAL',
                'Score Before': sum(p['Score Before'] for p in st.session_state.team1_players if isinstance(p['Score Before'], (int, float))),
                'Score After': sum(p['Score After'] for p in st.session_state.team1_players if isinstance(p['Score After'], (int, float))),
                'Difference': team1_total
            }]
            team1_df = pd.DataFrame(team1_data + total_row)
            st.dataframe(team1_df, hide_index=True, use_container_width=True)

            for idx, item in enumerate(team1_data):
                if st.button(f"Delete {item['Name']}", key=f"delete_team1_{idx}"):
                    if item in st.session_state.team1_players:
                        st.session_state.team1_players.remove(item)
                    else:
                        st.session_state.team1_penalties.remove(item)
                    st.rerun()

    if st.session_state.team2_players:
        st.markdown('<div class="section-title">Team 2</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider">⟡ ✿ ⟡</div>', unsafe_allow_html=True)
        team2_data = st.session_state.team2_players + st.session_state.team2_penalties
        if team2_data:
            team2_total = (
                sum(p['Difference'] for p in st.session_state.team2_players) +
                sum(p['Difference'] for p in st.session_state.team2_penalties)
            )
            total_row = [{
                'Name': 'TOTAL',
                'Score Before': sum(p['Score Before'] for p in st.session_state.team2_players if isinstance(p['Score Before'], (int, float))),
                'Score After': sum(p['Score After'] for p in st.session_state.team2_players if isinstance(p['Score After'], (int, float))),
                'Difference': team2_total
            }]
            team2_df = pd.DataFrame(team2_data + total_row)
            st.dataframe(team2_df, hide_index=True, use_container_width=True)

            for idx, item in enumerate(team2_data):
                if st.button(f"Delete {item['Name']}", key=f"delete_team2_{idx}"):
                    if item in st.session_state.team2_players:
                        st.session_state.team2_players.remove(item)
                    else:
                        st.session_state.team2_penalties.remove(item)
                    st.rerun()

def render_summary():
    """Render the summary section with winning team and overview."""
    if st.session_state.team1_players or st.session_state.team2_players:
        st.markdown("---")
        st.markdown('<div class="divider">﹒⟢﹒❀﹒ᵔᴗᵔ﹒♡﹒〇﹒ıllı</div>', unsafe_allow_html=True)

        team1_total = (
            sum(p['Difference'] for p in st.session_state.team1_players) +
            sum(p['Difference'] for p in st.session_state.team1_penalties)
        )
        team2_total = (
            sum(p['Difference'] for p in st.session_state.team2_players) +
            sum(p['Difference'] for p in st.session_state.team2_penalties)
        )

        st.write("winning team:")
        if team1_total > team2_total:
            st.write(f"Team 1 ({team1_total})")
        elif team2_total > team1_total:
            st.write(f"Team 2 ({team2_total})")
        else:
            st.write("Tie!")

        st.write("OVERVIEW")

        st.write("Team 1:")
        st.write(f"total stomps: {team1_total}")
        if st.session_state.team1_players:
            st.write("top 3 players:")
            top_players = sorted(
                [p for p in st.session_state.team1_players if isinstance(p['Difference'], (int, float))],
                key=lambda x: x['Difference'],
                reverse=True
            )[:3]
            for player in top_players:
                st.write(f"{player['Name']} | {player['Difference']}")

        st.write("Team 2:")
        st.write(f"total stomps: {team2_total}")
        if st.session_state.team2_players:
            st.write("top 3 players:")
            top_players = sorted(
                [p for p in st.session_state.team2_players if isinstance(p['Difference'], (int, float))],
                key=lambda x: x['Difference'],
                reverse=True
            )[:3]
            for player in top_players:
                st.write(f"{player['Name']} | {player['Difference']}")

def main():
    """Main application function."""
    set_page_style()
    initialize_session_state()
    render_header()
    render_player_input()
    render_penalty_input()
    render_team_statistics()
    render_summary()

if __name__ == "__main__":
    main()