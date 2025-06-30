import os, requests 
import streamlit as st

# Use the name of the container as the default URL.
# BASE_URL = os.getenv("BACK_END_URL", "http://fastapi-backend:8000")
BASE_URL = os.getenv("BACK_END_URL", "http://localhost:8000")

st.title("🎥 Movie Review Sentiment Explorer")

tab1, tab2, tab3 = st.tabs(["Movies", "Reviews", "View All"])

# ---------------------- Tab 1: Movie Management ----------------------
with tab1:
    st.subheader("🎥 Movie Management")
    
    # 1. Execute create_movie.
    with st.form("create_movie_form"):
        st.subheader("🎬 Add a New Movie")
        title = st.text_input("Movie Title")
        director = st.text_input("Director")
        genre = st.text_input("Genre")
        release_year = st.number_input("Release Year", min_value = 1886, max_value = 2026)
        image_url = st.text_input("Image URL")
        submitted = st.form_submit_button("Add Movie")
        if submitted:
            response = requests.post(
                f"{BASE_URL}/movies/create_movie",
                json = {
                    "title": title,
                    "director": director,
                    "genre": genre,
                    "release_year": release_year,
                    "image_url": image_url
                }
            )
            if response.status_code == 200:
                st.success("✅ Movie created successfully!")
            else:
                st.error(f"❌ {response.status_code} — {response.json().get('detail')}.")
    
    st.markdown("---")

    # 2. Execute update_movie.
    with st.form("update_movie_form"):
        st.subheader("✏️ Update an Existing Movie")
        movie_id = st.number_input("Movie ID to Update", step = 1)
        new_title = st.text_input("New Title (Optional)")
        new_director = st.text_input("New Director (Optional)")
        new_genre = st.text_input("New Genre (Optional)")
        new_year = st.number_input("New Release Year (Optional)", min_value = 1886, max_value = 2026)
        new_image_url = st.text_input("New Image URL (Optional)")
        submitted = st.form_submit_button("Update Movie")
        if submitted:
            payload = {k: v for k, v in {
                "title": new_title,
                "director": new_director,
                "genre": new_genre,
                "release_year": new_year,
                "image_url": new_image_url
            }.items() if v}
            response = requests.put(f"{BASE_URL}/movies/update_movie/{movie_id}", json = payload)
            if response.status_code == 200:
                st.success("✅ Movie updated successfully!")
            else:
                st.error(f"❌ {response.status_code} — {response.json().get('detail')}.")

    st.markdown("---")

    # 3. Execute delete_movie.
    with st.form("delete_movie_form"):
        st.subheader("🗑️ Delete a Movie")
        title_to_delete = st.text_input("Title of Movie to Delete")
        submitted = st.form_submit_button("Delete Movie")
        if submitted:
            response = requests.delete(f"{BASE_URL}/movies/delete_movie/{title_to_delete}")
            if response.status_code == 200:
                st.success(response.json()["Message"])
            else:
                st.error(f"❌ {response.status_code} — {response.json().get('detail')}.")


