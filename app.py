import streamlit as st
import pandas as pd
import plotly.express as px

def initialize_session_state():
    """Initialize session state variables."""
    if 'unassigned_players' not in st.session_state:
        st.session_state.unassigned_players = []
    if 'team1_players' not in st.session_state:
        st.session_state.team1_players = []
    if 'team2_players' not in st.session_state:
        st.session_state.team2_players = []

def render_header():
    """Render the application header."""
    st.title("Baddies Stomp Counter")
    st.markdown("""
    1. Add player stats below
    2. Use the team assignment section to organize players into teams
    3. View team statistics and comparisons
    """)

def render_player_input():
    """Render the player input section."""
    st.header("Add Player Stats")

    col1, col2, col3 = st.columns(3)

    with col1:
        player_name = st.text_input("Player Name")
    with col2:
        start_stomps = st.number_input("Start Stomps", min_value=0, value=0)
    with col3:
        end_stomps = st.number_input("End Stomps", min_value=0, value=0)

    if st.button("Add Player"):
        if player_name and end_stomps >= start_stomps:
            new_player = {
                "Player": player_name,
                "Start Stomps": start_stomps,
                "End Stomps": end_stomps,
                "Increase": end_stomps - start_stomps
            }
            st.session_state.unassigned_players.append(new_player)
            st.success(f"Added {player_name}'s stats!")
        else:
            st.error("Please enter valid player information.")

def render_team_assignment():
    """Render the team assignment section."""
    st.header("Team Assignment")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Available Players")
        for i, player in enumerate(st.session_state.unassigned_players):
            if st.button(f"➡️ {player['Player']} (+{player['Increase']} stomps)", key=f"unassigned_{i}"):
                team = st.radio(f"Select team for {player['Player']}", ["Team 1", "Team 2"])
                if team == "Team 1":
                    st.session_state.team1_players.append(player)
                else:
                    st.session_state.team2_players.append(player)
                st.session_state.unassigned_players.remove(player)
                st.rerun()

    with col2:
        st.subheader("Team 1")
        for i, player in enumerate(st.session_state.team1_players):
            if st.button(f"❌ {player['Player']} (+{player['Increase']} stomps)", key=f"team1_{i}"):
                st.session_state.unassigned_players.append(player)
                st.session_state.team1_players.remove(player)
                st.rerun()

    with col3:
        st.subheader("Team 2")
        for i, player in enumerate(st.session_state.team2_players):
            if st.button(f"❌ {player['Player']} (+{player['Increase']} stomps)", key=f"team2_{i}"):
                st.session_state.unassigned_players.append(player)
                st.session_state.team2_players.remove(player)
                st.rerun()

def render_team_statistics():
    """Render team statistics."""
    if st.session_state.team1_players or st.session_state.team2_players:
        st.header("Team Statistics")

        # Calculate team totals
        team1_total_increase = sum(p['Increase'] for p in st.session_state.team1_players)
        team2_total_increase = sum(p['Increase'] for p in st.session_state.team2_players)

        # Create team comparison DataFrame
        team_data = pd.DataFrame({
            "Team": ["Team 1", "Team 2"],
            "Players": [len(st.session_state.team1_players), len(st.session_state.team2_players)],
            "Total Stomp Increase": [team1_total_increase, team2_total_increase]
        })

        # Display team comparison
        st.dataframe(team_data, hide_index=True)

        # Create team comparison visualization
        fig = px.bar(team_data,
                    x="Team",
                    y="Total Stomp Increase",
                    title="Team Stomp Comparison",
                    color="Team")
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    render_player_input()
    render_team_assignment()
    render_team_statistics()

if __name__ == "__main__":
    main()