import streamlit as st

countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros", "Ivory Coast", "Djibouti", "Democratic Republic of the Congo", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Republic of the Congo", "Rwanda", "Sao Tome & Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

if"logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.button("Log in"):
    st.session_state.logged_in = True
    st.write("Logged in!")

if st.session_state.logged_in:
    st.write("Welcome!")

st.set_page_config(
    page_title = "MDI App",
    layout="wide",
    page_icon="smile.jpg"
)

st.title("Multi-Domain Intelligence Platform")
st.header("CST1510")
st.subheader("MDX DKP")

col1, col2 = st.columns(2)

with col1:
    st.write("This is my page content!")
    st.write("Another one!")

with col2:
    st.markdown("**Bold** and *italic*")
    st.caption("Test test")
    st.text("Test successful.")

with st.sidebar:
    st.header("Login menu")
    name = st.text_input("Username: ")
    password = st.text_input("Enter a password", type="password")

    if st.button("Login"):
        if name == "Shreyash" and password == "cheese123":
            st.success(f"{name} has successfully logged in.")
        else:
            st.warning("Incorrect username or password.")



age = st.number_input(
"Age", min_value=0,
 max_value=120, value=25
 )

val = st.slider(
"Pick value",
0, 100, 50
 )

country = st.selectbox(
"Favourite country",
 countries
 )

fruits = st.multiselect(
"Choose fruits",
 ["Apple", "Banana","Strawberry", "Guava", "Plum", "Watermelon", "Apricot", "Fig", "Orange", "Dragonfruit", "Cantaloupe"]
 )

agree = st.checkbox("I agree")

if agree:
    st.write("Good.")

date = st.date_input("Date")

with st.expander("About the app"):
    st.write("This app is a test app.")