# ---------------------- Tab 2: Review Management ----------------------
with tab2:
    st.subheader("💬 Review Management")
    
    # 4. Execute create_review. 
    with st.form("create_review_form"):
        st.subheader("💬 Add a Review to a Movie")
        movie_title_review = st.text_input("Movie Title (for the review)")
        movie_id = st.text_area("Movie Identifier")
        content = st.text_area("Review Content")
        rating = st.slider("Rating", 0.0, 10.0, step = 0.1)
        submitted = st.form_submit_button("Submit Review")
        if submitted:
            response = requests.post(
                f"{BASE_URL}/movies/create_review/{movie_title_review}",
                json = {"movie_id": movie_id, "content": content, "rating": rating}
            )
            if response.status_code == 200:
                st.success("✅ Review created successfully!")
            else:
                st.error(f"❌ {response.status_code} - {response.json().get('detail')}.")

    st.markdown("---")

    # 5. Execute update_review.
    with st.form("update_review_form"):
        st.subheader("🔄 Update a Review")
        title = st.text_input("Movie Title (for the review)")
        review_id = st.number_input("Review Identifier", step=1)
        new_content = st.text_area("Updated Content (optional)")
        new_rating = st.slider("Updated Rating", 0.0, 10.0, step = 0.1)
        submitted = st.form_submit_button("Update Review")
        if submitted:
            payload = {k: v for k, v in {"content": new_content, "rating": new_rating}.items() if v}
            response = requests.put(
                f"{BASE_URL}/movies/update_review/{title}/{review_id}",
                json = payload
            )
            if response.status_code == 200:
                st.success("✅ Review updated!")
            else:
                st.error(f"❌ {response.status_code} - {response.json().get('detail')}.")

    st.markdown("---")

    # 6. Execute delete_review.
    with st.form("delete_review_form"):
        st.subheader("🧹 Delete a Review")
        title = st.text_input("Movie Title")
        review_id = st.number_input("Review ID to delete", step = 1)
        submitted = st.form_submit_button("Delete Review")
        if submitted:
            response = requests.delete(f"{BASE_URL}/movies/delete_review/{title}/{int(review_id)}")
            if response.status_code == 200:
                st.success("✅ Review deleted and movie aggregates updated.")
            else:
                st.error(f"❌ {response.status_code} - {response.json().get('detail')}.")


# ---------------------- Tab 3: View Movies ----------------------
with tab3:
    st.subheader("📋 View Movies")
    # 7. Execute get_movies.
    show_all = st.checkbox("📜 Show All Movies (Ignore Filters)")

    # Filter inputs.
    with st.form(key = "movie_filter_form"):
        st.markdown("**Filter Movies**")
        movie_title = st.text_input("🎬 Title")
        movie_director = st.text_input("🎬 Director")
        movie_genre = st.text_input("📚 Genre")
        movie_release_year = st.text_input("📅 Release Year")
        min_rating = st.slider("⭐ Minimum Rating", 0.0, 10.0, 0.0, 0.5)
        sentiment = st.selectbox("💬 Sentiment", ["", "positive", "neutral", "negative"])

        submitted = st.form_submit_button("Search")

    # Create dictionary of parameters.
    if submitted or show_all:
        if show_all:
            response = requests.get(f"{BASE_URL}/movies")
        else:
            params = {}
            if movie_title: params["title"] = movie_title
            if movie_director: params["director"] = movie_director
            if movie_genre: params["genre"] = movie_genre
            if movie_release_year: params["release_year"] = movie_release_year
            if min_rating > 0: params["min_rating"] = min_rating
            if sentiment: params["sentiment"] = sentiment

            response = requests.get(f"{BASE_URL}/movies", params = params)
    
        # Display the results.
        if response.status_code == 200:
            for movie in response.json():
                with st.expander(f"{movie['title']} ({movie['release_year']})"):
                    st.image(movie.get("image_url", ""), width = 300)
                    st.markdown(f"**🆔 Movie Identifier:** {movie["id"]}")
                    st.markdown(f"**🎬 Director:** {movie['director']}")
                    st.markdown(f"**📅 Year:** {movie['release_year']}")
                    st.markdown(f"**🎭 Genre:** {movie['genre']}")
                    average_rating = movie.get("average_rating")
                    st.markdown(f"**⭐ Average Rating:** {average_rating:.2f}" if average_rating is not None else "**⭐ Average Rating:** N/A")
                    st.markdown(f"**💬 Sentiment:** {movie.get('overall_sentiment', 'N/A')}")
                    st.markdown("---")
                    if movie.get("reviews"):
                        for r in movie["reviews"]:
                            st.markdown(f"⭐ {r['rating']} — *{r['sentiment']}* — (Review Identifier {r['id']})\n> {r['content']}")
                    else:
                        st.info("No reviews for this movie yet.")
        else:
            st.error(f"❌ {response.status_code} — {response.json().get('detail')}.")
