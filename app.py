import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.title("Baddies Stomp Counter")
    st.markdown("""
    1. Add player stats below
    2. View team statistics
    """)

def render_player_input():
    """Render the player input section."""
    st.header("Add Player Stats")

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

def render_penalty_input():
    """Render the penalty input section."""
    st.header("Add Penalty")

    col1, col2, col3 = st.columns(3)

    with col1:
        penalty_name = st.text_input("Penalty Description")
    with col2:
        penalty_amount = st.number_input("Amount", min_value=0, value=0)
    with col3:
        team = st.selectbox("Team", ["Team 1", "Team 2"], key="penalty_team")

    if st.button("Add Penalty"):
        if penalty_name and penalty_amount > 0:
            new_penalty = {
                "Name": penalty_name,
                "Score Before": "N/A",
                "Score After": "N/A",
                "Difference": -penalty_amount  # Make penalties negative
            }
            if team == "Team 1":
                st.session_state.team1_penalties.append(new_penalty)
            else:
                st.session_state.team2_penalties.append(new_penalty)
            st.success(f"Added penalty to {team}")
        else:
            st.error("Please enter valid penalty information.")

def render_team_statistics():
    """Render team statistics."""
    if st.session_state.team1_players:
        st.header("Team 1")
        # Combine players and penalties for display
        team1_data = st.session_state.team1_players + st.session_state.team1_penalties
        if team1_data:
            # Calculate total including penalties
            team1_total = (
                sum(p['Difference'] for p in st.session_state.team1_players) +
                sum(p['Difference'] for p in st.session_state.team1_penalties)
            )
            # Create total row
            total_row = [{
                'Name': 'TOTAL',
                'Score Before': sum(p['Score Before'] for p in st.session_state.team1_players if isinstance(p['Score Before'], (int, float))),
                'Score After': sum(p['Score After'] for p in st.session_state.team1_players if isinstance(p['Score After'], (int, float))),
                'Difference': team1_total
            }]
            # Create DataFrame with all data
            team1_df = pd.DataFrame(team1_data + total_row)
            st.dataframe(team1_df, hide_index=True, use_container_width=True)

            # Delete buttons
            for idx, item in enumerate(team1_data):
                if st.button(f"Delete {item['Name']}", key=f"delete_team1_{idx}"):
                    if item in st.session_state.team1_players:
                        st.session_state.team1_players.remove(item)
                    else:
                        st.session_state.team1_penalties.remove(item)
                    st.rerun()

    if st.session_state.team2_players:
        st.header("Team 2")
        # Combine players and penalties for display
        team2_data = st.session_state.team2_players + st.session_state.team2_penalties
        if team2_data:
            # Calculate total including penalties
            team2_total = (
                sum(p['Difference'] for p in st.session_state.team2_players) +
                sum(p['Difference'] for p in st.session_state.team2_penalties)
            )
            # Create total row
            total_row = [{
                'Name': 'TOTAL',
                'Score Before': sum(p['Score Before'] for p in st.session_state.team2_players if isinstance(p['Score Before'], (int, float))),
                'Score After': sum(p['Score After'] for p in st.session_state.team2_players if isinstance(p['Score After'], (int, float))),
                'Difference': team2_total
            }]
            # Create DataFrame with all data
            team2_df = pd.DataFrame(team2_data + total_row)
            st.dataframe(team2_df, hide_index=True, use_container_width=True)

            # Delete buttons
            for idx, item in enumerate(team2_data):
                if st.button(f"Delete {item['Name']}", key=f"delete_team2_{idx}"):
                    if item in st.session_state.team2_players:
                        st.session_state.team2_players.remove(item)
                    else:
                        st.session_state.team2_penalties.remove(item)
                    st.rerun()

def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    render_player_input()
    render_penalty_input()
    render_team_statistics()

if __name__ == "__main__":
    main()