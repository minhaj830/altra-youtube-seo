# main.py
import streamlit as st
import requests
import pandas as pd

# YouTube API Settings
API_KEY = "AIzaSyCNcCb6GC7rBndDNva4prst6sYf2jZ_co4"  # Replace with your API key
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
SUGGESTIONS_URL = "https://suggestqueries-clientsd.youtube.com/complete/search"

# Streamlit App
st.title("YouTube Low Competition Keyword Finder 🔍")
keyword = st.text_input("Enter a seed keyword (e.g., 'tech reviews'):")

if keyword:
    # Fetch Related Keywords (Simulated via YouTube Search Suggestions)
    suggestions = requests.get(f"{SUGGESTIONS_URL}?client=youtube&ds=yt&q={keyword}").json()
    related_keywords = [suggestion[0] for suggestion in suggestions[1]]  # Extract suggestions

    # Analyze Keywords
    data = []
    for kw in related_keywords:
        # Fetch Competition (Total Search Results)
        params = {
            "part": "snippet",
            "q": kw,
            "type": "video",
            "key": API_KEY,
            "maxResults": 1  # Just to get totalResults
        }
        response = requests.get(SEARCH_URL, params=params).json()
        total_results = response.get("pageInfo", {}).get("totalResults", 0)
        
        # Calculate Metrics
        keyword_length = len(kw.split())
        data.append({
            "Keyword": kw,
            "Competition": total_results,
            "Length": keyword_length
        })

    # Sort by Low Competition & Long Keywords
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Competition", "Length"], ascending=[True, False])
    
    # Display Results
    st.subheader("Top Low-Competition Keywords:")
    st.dataframe(df)

    # Optional: Export to CSV
    st.download_button("Download CSV", df.to_csv(), file_name="keywords.csv")
