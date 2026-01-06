import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# -----------------------------
# 1. تحميل ملفات البيانات
# -----------------------------

# ضع ملفات shapefile في نفس المجلد
services_path = "services2.shp"
road_path = "ksh.shp"

# قراءة بيانات الخدمات والطرق
services_gdf = gpd.read_file(services_path)
road_gdf = gpd.read_file(road_path)

# -----------------------------
# 2. عنوان التطبيق
# -----------------------------
st.set_page_config(page_title="تطبيق خدمات الطريق", layout="wide")
st.title("تطبيق خدمات الطريق")

# -----------------------------
# 3. اختيار نوع الخدمة
# -----------------------------
service_types = services_gdf['Type'].unique().tolist()
selected_service = st.selectbox("اختر نوع الخدمة", ["اختر خدمة"] + service_types)

# -----------------------------
# 4. عرض النتائج
# -----------------------------
if selected_service != "اختر خدمة":
    filtered = services_gdf[services_gdf['Type'] == selected_service]
    
    if filtered.empty:
        st.warning("لم يتم العثور على خدمات.")
    else:
        st.success(f"تم العثور على {len(filtered)} خدمة:")
        for idx, row in filtered.iterrows():
            st.write(f"**الاسم:** {row.get('الخدم', 'غير متوفر')}")
            st.write(f"**الهاتف:** {row.get('phone', 'غير متوفر')}")
            st.write(f"**العنوان:** {row.get('address', 'غير متوفر')}")
            st.markdown("---")
        
        # -----------------------------
        # 5. رسم الخريطة
        # -----------------------------
        # حساب مركز الخريطة
        center_lat = filtered.geometry.y.mean()
        center_lon = filtered.geometry.x.mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # إضافة الطرق (اختياري)
        folium.GeoJson(road_gdf).add_to(m)

        # إضافة نقاط الخدمات
        for idx, row in filtered.iterrows():
            folium.Marker(
                [row.geometry.y, row.geometry.x],
                popup=f"الاسم: {row['الخدم']}<br>الهاتف: {row['Phone']}<br>العنوان: {row['Address']}"
            ).add_to(m)

        # عرض الخريطة داخل Streamlit
        st_folium(m, width=700, height=500)
