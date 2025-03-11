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
    2. View team statistics and penalties
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
                "Description": penalty_name,
                "Amount": penalty_amount
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
        team1_df = pd.DataFrame(st.session_state.team1_players)
        if not team1_df.empty:
            # Calculate total before displaying
            team1_total = sum(p['Difference'] for p in st.session_state.team1_players)
            # Add total row
            total_row = pd.DataFrame([{
                'Name': 'TOTAL',
                'Score Before': team1_df['Score Before'].sum(),
                'Score After': team1_df['Score After'].sum(),
                'Difference': team1_total
            }])
            team1_df = pd.concat([team1_df, total_row])
            st.dataframe(team1_df, hide_index=True, use_container_width=True)

            # Delete buttons for players
            for idx, player in enumerate(st.session_state.team1_players):
                if st.button(f"Delete {player['Name']}", key=f"delete_team1_{idx}"):
                    st.session_state.team1_players.pop(idx)
                    st.rerun()

        # Show penalties if any
        if st.session_state.team1_penalties:
            st.subheader("Team 1 Penalties")
            penalties_df = pd.DataFrame(st.session_state.team1_penalties)
            st.dataframe(penalties_df, hide_index=True, use_container_width=True)
            # Delete buttons for penalties
            for idx, penalty in enumerate(st.session_state.team1_penalties):
                if st.button(f"Delete Penalty {penalty['Description']}", key=f"delete_penalty_team1_{idx}"):
                    st.session_state.team1_penalties.pop(idx)
                    st.rerun()

    if st.session_state.team2_players:
        st.header("Team 2")
        team2_df = pd.DataFrame(st.session_state.team2_players)
        if not team2_df.empty:
            # Calculate total before displaying
            team2_total = sum(p['Difference'] for p in st.session_state.team2_players)
            # Add total row
            total_row = pd.DataFrame([{
                'Name': 'TOTAL',
                'Score Before': team2_df['Score Before'].sum(),
                'Score After': team2_df['Score After'].sum(),
                'Difference': team2_total
            }])
            team2_df = pd.concat([team2_df, total_row])
            st.dataframe(team2_df, hide_index=True, use_container_width=True)

            # Delete buttons for players
            for idx, player in enumerate(st.session_state.team2_players):
                if st.button(f"Delete {player['Name']}", key=f"delete_team2_{idx}"):
                    st.session_state.team2_players.pop(idx)
                    st.rerun()

        # Show penalties if any
        if st.session_state.team2_penalties:
            st.subheader("Team 2 Penalties")
            penalties_df = pd.DataFrame(st.session_state.team2_penalties)
            st.dataframe(penalties_df, hide_index=True, use_container_width=True)
            # Delete buttons for penalties
            for idx, penalty in enumerate(st.session_state.team2_penalties):
                if st.button(f"Delete Penalty {penalty['Description']}", key=f"delete_penalty_team2_{idx}"):
                    st.session_state.team2_penalties.pop(idx)
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