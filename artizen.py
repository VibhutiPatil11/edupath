import streamlit as st
import sqlite3
import os
from PIL import Image
from werkzeug.utils import secure_filename

# --------------- SETUP ------------------
st.set_page_config(page_title="ArtiZen", layout="wide")

# Initialize session state variables
if "user" not in st.session_state:
    st.session_state.user = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
if "shipping_method" not in st.session_state:
    st.session_state.shipping_method = "Direct from Artisan"

# --------------- DATABASE ------------------
conn = sqlite3.connect("artizen.db", check_same_thread=False)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS artisans (
    username TEXT PRIMARY KEY,
    password TEXT,
    secret TEXT,
    name TEXT,
    age INTEGER,
    brand TEXT,
    category TEXT,
    business TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artisan_username TEXT,
    product_name TEXT,
    price REAL,
    category TEXT,
    image_path TEXT
)''')

conn.commit()

# --------------- FUNCTIONS ------------------
def register_artisan(data):
    cur.execute("INSERT INTO artisans VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()

def check_login(username, password):
    cur.execute("SELECT * FROM artisans WHERE username=? AND password=?", (username, password))
    return cur.fetchone()

def get_profile(username):
    cur.execute("SELECT * FROM artisans WHERE username=?", (username,))
    return cur.fetchone()

def get_all_products():
    cur.execute("SELECT * FROM products")
    return cur.fetchall()

def get_user_products(username):
    cur.execute("SELECT * FROM products WHERE artisan_username=?", (username,))
    return cur.fetchall()

def upload_product(data):
    cur.execute("INSERT INTO products (artisan_username, product_name, price, category, image_path) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()

# --------------- UI ------------------
st.sidebar.title("\U0001F3A8 ArtiZen Navigation")
menu = st.sidebar.selectbox("Go to", ["Home", "Register", "Login", "Pitch & Funding", "Collaboration"])

if menu == "Home":
    st.title("\U0001F9F5 ArtiZen: Where Tradition Meets Technology")
    st.image("https://i.imgur.com/BuhjzHZ.png", width=500)
    st.write("Empowering local artisans with global access, fair trade, and AI-driven discovery.")

elif menu == "Register":
    st.header("\U0001F4DD Artisan Registration")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        secret = st.text_input("Your Secret Word")
        name = st.text_input("Full Name")
        age = st.number_input("Age", 15, 90)
        brand = st.text_input("Brand Name")
        category = st.selectbox("Category", ["Weaving", "Pottery", "Jewellery", "Paintings", "Sculptures", "Textiles"])
        business = st.radio("Business Type", ["Small Startup", "Established Brand"])
        submit = st.form_submit_button("Register")

    if submit:
        try:
            register_artisan((username, password, secret, name, age, brand, category, business))
            st.success("Registered Successfully! Please login.")
        except:
            st.error("Username already exists.")

elif menu == "Login":
    st.header("\U0001F510 Login")
    uname = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_login(uname, passwd)
        if user:
            st.success(f"Welcome {user[3]}!")
            st.session_state.user = uname
        else:
            st.error("Invalid username or password")

    if st.button("Forgot Password?"):
        sec_uname = st.text_input("Your Username")
        sec_ans = st.text_input("Your Secret Word")
        cur.execute("SELECT password FROM artisans WHERE username=? AND secret=?", (sec_uname, sec_ans))
        result = cur.fetchone()
        if result:
            st.info(f"Your password is: {result[0]}")
        else:
            st.warning("Incorrect details")

# --------------- DASHBOARD ------------------
if st.session_state.user:
    st.sidebar.subheader(f"Hello, {st.session_state.user}")
    tab = st.sidebar.radio("My Dashboard", [
        "Marketplace", "Upload Product", "My Profile", "Wishlist", "Cart", "Logout"])

    if tab == "Upload Product":
        st.header("\U0001F4E4 Upload Your Product")
        with st.form("upload"):
            pname = st.text_input("Product Name")
            price = st.number_input("Price", 1.0)
            pcat = st.selectbox("Product Category", ["Weaving", "Pottery", "Jewellery", "Paintings", "Sculptures", "Textiles"])
            pimage = st.file_uploader("Upload Image", type=['jpg', 'png'])
            submit_product = st.form_submit_button("Upload")

        if submit_product and pimage:
            img_path = os.path.join("static", secure_filename(pimage.name))
            with open(img_path, "wb") as f:
                f.write(pimage.getbuffer())
            upload_product((st.session_state.user, pname, price, pcat, img_path))
            st.success("Product uploaded successfully!")

    elif tab == "Marketplace":
        st.header("\U0001F6D2 Explore Marketplace")
        products = get_all_products()
        for p in products:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(p[5], width=150)
            with col2:
                st.markdown(f"**{p[2]}** - ₹{p[3]}")
                st.write(f"Category: {p[4]}")
                st.write(f"By: {p[1]}")
                if st.button(f"❤️ Wishlist {p[0]}", key=f"wish{p[0]}"):
                    st.session_state.wishlist.append(p)
                    st.success("Added to wishlist")
                if st.button(f"🛒 Add to Cart {p[0]}", key=f"cart{p[0]}"):
                    st.session_state.cart.append(p)
                    st.success("Added to cart")

    elif tab == "My Profile":
        st.header("\U0001F464 My Artisan Profile")
        user = get_profile(st.session_state.user)
        st.markdown(f"""
        **Name:** {user[3]}  
        **Brand:** {user[5]}  
        **Category:** {user[6]}  
        **Business Type:** {user[7]}  
        """)
        st.subheader("My Products:")
        for p in get_user_products(st.session_state.user):
            st.image(p[5], width=120)
            st.write(f"{p[2]} - ₹{p[3]}")

    elif tab == "Wishlist":
        st.header("❤️ My Wishlist")
        for p in st.session_state.wishlist:
            st.image(p[5], width=120)
            st.write(f"**{p[2]}** - ₹{p[3]}")
            if st.button(f"Remove {p[0]}", key=f"remove_wish{p[0]}"):
                st.session_state.wishlist = [x for x in st.session_state.wishlist if x[0] != p[0]]

    elif tab == "Cart":
        st.header("🛒 My Cart")
        total = 0
        for p in st.session_state.cart:
            st.image(p[5], width=100)
            st.write(f"{p[2]} - ₹{p[3]}")
            total += p[3]
            if st.button(f"Remove {p[0]}", key=f"remove_cart{p[0]}"):
                st.session_state.cart = [x for x in st.session_state.cart if x[0] != p[0]]
        st.markdown(f"### Total: ₹{total}")
        if total > 0:
            st.radio("Choose Shipping Method:", ["Direct from Artisan", "Via ArtiZen"], key="shipping_method")
            if st.button("Proceed to Payment"):
                st.success(f"Payment simulated! Total: ₹{total}, Shipping: {st.session_state.shipping_method}")
                st.session_state.cart = []

    elif tab == "Logout":
        st.session_state.user = None
        st.success("Logged out successfully!")

# --------------- PITCH & COLLAB ------------------
elif menu == "Pitch & Funding":
    st.header("\U0001F3A4 Pitch Your Product or Brand")
    st.text_input("Your Brand / Startup Name")
    st.text_area("Describe your idea or funding request")
    st.file_uploader("Attach Brochure or Proposal (PDF)")
    st.button("Submit Pitch")

elif menu == "Collaboration":
    st.header("\U0001F91D Collaborate with Other Brands")
    st.text_input("Your Brand Name")
    st.text_input("What type of collab are you looking for?")
    st.text_area("Share your idea")
    st.button("Send Collaboration Request")
