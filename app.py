import streamlit as st
import pandas as pd
import random
import datetime

# --- Load users ---
users_df = pd.read_csv("users.csv")

# --- Authenticate function ---
def authenticate(email, password, df):
    email = email.strip()
    password = password.strip()
    return any(
        email == row['email'] and password == row['password']
        for _, row in df.iterrows()
    )

# --- Generate simulated vitals ---
def generate_patient_data():
    names = ['Juan Perez', 'Ana González', 'Carlos Méndez', 'Lucía Torres']
    patients = []
    for i in range(4):
        patients.append({
            "Bed": i + 1,
            "Name": names[i],
            "Heart Rate": random.randint(60, 100),
            "Blood Pressure": f"{random.randint(100, 130)}/{random.randint(60, 90)}",
            "O2 Sat (%)": random.randint(90, 100),
            "Temp (°C)": round(random.uniform(36.5, 39.5), 1),
            "Status": random.choice(["Stable", "Under Observation", "Critical"]),
            "Last Updated": datetime.datetime.now().strftime("%H:%M:%S")
        })
    return pd.DataFrame(patients)

# --- Dashboard after login ---
def show_dashboard(email):
    st.title("🧠 Virtual ICU & Bed Management")
    st.success(f"Welcome, {email}")

    st.subheader("🔍 ICU Patient Vitals (Live Data Simulation)")
    data = generate_patient_data()
    st.dataframe(data, use_container_width=True)

    st.subheader("🚨 Alerts")
    for _, row in data.iterrows():
        if row["Temp (°C)"] > 38.5:
            st.error(f"High fever in {row['Name']} (Bed {row['Bed']}) — {row['Temp (°C)']} °C")
        if row["O2 Sat (%)"] < 92:
            st.warning(f"Low oxygen in {row['Name']} (Bed {row['Bed']}) — {row['O2 Sat (%)']}%")

    st.subheader("👨‍⚕️ Assign Staff to Beds")
    bed = st.selectbox("Choose Bed", data["Bed"])
    staff = st.text_input("Enter staff name")
    if st.button("Assign"):
        st.success(f"{staff} assigned to Bed {bed}")

    st.subheader("📤 Download ICU Report")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "icu_report.csv", "text/csv")

    if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.experimental_rerun()

# --- Main App Logic ---
def main():
    st.set_page_config(page_title="Hospital ICU Dashboard", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.email = ""

    if not st.session_state.logged_in:
        st.title("🔐 Hospital Secure Login")

        email = st.text_input("Email (hospital.org only)")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not email.endswith("@hospital.org"):
                st.error("Only hospital email addresses are allowed.")
            elif authenticate(email, password, users_df):
                st.session_state.logged_in = True
                st.session_state.email = email
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
    else:
        show_dashboard(st.session_state.email)

if __name__ == "__main__":
    main()

