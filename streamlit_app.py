import streamlit as st

params = st.query_params
if "guest" in params:
    if params["guest"] == "guest-access-code-for-anonymous-uploads":
        st.session_state.authenticated = True
        st.session_state.username = "guest"

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None


def check_credentials(username, password):
    # Simple credential check (replace with your own logic or database)
    valid_credentials = {
        "a-good-username": "an-even-better-password"
    }
    return valid_credentials.get(username) == password


def login_page():
    st.title("Login")
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()  # Refresh to show main app
            else:
                st.error("Invalid username or password")


def main_app():
    photo_page = st.Page("photo.py", title="Photo Page", icon=":material/camera:")
    slideshow_page = st.Page("slideshow.py", title="Slideshow Page", icon=":material/camera:")
    manage_page = st.Page("manage.py", title="Manage Uploads", icon=":material/camera:")
    restore_page = st.Page("restore.py", title="Restore Uploads", icon=":material/camera:")
    pg = st.navigation(pages=[photo_page, slideshow_page, manage_page, restore_page])
    if st.session_state.username == "guest":
        pg = st.navigation(pages=[photo_page])
    pg.run()


# Main logic
if not st.session_state.authenticated:
    login_page()
else:
    main_app()
