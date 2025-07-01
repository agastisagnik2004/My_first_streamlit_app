import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set wide layout
st.set_page_config(page_title="IPL Matches Dashboard", layout="wide")

# Load data with caching
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("matches.csv")
        data = data.dropna(subset=['season', 'player_of_match', 'result', 'winner', 'toss_decision'])
        data['season'] = data['season'].astype(str)
        data['result_margin'] = pd.to_numeric(data['result_margin'], errors='coerce')
        return data
    except FileNotFoundError:
        st.error("Error: matches.csv file not found.")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.stop()

# Title
st.title("IPL Matches Dashboard")

# Sidebar
st.sidebar.header("Player Profile")
players = sorted(df['player_of_match'].unique())
selected_player = st.sidebar.selectbox("Select Player of the Match", players)

# View toggle
view_option = st.radio("View Mode", ["Overall Stats", "Selected Player Stats"], horizontal=True)

# Filtered data for selected player
player_df = df[df['player_of_match'] == selected_player]

# Header
st.header("Match Statistics")

# Create columns
col1, col2 = st.columns(2)

# ----------- Visualizations -----------

# View: Overall or Player-specific
if view_option == "Overall Stats":
    # Matches per Season
    with col1:
        st.subheader("Matches per Season")
        matches_per_season = df['season'].value_counts().sort_index()
        fig1 = px.bar(x=matches_per_season.index, y=matches_per_season.values, 
                      labels={'x': 'Season', 'y': 'Number of Matches'},
                      title="Number of Matches per Season")
        fig1.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)

    # Result Distribution
    with col2:
        st.subheader("Match Result Distribution")
        result_counts = df['result'].value_counts()
        fig2 = px.pie(values=result_counts.values, names=result_counts.index, 
                      title="Distribution of Match Results")
        fig2.update_traces(textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    # Top Players
    st.subheader("Top 10 Players of the Match")
    top_players = df['player_of_match'].value_counts().head(10)
    fig3 = px.bar(x=top_players.index, y=top_players.values, 
                  labels={'x': 'Player', 'y': 'Awards'},
                  title="Most Player of the Match Awards")
    fig3.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig3, use_container_width=True)

    # Toss Decision
    with col1:
        st.subheader("Toss Decision Distribution")
        toss_decisions = df['toss_decision'].value_counts()
        fig4 = px.bar(x=toss_decisions.index, y=toss_decisions.values, 
                      labels={'x': 'Toss Decision', 'y': 'Count'},
                      title="Toss Decisions (Bat vs Field)")
        st.plotly_chart(fig4, use_container_width=True)

    # Top Teams
    with col2:
        st.subheader("Top Teams by Wins")
        team_wins = df['winner'].value_counts().head(10)
        fig5 = px.bar(x=team_wins.index, y=team_wins.values, 
                      labels={'x': 'Team', 'y': 'Wins'},
                      title="Top 10 Teams by Number of Wins")
        fig5.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)

    # Win Margin
    st.subheader("Win Margin Distribution")
    win_by_runs = df[df['result'] == 'runs']['result_margin'].dropna()
    win_by_wickets = df[df['result'] == 'wickets']['result_margin'].dropna()

    fig6 = go.Figure()
    fig6.add_trace(go.Histogram(x=win_by_runs, name='Wins by Runs', nbinsx=20, opacity=0.5))
    fig6.add_trace(go.Histogram(x=win_by_wickets, name='Wins by Wickets', nbinsx=20, opacity=0.5))
    fig6.update_layout(title="Distribution of Win Margins",
                       xaxis_title="Margin",
                       yaxis_title="Count",
                       barmode='overlay')
    st.plotly_chart(fig6, use_container_width=True)

else:
    # Stats for selected player
    st.subheader(f"🎯 Stats for: {selected_player}")
    st.write(f"Total 'Player of the Match' awards: {len(player_df)}")

    # Matches per season (for player)
    with col1:
        st.subheader("Awards per Season")
        season_awards = player_df['season'].value_counts().sort_index()
        fig_player_season = px.bar(x=season_awards.index, y=season_awards.values,
                                   labels={'x': 'Season', 'y': 'Awards'},
                                   title=f"{selected_player}'s Awards per Season")
        fig_player_season.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_player_season, use_container_width=True)

    # Winning team when player got award
    with col2:
        st.subheader("Teams When Player Won")
        team_win_counts = player_df['winner'].value_counts()
        fig_team = px.bar(x=team_win_counts.index, y=team_win_counts.values,
                          labels={'x': 'Team', 'y': 'Wins'},
                          title=f"Winning Teams When {selected_player} Got the Award")
        fig_team.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_team, use_container_width=True)

# Dataset Summary
st.header("Dataset Summary")
st.write(f"Total Matches: {len(df)}")
st.write(f"Seasons Covered: {df['season'].min()} to {df['season'].max()}")
st.write(f"Unique Teams: {df['team1'].nunique()}")
st.write(f"Unique Players of the Match: {df['player_of_match'].nunique()}")

# # Show raw data
# with st.expander("View Raw Data"):
#     st.dataframe(df)
