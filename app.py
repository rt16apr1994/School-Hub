import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai

# --- Configuration ---
# Google Sheets Connection (Keep your secrets as they are)
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("School_Data").sheet1 

# AI Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- UI Layout & Custom CSS ---
st.set_page_config(page_title="The Sanskriti School | AI Portal", layout="wide")

# Custom CSS for School Branding (Navy Blue & Gold Theme)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #002147; color: white; border-radius: 5px; width: 100%; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .header-box {
        background-color: #002147;
        padding: 40px;
        border-radius: 10px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid #FFD700;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>THE SANSKRITI SCHOOL</h1>
        <p style='font-size: 1.2rem;'>Nurturing Excellence, Enriching Lives</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content: Two Columns ---
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    # Banner Image (Placeholder for School Building)
    st.image("https://images.unsplash.com/photo-1546410531-bb4caa6b424d?auto=format&fit=crop&w=1000", caption="Our State-of-the-art Campus")
    
    st.markdown("""
    <div class="card">
        <h3>About Our School</h3>
        <p>The Sanskriti School stands for holistic development. We combine traditional values with modern technology 
        to ensure our students are ready for the future challenges.</p>
        <ul>
            <li>Smart Classrooms</li>
            <li>International Sports Facilities</li>
            <li>Experienced Faculty</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # --- AI Chat Section ---
    st.markdown('<div class="card"><h3>🤖 Ask Our AI Assistant</h3></div>', unsafe_allow_html=True)
    user_query = st.chat_input("Admissions, Fees, ya Facilities ke baare mein puchein...")
    
    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Aap The Sanskriti School ke official assistant hain. Is sawal ka polite jawab dein: {user_query}")
                st.write(response.text)

with col2:
    # --- Admission Form ---
    st.markdown('<div class="card" style="border-top: 5px solid #002147;">', unsafe_allow_html=True)
    st.subheader("📩 Admission Inquiry 2026-27")
    
    with st.form("inquiry_form", clear_on_submit=True):
        name = st.text_input("Student Name*")
        parent_name = st.text_input("Parent's Name*")
        phone = st.text_input("Mobile Number*")
        grade = st.selectbox("Seeking Admission for", ["Nursery", "KG", "Class 1-5", "Class 6-10", "Class 11-12"])
        message = st.text_area("Specific Query (Optional)")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if name and phone:
                try:
                    sheet.append_row([name, parent_name, phone, grade, message])
                    st.success("Thank you! Your inquiry has been recorded in our Google Sheet.")
                    st.balloons()
                except Exception as e:
                    st.error("Error connecting to Google Sheets.")
            else:
                st.warning("Please fill the mandatory fields (*)")
    st.markdown('</div>', unsafe_allow_html=True)

    # School Stats or Quick Links
    st.markdown("""
    <div class="card">
        <h4>Quick Highlights</h4>
        <p>🏆 Ranked #1 in Academic Excellence</p>
        <p>🎓 100% Board Results</p>
        <p>🌍 Global Exchange Programs</p>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://via.placeholder.com/150x150.png?text=SCHOOL+LOGO", width=150)
st.sidebar.title("Navigation")
st.sidebar.info("📍 Location: Lucknow, India")
st.sidebar.button("Download Prospectus")
st.sidebar.button("School Gallery")
st.sidebar.write("---")
st.sidebar.write("📞 Contact: +91-XXXX-XXX-XXX")
