import pandas as pd
import streamlit as st
import pydeck as pdk

st.set_page_config(page_title="FA-FPO_Map", layout="wide")

df_fresh=pd.read_excel('/app/fa-fpo-mapping/fa_fpo_gps.xlsx', sheet_name='Sheet1')
df = df_fresh[df_fresh['lat'].notnull()]
df = df[df['FA Mobile'].notnull()]
df['FA Mobile']=df['FA Mobile'].round(decimals=0)

df['FA Mobile']=df['FA Mobile'].astype(str)
df = df[df['Cycle'].notnull()]

df2=pd.read_excel('/app/fa-fpo-mapping/fa_fpo_gps.xlsx', sheet_name='Sheet2')
df2 = df2[df2['FAPhoneNumber'].notnull()]

df2['FAPhoneNumber']=df2['FAPhoneNumber'].astype(str)

st.header("Welcome to FA-FPO Mapping Plot:")

st.subheader("Select a Parameter to Filter:")

fa_num_selected = st.selectbox(label="Select FA Mobile Number:", options=df['FA Mobile'].unique())

df_filtered = df[df['FA Mobile']== fa_num_selected]

st.subheader("FPO Location Details:")
st.table(df_filtered)

# st.write(fa_num_selected[0:10])

df2_filtered = df2[df2['FAPhoneNumber'] == fa_num_selected[0:10]]
st.subheader("FA Location details:")
st.table(df2_filtered)

# st.map(df)



layer1=pdk.Layer(
    'ScatterplotLayer', 
    data=df_filtered, 
    get_position='[lon, lat]',
    auto_highlight=True,
    get_radius=500,

    get_fill_color='[37, 150, 90, 140]',
    pickable=True 
    )

layer2=pdk.Layer(
    'ScatterplotLayer', 
    data=df2_filtered, 
    get_position='[lon, lat]',
    auto_highlight=True,
    get_radius=200,

    get_fill_color='[180, 0, 200, 140]',
    pickable=True 
    )

# layer2=pdk.Layer(
#     'HexagonLayer',
#     df,
#     get_position=['lon', 'lat'],
#     auto_highlight=True,
#     elevation_scale=40,
#     pickable=True,
#     elevation_range=list(df['farmer']),
#     extruded=True,
#     coverage=1)

# st.write(df_filtered['lat'].max())

view_state = pdk.ViewState(
    longitude=df_filtered['lon'].max(),
    latitude=df_filtered['lat'].max(),
    zoom=10,
    min_zoom=1,
    max_zoom=20,
    pitch=20,
    # bearing=
    )

r=pdk.Deck(initial_view_state=view_state, layers=[layer1, layer2], map_style='light')

st.pydeck_chart(r)

# r.to_html('map_new.html')

