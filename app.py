import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('netflix_titles.csv')
df.fillna("Unknown", inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['month_added'] = df['date_added'].dt.month_name()
df['duration_minutes'] = df['duration'].str.extract(r'(\d+)').astype(float)

def main():
    st.title("Netflix Exploratory Data Analysis")

    # Sidebar
    st.sidebar.header("Filters")
    selected_type = st.sidebar.radio("Select Type", ["All", "Movie", "TV Show"])

    # Filter dataset
    filtered_df = df if selected_type == "All" else df[df["type"] == selected_type]

    

    # Top 10 Genres
    genres = df["listed_in"].str.split(", ").explode().value_counts().head(10)
    fig2 = px.bar(y=genres.index, x=genres.values, orientation='h', 
                  labels={'x': 'Count', 'y': 'Genre'},
                  title="Top 10 Genres", color=genres.values)
    st.plotly_chart(fig2)

    # Release Trend Over Years
    fig3 = px.histogram(df, x='release_year', nbins=15, title="Release Trend Over Years", color_discrete_sequence=["red"])
    st.plotly_chart(fig3)

    # Top 10 Countries Producing Content
    top_countries = df["country"].value_counts().head(10)
    fig4 = px.bar(y=top_countries.index, x=top_countries.values, orientation='h',
                  labels={'x': 'Count', 'y': 'Country'},
                  title="Top 10 Countries Producing Content", color=top_countries.values)
    st.plotly_chart(fig4)

    # Content Ratings Distribution
    ratings = df["rating"].value_counts()
    fig5 = px.bar(y=ratings.index, x=ratings.values, orientation='h',
                  labels={'x': 'Count', 'y': 'Rating'},
                  title="Content Ratings Distribution", color=ratings.values)
    st.plotly_chart(fig5)

    # Monthly Additions Trend
    fig6 = px.histogram(df, x='month_added', title="Monthly Additions Trend",
                        category_orders={"month_added": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]})
    st.plotly_chart(fig6)

    # Top 10 Directors
    top_directors = df[df['director'] != "Unknown"]["director"].value_counts().head(10)
    fig7 = px.bar(y=top_directors.index, x=top_directors.values, orientation='h',
                  labels={'x': 'Count', 'y': 'Director'},
                  title="Top 10 Directors", color=top_directors.values)
    st.plotly_chart(fig7)

    # Movie Durations Distribution
    fig8 = px.histogram(df[df['type'] == "Movie"], x='duration_minutes', nbins=30,
                        title="Distribution of Movie Durations", color_discrete_sequence=["purple"])
    st.plotly_chart(fig8)

    # Top 5 Longest Movies
    longest_movies = df[df['type'] == "Movie"].nlargest(5, 'duration_minutes')[['title', 'duration_minutes']]
    fig9 = px.bar(longest_movies, y='title', x='duration_minutes', orientation='h',
                  title="Top 5 Longest Movies", color='duration_minutes')
    st.plotly_chart(fig9)

    # Top 5 Shortest Movies
    shortest_movies = df[df['type'] == "Movie"].nsmallest(5, 'duration_minutes')[['title', 'duration_minutes']]
    fig10 = px.bar(shortest_movies, y='title', x='duration_minutes', orientation='h',
                   title="Top 5 Shortest Movies", color='duration_minutes')
    st.plotly_chart(fig10)

    # Top 10 Actors
    top_actors = df[df['cast'] != "Unknown"]["cast"].str.split(", ").explode().value_counts().head(10)
    fig11 = px.bar(y=top_actors.index, x=top_actors.values, orientation='h',
                   title="Top 10 Actors on Netflix", color=top_actors.values)
    st.plotly_chart(fig11)

    # Top 10 Countries with TV Shows
    tv_shows_by_country = df[(df['type'] == "TV Show") & (df['country'] != "Unknown")]['country'].value_counts().head(10)
    fig12 = px.bar(y=tv_shows_by_country.index, x=tv_shows_by_country.values, orientation='h',
                   title="Top 10 Countries with Most TV Shows", color=tv_shows_by_country.values)
    st.plotly_chart(fig12)

    # Top 10 Countries with Movies
    movies_by_country = df[(df['type'] == "Movie") & (df['country'] != "Unknown")]['country'].value_counts().head(10)
    fig13 = px.bar(y=movies_by_country.index, x=movies_by_country.values, orientation='h',
                   title="Top 10 Countries with Most Movies", color=movies_by_country.values)
    st.plotly_chart(fig13)

    # Longest TV Shows by Seasons
    tv_shows = df[df['type'] == "TV Show"]
    tv_shows['season_count'] = tv_shows['duration'].str.extract(r'(\d+)').astype(float)
    longest_tv_shows = tv_shows.nlargest(10, 'season_count')[['title', 'season_count']]
    fig14 = px.bar(longest_tv_shows, y='title', x='season_count', orientation='h',
                    title="Top 10 Longest TV Shows by Seasons", color='season_count')
    st.plotly_chart(fig14)

if __name__ == "__main__":
    main()
