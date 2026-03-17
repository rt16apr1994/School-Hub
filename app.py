import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai

# --- Configuration ---
# Google Sheets Connection
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# 'creds.json' aapki service account file hai
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("School_Data").sheet1 # Apni sheet ka naam likhein

# AI Setup (Gemini API)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- UI Layout ---
st.set_page_config(page_title="The Sanskriti School AI Portal")

st.title("Welcome to The Sanskriti School")
st.write("Quality Education for a Better Future")

# --- AI Inquiry Section ---
st.subheader("🤖 AI Admission Assistant")
user_query = st.text_input("School ke baare mein kuch bhi puchein:")
if user_query:
    response = model.generate_content(f"Aap ek school assistant hain. Is sawal ka jawab dein: {user_query}")
    st.write(response.text)

# --- Admission/Inquiry Form ---
st.divider()
st.subheader("📩 Inquiry Form")

with st.form("inquiry_form", clear_on_submit=True):
    name = st.text_input("Student Name")
    parent_name = st.text_input("Parent's Name")
    phone = st.text_input("Phone Number")
    grade = st.selectbox("Admission for Grade", ["Nursery", "KG", "1st", "2nd", "3rd"])
    message = st.text_area("Anything else you want to ask?")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if name and phone:
            # Data ko Google Sheet mein append karna
            sheet.append_row([name, parent_name, phone, grade, message])
            st.success("Aapki inquiry save ho gayi hai! Hum jald hi sampark karenge.")
        else:
            st.error("Kripya zaruri fields bharein.")

# --- School Info (Reference style) ---
st.sidebar.title("School Navigation")
st.sidebar.write("• About Us")
st.sidebar.write("• Academics")
st.sidebar.write("• Facilities")
st.sidebar.write("• Contact Us")
