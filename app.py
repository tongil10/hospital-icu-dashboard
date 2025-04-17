import streamlit as st
import pandas as pd
import random
import datetime

# --- Simulated users database ---
users_df = pd.read_csv("users.csv")

# --- Authenticate user ---
def authenticate(email, password, df):
    email = email.strip()
    password = password.strip()
    return any(
        email == row['email'] and password == row['password']
        for index, row in df.iterrows()
    )

# --- Simulate patient data ---
def generate_patient_data():
    patients = []
    names = ['Juan Perez', 'Ana González', 'Carlos Méndez', 'Lucía Torres']
    for i in range(4):
        patient = {
            "Bed": i + 1,
            "Name": names[i],
            "Heart Rate": random.randint(60, 100),
            "Blood Pressure": f"{random.randint(100, 130)}/{random.randint(60, 90)}",
            "O2 Sat (%)": random.randint(90, 100),
            "Temp (°C)": round(random.uniform(36.5, 39.5), 1),
            "Status": random.choice(["Stable", "Under Observation", "Critical"]),
            "Last Updated": datetime.datetime.now().strftime("%H:%M:%S")
        }
        patients.append(patient)
    return pd.DataFrame(patients)

# --- Main Dashboard after login ---
def show_dashboard(email):
    st.title("🧠 Virtual ICU & Bed Management")
    st.success(f"Welcome, {email}")

    # --- Live Patient Monitor ---
    st.subheader("🔍 ICU Patient Vitals (Live Data Simulation)")
    data = generate_patient_data()
    st.dataframe(data, use_container_width=True)

    # --- Alerts ---
    st.subheader("🚨 Alerts")
    for index, row in data.iterrows():
        if row["Temp (°C)"] > 38.5:
            st.error(f"High fever detected in {row['Name']} (Bed {row['Bed']}) — {row['Temp (°C)']} °C")
        if row["O2 Sat (%)"] < 92:
            st.warning(f"Low oxygen level in {row['Name']} (Bed {row['Bed']}) — {row['O2 Sat (%)']}%")

    # --- Assign Staff to Beds ---
    st.subheader("👨‍⚕️ Assign Staff to Beds")
    bed_no = st.selectbox("Choose Bed", data["Bed"])
    staff_name = st.text_input("Enter staff name")
    if st.button("Assign"):
        st.success(f"{staff_name} has been assigned to Bed {bed_no}")

    # --- Download Report (Optional) ---
    st.subheader("📤 Download ICU Report")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "icu_report.csv", "text/csv")

# --- Main App ---
def main():
    st.set_page_config(page_title="Hospital ICU Dashboard", layout="wide")
    st.title("🔐 Hospital Secure Login")

    email = st.text_input("Email (hospital.org only)")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email.endswith("@hospital.org"):
            st.error("Only hospital email addresses are allowed.")
        elif authenticate(email, password, users_df):
            show_dashboard(email)
        else:
            st.error("Invalid credentials. Try again.")

if __name__ == "__main__":
    main()
