from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import time

st.set_page_config(
    page_title="🏎️ F1 Pit Wall AI",
    page_icon="🏁",
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
    color: white;
}

.stApp {
    background: linear-gradient(135deg, #050505 0%, #0b0b0b 45%, #8b0000 100%);
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.15);
    border-left: 5px solid #e10600;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(225,6,0,0.25);
    transition: all 0.4s ease-in-out;
}

.glass:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(225,6,0,0.4);
}

.main-title {
    font-size: 3.2rem;
    font-weight: 900;
    color: #ff1e1e;
    text-align: center;
    letter-spacing: 2px;
}

.subtitle {
    text-align: center;
    font-style: italic;
    margin-bottom: 1.5rem;
}

.red-light {
    display: inline-block;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: red;
    margin: 4px;
    box-shadow: 0 0 18px red;
    animation: pulse 1.2s infinite;
}

@keyframes pulse {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🏎️ F1 PIT WALL AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Lights out and away we go.</div>", unsafe_allow_html=True)

# ---------------- START LIGHTS ----------------
st.markdown("### 🔴 Race Start Sequence")
lights_placeholder = st.empty()

for i in range(1, 6):
    lights_html = "".join(["<span class='red-light'></span>" for _ in range(i)])
    lights_placeholder.markdown(lights_html, unsafe_allow_html=True)
    time.sleep(0.35)

time.sleep(0.5)
lights_placeholder.markdown("## 🏁 LIGHTS OUT!", unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Championship")
st.sidebar.subheader("Driver Standings")

standings = {
    "Verstappen": 88,
    "Leclerc": 74,
    "Norris": 69,
    "Russell": 61,
    "Hamilton": 55
}

st.sidebar.bar_chart(standings)

st.sidebar.divider()
st.sidebar.subheader("🛞 Strategy Simulator")

track = st.sidebar.selectbox(
    "Select Track",
    ["Monaco", "Silverstone", "Monza", "Suzuka"]
)

weather = st.sidebar.selectbox(
    "Weather",
    ["Dry", "Wet", "Mixed"]
)

if st.sidebar.button("Simulate Strategy"):
    if weather == "Dry":
        st.sidebar.success("🟡 Soft → ⚪ Medium → ⚪ Medium")
    elif weather == "Wet":
        st.sidebar.info("🔵 Inter → 🟢 Wet → ⚪ Medium")
    else:
        st.sidebar.warning("🟡 Soft → 🔵 Inter → ⚪ Medium")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2.2, 1], gap="large")

with left:
    st.markdown("### 📻 Team Radio")

    input_txt = st.text_input(
        "",
        placeholder="Ask your driver/team question...",
        label_visibility="collapsed"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
 "You are an expert Formula 1 AI assistant. Always give factually correct and verified Formula 1 answers. "
 "If the user's question is ambiguous, ask for clarification instead of guessing. "
 "Use race engineer style phrases only after giving the correct answer."),
        ("user", "{query}")
    ])

    llm = Ollama(model="llama2")
    parser = StrOutputParser()
    chain = prompt | llm | parser

    if input_txt:
        response = chain.invoke({"query": input_txt})
        st.markdown(
            f"<div class='glass'><b>📡 Race Engineer:</b><br><br>{response}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='glass'><b>🏁 Grid Update:</b> Waiting on your team radio message...</div>",
            unsafe_allow_html=True
        )

with right:
    st.markdown("### 🏁 Race Weekend")

    st.markdown("""
    <div class='glass'>
    <b>🏆 2026 GP Winners</b><br><br>
    🇦🇺 Australia — George Russell<br>
    🇨🇳 China — Kimi Antonelli<br>
    🇯🇵 Japan — Kimi Antonelli
    </div>
    """, unsafe_allow_html=True)

    facts = [
        "🗣️ 'Simply lovely!' — Verstappen",
        "🎤 'Leave me alone, I know what I'm doing' — Kimi",
        "⚡ Pit stops below 2 seconds",
        "😂 Vettel swapped P1 boards",
        "🌧️ Brazil 2016 magic",
        "🔥 Monaco = pressure cooker",
        "😂'Leave me alone, I know what to do' – Kimi Räikkönen (Abu Dhabi 2012).",
        "🔥'I have the seat full of water!' – Charles Leclerc (Australia 2025).",
        "🗣️'Just let me fing drive!' – George Russell (Austria 2024).",
        "⚡'Bring back the fking V12s' – Sebastian Vettel (Russia 2019).",
        "🔥'The marshals must be having a beer then!' – Carlos Sainz (Hungary 2019).",
        "🎤'I like 'em vulnerable' – Daniel Ricciardo (Monaco 2017).",
        "⚡'Giant lizard on the track' – Max Verstappen (Singapore 2016).",
        "🗣️'Tell him to get out of the way' – Kimi Räikkönen (Austria 2018).",
        "⚡'Paddy, I am actually in the lead right now, I'm quite comfortable here' – Lewis Hamilton (Abu Dhabi 2016)."
    ]

    st.markdown(
        "<div class='glass'><b>🔥 F1 Moments</b><br><br>"
        + "<br><br>".join(facts)
        + "</div>",
        unsafe_allow_html=True
    )