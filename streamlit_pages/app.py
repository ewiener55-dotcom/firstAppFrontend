import streamlit as st
import requests

API = "https://firstapp-errq.onrender.com/activities/"

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# ---------------- NAV BAR ----------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.page = "Home"
with col2:
    if st.button("Upload"):
        st.session_state.page = "Upload"
with col3:
    if st.button("Last Uploaded"):
        st.session_state.page = "Uploaded"

# ---------------- PAGE LOGIC ----------------
# Uploaded page
if st.session_state.page == "Uploaded":
    st.title("Last Uploaded Activity")
    item = st.session_state.last_uploaded
    if item:
        st.subheader(item["Title"])
        st.image(item['Image'], width=300)  # full URL already included
        st.write("Rating:", item["Rating"])
    else:
        st.info("No uploaded item found. Upload something first!")

    if st.button("Back to Upload"):
        st.session_state.page = "Upload"

    st.stop()  # stop further code so Upload/Home blocks don't run

# Upload page
elif st.session_state.page == "Upload":
    st.title("Upload and Rate New Activity")

    title = st.text_input("Title")
    image = st.file_uploader("Image", type=["png", "jpg", "jpeg"])
    rating = st.slider("Rating", 0, 10)

    # Submit button must be **inside this block**
    submitted = st.button("Submit")
    if submitted:
        if not title or not image:
            st.warning("Missing Fields")
        else:
            files = {"Image": image}
            data = {"Title": title, "Rating": rating}
            res = requests.post(API, data=data, files=files)

            if res.status_code in [200, 201]:
                st.success("Upload successful! 🎉")
                st.session_state.last_uploaded = res.json()
                st.session_state.page = "Uploaded"  # switch page
            else:
                st.error(f"Upload failed! Status code: {res.status_code}")

# Home page
elif st.session_state.page == "Home":
    st.title("SUPER FUN APP - All Activities")
    res = requests.get(API)
    if res.status_code == 200:
        for item in res.json():
            st.subheader(item["Title"])
            st.image(item['Image'], width=150)  # full URL already included
            st.write("Rating:", item["Rating"])
            st.divider()
    else:
        st.error("Could not connect to Django API")
