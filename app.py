# app.py
# Streamlit app for the GreenSpark application
# Converted from Flask server to Streamlit

import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------
# Firebase Initialization
# -------------------------------
if not firebase_admin._apps:
    # Use your own service account key here
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------------------------
# Constants
# -------------------------------
APP_ID = "default-app-id"
PUBLIC_COLLECTION_PATH = f"artifacts/{APP_ID}/public/data"
USERS_COLLECTION_PATH = f"artifacts/{APP_ID}/users"

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="GreenSpark Dashboard", layout="centered")
st.title("🌱 GreenSpark Dashboard")

# --- Member Count ---
st.subheader("👥 Member Count")

if st.button("Get Member Count"):
    try:
        doc_ref = db.collection(PUBLIC_COLLECTION_PATH).document("member_count").get()
        if doc_ref.exists:
            data = doc_ref.to_dict()
            st.success(f"Total Members: {data.get('total', 0)}")
        else:
            st.warning("No member count found.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.button("Increment Member Count"):
    try:
        doc_ref = db.collection(PUBLIC_COLLECTION_PATH).document("member_count")
        doc_ref.set({"total": firestore.Increment(1)}, merge=True)
        st.success("✅ Member count incremented!")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# --- User Profile ---
st.subheader("🙍 User Profile")

user_id = st.text_input("Enter User ID")

if st.button("Get User Profile"):
    try:
        doc_ref = db.collection(f"{USERS_COLLECTION_PATH}/{user_id}/profile").document("details").get()
        if doc_ref.exists:
            st.json(doc_ref.to_dict())
        else:
            st.warning("Profile not found.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.write("Update Profile:")
name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Update Profile"):
    try:
        doc_ref = db.collection(f"{USERS_COLLECTION_PATH}/{user_id}/profile").document("details")
        doc_ref.set({"name": name, "email": email}, merge=True)
        st.success("✅ Profile updated successfully!")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# --- Translations ---
st.subheader("🌍 Translations")

language_code = st.selectbox("Select Language", ["en", "hi"])
translations = {
    "en": {"home": "Home", "about": "About", "login": "Login"},
    "hi": {"home": "होम", "about": "हमारे बारे में", "login": "लॉग इन"}
}

if st.button("Get Translations"):
    st.json(translations.get(language_code, translations["en"]))
