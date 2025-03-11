import streamlit as st
import pandas as pd
import plotly.express as px

def initialize_session_state():
    """Initialize session state variables."""
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'team1' not in st.session_state:
        st.session_state.team1 = []
    if 'team2' not in st.session_state:
        st.session_state.team2 = []

def render_header():
    """Render the application header."""
    st.title("Baddies Stomp Counter")
    st.markdown("""
    Track individual player stomps and team performance.
    Add players and their stomp counts below.
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
            st.session_state.players.append(new_player)
            st.success(f"Added {player_name}'s stats!")
        else:
            st.error("Please enter valid player information.")

def render_player_stats():
    """Render the player statistics section."""
    if st.session_state.players:
        st.header("Player Statistics")

        df = pd.DataFrame(st.session_state.players)
        st.dataframe(df, hide_index=True)

        # Visualization
        fig = px.bar(df, 
                    x="Player", 
                    y="Increase",
                    title="Stomp Increases by Player",
                    labels={"Increase": "Stomp Increase"})
        st.plotly_chart(fig, use_container_width=True)

def render_team_comparison():
    """Render the team comparison section."""
    st.header("Team Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Team 1")
        team1_name = st.text_input("Team 1 Name", value="Team 1")
        team1_start = st.number_input("Team 1 Start Stomps", min_value=0, value=0)
        team1_end = st.number_input("Team 1 End Stomps", min_value=0, value=0)

    with col2:
        st.subheader("Team 2")
        team2_name = st.text_input("Team 2 Name", value="Team 2")
        team2_start = st.number_input("Team 2 Start Stomps", min_value=0, value=0)
        team2_end = st.number_input("Team 2 End Stomps", min_value=0, value=0)

    if st.button("Compare Teams"):
        team_data = pd.DataFrame({
            "Team": [team1_name, team2_name],
            "Start Stomps": [team1_start, team2_start],
            "End Stomps": [team1_end, team2_end],
            "Increase": [team1_end - team1_start, team2_end - team2_start]
        })

        st.dataframe(team_data, hide_index=True)

        # Team comparison visualization
        fig = px.bar(team_data,
                    x="Team",
                    y=["Start Stomps", "End Stomps"],
                    title="Team Stomps Comparison",
                    barmode="group")
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    render_player_input()
    render_player_stats()
    render_team_comparison()

if __name__ == "__main__":
    main()