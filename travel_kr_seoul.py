import streamlit as st
import streamlit.components.v1 as components

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Load API Key
API_KEY_PATH = r"C:\DS_2025_Intern\keys\.openai_api_key.txt"

if os.path.exists(API_KEY_PATH):
    with open(API_KEY_PATH, "r") as f:
        GOOGLE_API_KEY = f.read().strip()
else:
    st.error("🔑 API Key file not found. Please check the file path.")
    st.stop()

# Initialize AI Model
chat_model = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-2.0-flash-exp", temperature=1)

# Define the chat template
chat_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful AI assistant providing estimated travel costs, available transport options, and language communication tips within South Korea."),
        ("human", "Find the best travel options from {source} to {destination}, including cost, available transport options, and local language tips."),
    ]
)

parser = StrOutputParser()
chain = chat_template | chat_model | parser

# Streamlit UI
st.set_page_config(layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #ff5733;'>🇰🇷 <span style='color: #ffcc00;'>AI-Powered</span> <span style='color: #33cc33;'>Travel Planner</span> (South Korea) ✈️🚆🚌🚗</h1>", 
    unsafe_allow_html=True
)

audio_path = r"C:\streamlit\travel\kr.mp3"
if os.path.exists(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.write("🔊 Click Play to hear useful Korean travel phrases!")
        else:
            st.error("⚠️ Audio file is empty. Please check the file.")
else:
    st.warning("⚠️ Audio file not found. Please check the path.")



snowfall_html = """
<div id="snow-container"></div>
<style>
  #snow-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
  .snowflake {
    position: absolute;
    font-size: 15px;
    opacity: 0.9;
    user-select: none;
  }
</style>
<script>
  function getRandomColor() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff', '#00ffff', '#ffff00', '#ffa500', '#800080']; 
    return colors[Math.floor(Math.random() * colors.length)];
  }

  function createSnowflake() {
    let snowflake = document.createElement('div');
    snowflake.innerHTML = '❄';
    snowflake.classList.add('snowflake');
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.top = '-20px';
    snowflake.style.fontSize = Math.random() * 20 + 10 + 'px';
    snowflake.style.color = getRandomColor();  

    document.getElementById('snow-container').appendChild(snowflake);

    let speed = Math.random() * 3 + 2;
    let angle = Math.random() * 2 - 1;

    function fall() {
      if (parseFloat(snowflake.style.top) < window.innerHeight) {
        snowflake.style.top = parseFloat(snowflake.style.top) + speed + 'px';
        snowflake.style.left = parseFloat(snowflake.style.left) + angle + 'px';
        requestAnimationFrame(fall);
      } else {
        snowflake.remove();
      }
    }
    fall();
  }

  setInterval(createSnowflake, 200);
</script>
"""


components.html(snowfall_html, height=150)












# Sidebar with fixed place names
st.sidebar.header("🌍 Popular Locations in South Korea")
places = {
    "Seoul": "🏙️", "Busan": "🌊", "Incheon": "🛫", "Daegu": "🏢",
    "Daejeon": "🔬", "Gwangju": "🎨", "Ulsan": "🏭", "Jeju": "🏝️",
    "Suwon": "🏰", "Pohang": "⚓", "Jeonju": "🥢", "Gyeongju": "🏛️",
    "Chuncheon": "🌲", "Andong": "🎎"
}

for place, emoji in places.items():
    st.sidebar.write(f"{emoji} **{place}**")

# User Input Section (Two Columns)
col1, col2 = st.columns([1, 2])

# Left Column: User Inputs
with col1:
    source = st.selectbox("📍 Select Source Location:", list(places.keys()))
    destination = st.selectbox("🎯 Select Destination:", list(places.keys()))
    
    # Travel Mode Selection
    st.subheader("🚖 Choose Travel Mode")
    travel_modes = {
        "Train 🚆": "train",
        "Bus 🚌": "bus",
        "Plane ✈️": "plane",
        "Car 🚗": "car"
    }
    
    selected_mode = st.radio("Select Your Preferred Travel Mode:", list(travel_modes.keys()))

    if st.button("🔍 Get Travel Options"):
        if source and destination and source != destination:
            response = chain.invoke({"source": source, "destination": destination})
            st.success("✅ Here are your travel options:")
            st.write(response)

            # Language and Communication Tips
            st.subheader("🗣 Language & Communication Tips")
            language_tips = {
                "Seoul": "🗣 Korean is the primary language. Many people, especially younger generations, understand English.",
                "Busan": "📢 Busan has a unique dialect, but standard Korean is understood. English is spoken in tourist areas.",
                "Incheon": "✈️ English is common near the airport. Learning basic Korean phrases helps.",
                "Daegu": "🔤 Limited English speakers. Learn key Korean travel phrases.",
                "Daejeon": "🔬 Basic English in major areas, but Korean is necessary for deeper communication.",
                "Gwangju": "🎨 Mostly Korean-speaking. English signs are available in major spots.",
                "Ulsan": "🏭 Industrial city with some English-speaking professionals.",
                "Jeju": "🏝️ Tourist-friendly with good English support in key attractions.",
                "Suwon": "🏰 Limited English. Learning basic Korean is helpful.",
                "Pohang": "⚓ More Korean speakers, minimal English outside tourist spots.",
                "Jeonju": "🥢 Traditional Korean city; knowing basic Korean is useful.",
                "Gyeongju": "🏛️ Historical city with some English support at landmarks.",
                "Chuncheon": "🌲 Mostly Korean speakers, English signs in tourist spots.",
                "Andong": "🎎 Traditional town, knowing Korean phrases is beneficial."
            }
            st.write(language_tips.get(source, "🗣 Korean is the main language spoken here. Learning a few basic phrases will be very helpful!"))
        else:
            st.error("⚠️ Please select different source and destination.")

# Right Column: Travel Images
image_paths = {
    "train": r"C:\streamlit\travel\train.webp",
    "bus": r"C:\streamlit\travel\bus.webp",
    "plane": r"C:\streamlit\travel\plane.webp",
    "car": r"C:\streamlit\travel\car.webp"
}

with col2:
    if selected_mode:
        selected_image = travel_modes[selected_mode]
        image_path = image_paths.get(selected_image)
        if os.path.exists(image_path):
            st.image(image_path, caption=f"🚆 {selected_mode} Travel in South Korea", use_column_width=True)
        else:
            st.warning(f"⚠️ Image not found: {image_path}")

# Audio File Handling (Basic Korean Phrases)
st.subheader("🎧 Learn Basic Korean Phrases")

phrases = {
    "Hello": "안녕하세요 (Annyeonghaseyo)",
    "Thank you": "감사합니다 (Gamsahamnida)",
    "Yes": "네 (Ne)",
    "No": "아니요 (Aniyo)",
    "Excuse me": "실례합니다 (Sillyehamnida)",
    "Where is the bathroom?": "화장실 어디에요? (Hwajangsil eodieyo?)",
    "How much is this?": "이거 얼마에요? (Igeo eolmaeyo?)",
    "I don't understand": "이해하지 못해요 (Ihaehaji mothaeyo)"
}
for eng, kor in phrases.items():
    st.write(f"🔹 **{eng}**: {kor}")








# Add Travel Map Feature
# 🗺️ Google Maps or Kakao Map Integration
st.subheader("📍 View Your Travel Route")
map_choice = st.radio("Choose Map API:", ["Google Maps", "Kakao Map"])

if map_choice == "Google Maps":
    GOOGLE_MAPS_URL = f"https://www.google.com/maps/dir/{source}/{destination}"
    st.markdown(f"[🗺️ Open in Google Maps]({GOOGLE_MAPS_URL})", unsafe_allow_html=True)
elif map_choice == "Kakao Map":
    KAKAO_MAP_URL = f"https://map.kakao.com/?sName={source}&eName={destination}"
    st.markdown(f"[🗺️ Open in Kakao Map]({KAKAO_MAP_URL})", unsafe_allow_html=True)

















# Sidebar Navigation  
st.sidebar.title("📌 Navigation")
option = st.sidebar.radio("Select a category:", [
    "Destinations", "Transportation", "Accommodation", "Food & Dining", "Activities", "Culture & Tips", "Travel Essentials"
])

# Destinations Section  
if option == "Destinations":
    st.subheader("📍 Popular Destinations in South Korea")  
    st.markdown("""  
    - **[Seoul](https://english.visitkorea.or.kr/)** – 🏛️ Palaces, 🛍️ shopping, 🎶 K-pop culture  
    - **[Busan](https://www.visitbusan.net/index.do?locale=en_US)** – 🏖️ Beaches, 🦞 seafood, 🏯 coastal temples  
    - **[Jeju Island](https://www.visitjeju.net/en)** – 🌋 Volcanic island, ⛲ waterfalls, 🏕️ nature  
    """)

# Transportation Section  
elif option == "Transportation":
    st.subheader("🚆 Getting Around South Korea")  
    st.markdown("""  
    - 🚄 **[KTX (High-Speed Train)](https://www.letskorail.com/ebizbf/EbizBfTicketSearch.do)**  
    - 🚇 **[Subways & Buses](https://www.seoulmetro.co.kr/eng/)**  
    - 🚖 **[Kakao Taxi](https://www.kakaomobility.com/service/taxi/)** for easy rides  
    """)

# Accommodation Section  
elif option == "Accommodation":
    st.subheader("🏨 Where to Stay")  
    st.markdown("""  
    - 🏩 **Luxury Hotels:** [Lotte](https://www.lottehotel.com/global/en.html)  
    - 🏠 **Guesthouses & Hostels:** [HostelWorld](https://www.hostelworld.com/)  
    - 🏡 **Airbnb:** [Check Airbnb](https://www.airbnb.com/s/South-Korea/)  
    """)

# Food Section  
elif option == "Food & Dining":
    st.subheader("🍜 Must-Try Korean Dishes")  
    st.markdown("""  
    - 🌶️ **Kimchi (김치)** – Fermented spicy cabbage ([Read More](https://www.korea.net/NewsFocus/Culture/view?articleId=154891))  
    - 🍚 **Bibimbap (비빔밥)** – Mixed rice with vegetables ([Guide](https://www.tripsavvy.com/bibimbap-korean-rice-dish-2118870))  
    - 🥩 **Korean BBQ (삼겹살, 갈비)** – Grilled meat with side dishes ([Best BBQ Spots](https://seoulistic.com/where-to-eat/best-korean-bbq-restaurants-in-seoul/))  
    """)

# Activities Section  
elif option == "Activities":
    st.subheader("🎟️ Things to Do in South Korea")  
    st.markdown("""  
    - 🏯 **Palaces & Temples:** [Gyeongbokgung](https://www.royalpalace.go.kr/)  
    - 🛍️ **Shopping:** [Myeongdong](https://english.visitkorea.or.kr/)  
    - 🎶 **K-pop & Entertainment:** [SMTOWN Museum](https://www.smtownland.com/)  
    """)

# Culture & Tips Section  
elif option == "Culture & Tips":
    st.subheader("📖 Korean Culture & Travel Tips")  
    st.markdown("""  
    - 🗣️ **Basic Korean Phrases:** [Learn Here](https://www.90daykorean.com/common-korean-phrases/)  
    - 🤝 **Etiquette & Customs:** [Guide](https://www.korea.net/AboutKorea/Korean-Life/Etiquette)  
    - 👘 **Hanbok Rental:** [Traditional Dress](https://hanboknam.com/)  
    """)

# Travel Essentials Section  
elif option == "Travel Essentials":
    st.subheader("🛂 Travel Essentials")  
    st.markdown("""  
    - 🛂 **Visa:** [Apply for K-ETA](https://www.k-eta.go.kr/portal/apply/index.do)  
    - 💰 **Currency:** South Korean Won ([Exchange Rates](https://www.xe.com/currencyconverter/))  
    - 📶 **SIM Card & WiFi:** [Best SIMs](https://www.klook.com/en-US/city/96-seoul-things-to-do/34-internet-access/)  
    """)

st.success("🎉 You're ready to explore South Korea! Happy travels! ✈️")
