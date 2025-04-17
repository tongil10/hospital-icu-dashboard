import streamlit as st
import pandas as pd

# CONFIG
HOSPITAL_DOMAIN = "@hospitalmex.org"

# Load users from CSV
def load_users():
    try:
        return pd.read_csv("users.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["email", "password"])

# Login check
def authenticate(email, password, users_df):
    if any((email.strip() == row['email'] and password.strip() == row['password']) for index, row in df.iterrows()):
        return False
    user = users_df[(users_df['email'] == email) & (users_df['password'] == password)]
    return not user.empty

# Main App
def main():
    st.set_page_config(page_title="Hospital Secure Login", layout="centered")
    st.title("🔐 Hospital Staff Login")

    st.write("Please login using your **hospital email**.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users_df = load_users()
        if authenticate(email, password, users_df):
            st.success("✅ Login successful!")
            show_dashboard(email)
        else:
            st.error("❌ Invalid credentials or unauthorized email domain.")

def show_dashboard(user_email):
    st.subheader(f"👨‍⚕️ Welcome, {user_email}")
    st.write("This is your virtual ICU monitoring dashboard.")
    # Here you can show vitals, graphs, alerts, etc.
    st.info("📊 Sample ICU data will appear here soon!")

if __name__ == "__main__":
    main()
