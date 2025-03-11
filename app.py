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
    """Render the team assignment section with drag and drop."""
    st.header("Team Assignment")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Available Players")
        for player in st.session_state.unassigned_players:
            with st.container(border=True):
                st.write(f"{player['Player']}: +{player['Increase']} stomps")
                target = st.selectbox(
                    "Drag to team",
                    ["Unassigned", "Team 1", "Team 2"],
                    key=f"select_{player['Player']}"
                )
                if target != "Unassigned":
                    if target == "Team 1":
                        st.session_state.team1_players.append(player)
                    else:
                        st.session_state.team2_players.append(player)
                    st.session_state.unassigned_players.remove(player)
                    st.rerun()

    with col2:
        st.subheader("Team 1")
        for player in st.session_state.team1_players:
            with st.container(border=True):
                st.write(f"{player['Player']}: +{player['Increase']} stomps")
                target = st.selectbox(
                    "Change team",
                    ["Team 1", "Unassigned", "Team 2"],
                    key=f"team1_{player['Player']}"
                )
                if target != "Team 1":
                    if target == "Unassigned":
                        st.session_state.unassigned_players.append(player)
                    else:
                        st.session_state.team2_players.append(player)
                    st.session_state.team1_players.remove(player)
                    st.rerun()

    with col3:
        st.subheader("Team 2")
        for player in st.session_state.team2_players:
            with st.container(border=True):
                st.write(f"{player['Player']}: +{player['Increase']} stomps")
                target = st.selectbox(
                    "Change team",
                    ["Team 2", "Unassigned", "Team 1"],
                    key=f"team2_{player['Player']}"
                )
                if target != "Team 2":
                    if target == "Unassigned":
                        st.session_state.unassigned_players.append(player)
                    else:
                        st.session_state.team1_players.append(player)
                    st.session_state.team2_players.remove(player)
                    st.rerun()

def render_team_statistics():
    """Render team statistics."""
    if st.session_state.team1_players or st.session_state.team2_players:
        st.header("Team Statistics")

        # Team 1 Statistics
        if st.session_state.team1_players:
            st.subheader("Team 1 Players")
            team1_df = pd.DataFrame(st.session_state.team1_players)

            # Individual player chart for Team 1
            fig1 = px.bar(team1_df,
                         x="Player",
                         y="Increase",
                         title="Team 1 Player Stomps",
                         color="Player")
            st.plotly_chart(fig1, use_container_width=True)

            # Team 1 total
            team1_total = sum(p['Increase'] for p in st.session_state.team1_players)
            st.metric("Team 1 Total Stomp Increase", team1_total)

        # Team 2 Statistics
        if st.session_state.team2_players:
            st.subheader("Team 2 Players")
            team2_df = pd.DataFrame(st.session_state.team2_players)

            # Individual player chart for Team 2
            fig2 = px.bar(team2_df,
                         x="Player",
                         y="Increase",
                         title="Team 2 Player Stomps",
                         color="Player")
            st.plotly_chart(fig2, use_container_width=True)

            # Team 2 total
            team2_total = sum(p['Increase'] for p in st.session_state.team2_players)
            st.metric("Team 2 Total Stomp Increase", team2_total)

def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    render_player_input()
    render_team_assignment()
    render_team_statistics()

if __name__ == "__main__":
    main()