import streamlit as st
import random
from PIL import Image
from pyzbar.pyzbar import decode

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EcoScanner", page_icon="🌿", layout="centered")

# ---------------- DARK THEME + TREE CSS ----------------
CSS = """
<style>
.stApp {
    background: linear-gradient(135deg, #1a0033, #330066, #660099);
    color: #ffffff;
    font-family: 'Segoe UI';
}

.big-title {
    font-size:40px;
    text-align:center;
    font-weight:700;
    color:#e1bee7;
}

.subtitle {
    text-align:center;
    color:#ce93d8;
}

.mascot {
    text-align:center;
    font-size:70px;
    animation: bounce 1.5s infinite;
}

@keyframes bounce {
    0%,100% {transform:translateY(0);}
    50% {transform:translateY(-10px);}
}

.tree {
    width: 120px;
    margin: auto;
    text-align:center;
    animation: grow 1.5s ease-in-out;
}

@keyframes grow {
    from {transform: scale(0.3);}
    to {transform: scale(1);}
}

.progress-container {
    height:22px;
    background:#4a0073;
    border-radius:14px;
    overflow:hidden;
}

.progress-bar {
    height:100%;
    background:#d1c4e9;
}

.stButton>button {
    background-color:#6a0dad;
    color:#fff;
    border-radius:12px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
for key in ["achievements","leaderboard","music_played"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------------- HEADER ----------------
st.markdown("<div class='mascot'>🌍🌿</div>", unsafe_allow_html=True)
st.markdown("<div class='big-title'>EcoScanner</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Scan • Learn • Grow Green</div>", unsafe_allow_html=True)

# ---------------- TABS ----------------
tabs = st.tabs(["📷 Barcode Scanner","🔎 Eco Scanner","🌳 Eco Tree","🏆 Achievements"])

# =====================================================
# 📷 BARCODE SCANNER (MOBILE CAMERA)
# =====================================================
with tabs[0]:
    st.header("📷 Scan Product Barcode")

    image = st.camera_input("Scan barcode using your mobile camera")

    if image:
        img = Image.open(image)
        barcodes = decode(img)

        if barcodes:
            for barcode in barcodes:
                code = barcode.data.decode("utf-8")
                st.success(f"Barcode detected: {code}")

                # Demo logic (you can connect database later)
                st.info("Sample Product Detected")
                st.write("Material: Plastic")
                st.write("Packaging: Plastic Wrapper")
        else:
            st.error("No barcode detected. Try again.")

# =====================================================
# 🔎 ECO SCANNER
# =====================================================
with tabs[1]:
    st.header("🔎 Eco Score Analyzer")

    material = st.selectbox("Material", ["Cotton","Jute","Plastic","Metal","Glass"])
    packaging = st.selectbox("Packaging", ["Plastic Wrapper","Paper Wrap","Glass Jar","No Packaging"])
    eco_traits = st.multiselect("Eco Features", ["Recyclable","Organic","Plastic-Free"])

    if st.button("Analyze Product"):
        score = 50
        if material == "Plastic": score -= 25
        if material == "Glass": score += 15
        if packaging == "Plastic Wrapper": score -= 15
        if packaging in ["Paper Wrap","Glass Jar","No Packaging"]: score += 10
        score += len(eco_traits) * 10
        score = max(0, min(100, score))

        st.subheader("Eco Score")
        st.markdown(
            f"<div class='progress-container'><div class='progress-bar' style='width:{score}%'></div></div>",
            unsafe_allow_html=True
        )
        st.write(f"🌱 Score: **{score}/100**")

        if score >= 75:
            st.session_state["achievements"].append("Eco Friendly Choice 🌿")
            st.balloons()

        st.session_state["last_score"] = score

# =====================================================
# 🌳 TREE GROWING ANIMATION
# =====================================================
with tabs[2]:
    st.header("🌳 Your Eco Tree")

    score = st.session_state.get("last_score", 0)

    if score == 0:
        st.info("Analyze a product to grow your tree 🌱")

    elif score < 40:
        st.markdown("<div class='tree'>🌱</div>", unsafe_allow_html=True)
        st.write("Small Sapling")

    elif score < 70:
        st.markdown("<div class='tree'>🌿</div>", unsafe_allow_html=True)
        st.write("Growing Tree")

    else:
        st.markdown("<div class='tree'>🌳</div>", unsafe_allow_html=True)
        st.write("Healthy Big Tree 🌍")

# =====================================================
# 🏆 ACHIEVEMENTS
# =====================================================
with tabs[3]:
    st.header("🏆 Achievements")

    if st.session_state["achievements"]:
        for a in st.session_state["achievements"]:
            st.success(a)
    else:
        st.info("No achievements yet. Start scanning!")


