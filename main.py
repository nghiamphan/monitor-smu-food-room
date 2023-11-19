import streamlit as st
import schedule
import time
import utils as u


def input():
    st.write(st.secrets["URL"])
    st.session_state["is_monitored"] = st.toggle("Monitor registration")
    st.session_state["time_interval"] = st.number_input(
        "Set time interval between each check", value=5, min_value=1, format="%i"
    )
    st.session_state["receiver_email"] = st.text_input(
        "Email to send notification:", placeholder="Leave empty to use default email"
    )
    st.button("Manual Check registration", on_click=check_registration)


def check_registration():
    if not u.is_registration_open():
        u.send_email(st.session_state["receiver_email"])


if __name__ == "__main__":
    input()

    schedule.clear()
    if st.session_state["is_monitored"]:
        schedule.every(st.session_state["time_interval"]).minutes.do(check_registration)

    st.write("Pending Checks")
    st.write(schedule.get_jobs())

    while st.session_state["is_monitored"]:
        schedule.run_pending()
        time.sleep(1)
