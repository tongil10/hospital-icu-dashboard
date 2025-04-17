import streamlit as st
import pandas as pd
import random
import datetime

# --- Load users.csv ---
users_df = pd.read_csv("users.csv")

# --- Authentication function ---
def authenticate(email, password, df):
    email = email.strip()
    password = password.strip()
    return any(email == row['email'] and password == row['password'] for _, row in df.iterrows())

# --- Simulate patient data ---
def generate_patient_data():
    names = ['Juan Perez', 'Ana González', 'Carlos Méndez', 'Lucía Torres']
    data = []
    for i in range(4):
        data.append({
            "Bed": i + 1,
            "Name": names[i],
            "Heart Rate": random.randint(60, 100),
            "Blood Pressure": f"{random.randint(100, 130)}/{random.randint(60, 90)}",
            "O2 Sat (%)": random.randint(90, 100),
            "Temp (°C)": round(random.uniform(36.5, 39.5), 1),
            "Status": random.choice(["Stable", "Under Observation", "Critical"]),
            "Last Updated": datetime.datetime.now().strftime("%H:%M:%S")
        })
    return pd.DataFrame(data)

# --- Dashboard ---
import plotly.graph_objects as go
import time

def show_dashboard():
    st.title("🧠 Virtual ICU & Bed Management")
    st.success(f"Welcome, {st.session_state.user_email}")

    # Simulated live data
    st.subheader("📊 Live Vitals Overview (Animated)")

    placeholder = st.empty()
    heart_data = []
    temp_data = []
    o2_data = []
    timestamps = []

    for i in range(30):  # simulate 30 time points (can change to while True for infinite)
        # Simulate one patient
        hr = random.randint(60, 100)
        temp = round(random.uniform(36.5, 39.0), 1)
        o2 = random.randint(90, 100)
        now = datetime.datetime.now().strftime("%H:%M:%S")

        heart_data.append(hr)
        temp_data.append(temp)
        o2_data.append(o2)
        timestamps.append(now)

        with placeholder.container():
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Heart Rate (bpm)", f"{hr}")
                st.metric("Oxygen (%)", f"{o2}")
                st.metric("Temperature (°C)", f"{temp}")
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=timestamps, y=heart_data, mode='lines+markers', name='Heart Rate'))
                fig.add_trace(go.Scatter(x=timestamps, y=temp_data, mode='lines+markers', name='Temp (°C)'))
                fig.add_trace(go.Scatter(x=timestamps, y=o2_data, mode='lines+markers', name='O2 Sat (%)'))
                fig.update_layout(
                    title="Live Vitals",
                    xaxis_title="Time",
                    yaxis_title="Value",
                    xaxis=dict(showgrid=False),
                    yaxis=dict(range=[50, 110]),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

        time.sleep(0.5)  # Simulate new data every 0.5 sec

    st.subheader("🚨 Alerts")
    for _, row in df.iterrows():
        if row["Temp (°C)"] > 38.5:
            st.error(f"{row['Name']} (Bed {row['Bed']}): High Fever — {row['Temp (°C)']} °C")
        if row["O2 Sat (%)"] < 92:
            st.warning(f"{row['Name']} (Bed {row['Bed']}): Low O2 Saturation — {row['O2 Sat (%)']}%")

    st.subheader("👨‍⚕️ Assign Staff to Bed")
    bed = st.selectbox("Choose Bed", df["Bed"])
    staff = st.text_input("Staff Name")
    if st.button("Assign"):
        st.success(f"{staff} assigned to Bed {bed}")

    st.subheader("📤 Download Report")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "icu_report.csv", "text/csv")

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.experimental_rerun()

# --- MAIN ---
def main():
    st.set_page_config(page_title="Hospital ICU Dashboard", layout="wide")

    # Session state setup
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

    # Show login if not logged in
    if not st.session_state.logged_in:
        st.title("🔐 Hospital Secure Login")

        email = st.text_input("Email (hospital.org only)")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not email.endswith("@hospital.org"):
                st.error("Email must end with @hospital.org")
            elif authenticate(email, password, users_df):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
    else:
        show_dashboard()

if __name__ == "__main__":
    main()


