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
st.write("물건을 사고파는 영어 대화를 연습해 봐요.")

if st.session_state.role is None:
    st.subheader("어떤 역할을 연습할까요?")
    buyer, seller = st.columns(2)
    with buyer:
        with st.container(border=True):
            st.subheader("🧑‍💼 Buyer")
            st.write("가격을 확인하고 사고 싶은 물건을 골라요.")
            if st.button("구매자 선택하기", use_container_width=True):
                st.session_state.role = "buyer"
                st.session_state.cart = {}
                st.rerun()
    with seller:
        with st.container(border=True):
            st.subheader("🧑‍🍳 Seller")
            st.write("예산 안에서 물건을 골라 구매 리스트를 만들어요.")
            if st.button("판매자 선택하기", use_container_width=True):
                st.session_state.role = "seller"
                st.session_state.cart = {}
                st.rerun()
else:
    role = st.session_state.role
    heading = "구매자" if role == "buyer" else "판매자"

    if st.button("← 역할 선택으로 돌아가기"):
        st.session_state.role = None
        st.session_state.cart = {}
        st.rerun()

    st.subheader(f"{'🧑‍💼' if role == 'buyer' else '🧑‍🍳'} {heading} 화면")
    if role == "buyer":
        st.info("💰 구매 가능 예산: **₩2,000**")
        st.caption("물건의 가격은 표시되지 않아요.")
    else:
        st.caption("물건의 종류와 가격을 확인해 보세요.")

    st.markdown("### 물건 고르기")
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
                    "구매 리스트에 담기",
                    key=f"add_{role}_{item['name']}",
                    use_container_width=True,
                ):
                    cart = st.session_state.cart
                    cart[item["name"]] = cart.get(item["name"], 0) + 1
                    st.rerun()

    st.markdown("### 🧺 구매 리스트")
    cart = st.session_state.cart
    if not cart:
        st.write("아직 담은 물건이 없어요. 위에서 물건을 골라 보세요.")
    else:
        for item in ITEMS:
            quantity = cart.get(item["name"], 0)
            if quantity:
                name_column, quantity_column, remove_column = st.columns([5, 2, 2])
                name_column.write(f"{item['emoji']} **{item['name']}**")
                quantity_column.write(f"수량: {quantity}")
                if remove_column.button(
                    "하나 빼기",
                    key=f"remove_{role}_{item['name']}",
                    use_container_width=True,
                ):
                    if quantity == 1:
                        del cart[item["name"]]
                    else:
                        cart[item["name"]] = quantity - 1
                    st.rerun()

    st.markdown("### 💬 Useful English")
    if role == "buyer":
        st.write('“I’d like some **apples**, please.”')
        st.write('“How much is it?”')
    else:
        st.write('“What would you like?”')
        st.write('“Here you are. Thank you!”')
