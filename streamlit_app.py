import streamlit as st


ITEMS = [
    {"name": "Apples", "emoji": "🍎", "price": 500},
    {"name": "Bananas", "emoji": "🍌", "price": 700},
    {"name": "Bread", "emoji": "🍞", "price": 1_000},
    {"name": "Milk", "emoji": "🥛", "price": 1_200},
    {"name": "Eggs", "emoji": "🥚", "price": 1_500},
    {"name": "Juice", "emoji": "🧃", "price": 800},
]

st.set_page_config(page_title="Let's Shop! | English Practice", page_icon="🛍️")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #111827 0%, #172554 55%, #12312d 100%);
        color-scheme: dark;
    }
    .stApp, .stApp * {
        color: #f8fafc;
    }
    .stApp [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #243247;
        border-color: #52647d;
        border-radius: 1rem;
    }
    .stApp [data-testid="stVerticalBlockBorderWrapper"],
    .stApp [data-testid="stVerticalBlockBorderWrapper"] * {
        color: #f8fafc;
    }
    .stApp div.stButton > button,
    .stApp div.stButton > button * {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        color: #172033;
        font-weight: 600;
    }
    .stApp div.stButton > button:hover,
    .stApp div.stButton > button:hover * {
        background-color: #dbeafe;
        border-color: #93c5fd;
        color: #172033;
    }
    .main .block-container {
        max-width: 920px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }
    .eyebrow {
        color: #57677f;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "role" not in st.session_state:
    st.session_state.role = None
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.markdown('<p class="eyebrow">English shopping practice</p>', unsafe_allow_html=True)
st.title("🛍️ Let's Shop!")
st.write("Practice English conversations for buying and selling items.")

if st.session_state.role is None:
    st.subheader("Which role would you like to practice?")
    buyer, seller = st.columns(2)
    with buyer:
        with st.container(border=True):
            st.subheader("🧑‍💼 Buyer")
            st.write("Check your budget and choose the items you want to buy.")
            if st.button("Choose Buyer", use_container_width=True):
                st.session_state.role = "buyer"
                st.session_state.cart = {}
                st.rerun()
    with seller:
        with st.container(border=True):
            st.subheader("🧑‍🍳 Seller")
            st.write("Choose items and build a shopping list while staying within your budget.")
            if st.button("Choose Seller", use_container_width=True):
                st.session_state.role = "seller"
                st.session_state.cart = {}
                st.rerun()
else:
    role = st.session_state.role
    heading = "Buyer" if role == "buyer" else "Seller"

    if st.button("← Back to role selection"):
        st.session_state.role = None
        st.session_state.cart = {}
        st.rerun()

    st.subheader(f"{'🧑‍💼' if role == 'buyer' else '🧑‍🍳'} {heading} View")
    if role == "buyer":
        st.info("💰 Available budget: **₩2,000**")
        st.caption("Item prices are hidden.")
    else:
        st.caption("Review the available items and their prices.")

    st.markdown("### Choose Items")
    columns = st.columns(3)
    for index, item in enumerate(ITEMS):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']} {item['name']}")
                if role == "seller":
                    st.write(f"₩{item['price']:,}")
                else:
                    st.write("&nbsp;", unsafe_allow_html=True)
                if st.button(
                    "Add to Shopping List",
                    key=f"add_{role}_{item['name']}",
                    use_container_width=True,
                ):
                    cart = st.session_state.cart
                    cart[item["name"]] = cart.get(item["name"], 0) + 1
                    st.rerun()

    st.markdown("### 🧺 Shopping List")
    cart = st.session_state.cart
    if not cart:
        st.write("Your list is empty. Choose some items above to get started.")
    else:
        for item in ITEMS:
            quantity = cart.get(item["name"], 0)
            if quantity:
                name_column, quantity_column, remove_column = st.columns([5, 2, 2])
                name_column.write(f"{item['emoji']} **{item['name']}**")
                quantity_column.write(f"Quantity: {quantity}")
                if remove_column.button(
                    "Remove One",
                    key=f"remove_{role}_{item['name']}",
                    use_container_width=True,
                ):
                    if quantity == 1:
                        del cart[item["name"]]
                    else:
                        cart[item["name"]] = quantity - 1
                    st.rerun()

    if role == "seller":
        total = sum(
            item["price"] * cart.get(item["name"], 0)
            for item in ITEMS
        )
        st.markdown(f"### Total: ₩{total:,}")

    st.markdown("### 💬 Useful English")
    if role == "buyer":
        st.write('“I’d like some **apples**, please.”')
        st.write('“How much is it?”')
    else:
        st.write('“What would you like?”')
        st.write('“Here you are. Thank you!”')
