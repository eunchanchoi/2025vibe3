pip install streamlit-folium
import streamlit_folium
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="나만의 북마크 지도 🗺️", layout="wide")

st.title("📌 나만의 북마크 지도")
st.write("지도를 클릭해서 북마크를 추가해보세요!")

# 초기 위치: 서울
default_lat, default_lon = 37.5665, 126.9780

# 세션 상태에 북마크 저장
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 지도 생성
m = folium.Map(location=[default_lat, default_lon], zoom_start=12)

# 기존 북마크 마커 추가
for bm in st.session_state.bookmarks:
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=bm["label"],
        icon=folium.Icon(color="red", icon="bookmark")
    ).add_to(m)

# 지도 출력 (clickable)
st.markdown("### 🗺️ 지도")
map_data = st_folium(m, width=700, height=500)

# 지도 클릭시 마커 추가
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    with st.form("북마크 폼"):
        label = st.text_input("이 장소의 이름을 입력하세요", value=f"위치 {len(st.session_state.bookmarks)+1}")
        submitted = st.form_submit_button("북마크 추가")

        if submitted:
            st.session_state.bookmarks.append({"lat": lat, "lon": lon, "label": label})
            st.success(f"📌 '{label}' 북마크가 추가되었습니다!")
            st.experimental_rerun()

# 북마크 목록 출력
st.markdown("### 📍 북마크 목록")
if st.session_state.bookmarks:
    st.dataframe(st.session_state.bookmarks, use_container_width=True)
else:
    st.info("아직 북마크가 없습니다. 지도를 클릭해 추가해보세요!")
