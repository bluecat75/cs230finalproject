'''
Name: Jeremy Wang
CS230: Section SN1
Data: Used cars for sale on Craigslist
URL: Link to your web application online (see extra credit)

Description: This program can display info like price, odometer, title status etc... after user input year, brand, model.
It also shows graphs and other statistic analysis.
'''

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import math
import pydeck as pdk

auto = pd.read_csv('C:\\Users\\wangz\\Desktop\\CS230\\finalproject\\cl_used_cars_7000_sample.csv')

#prepare for creating the map
map_data = auto[['lat','long','url']]
map_data = map_data.dropna()
map_data.columns = ['lat','lon','url']

#Background
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://i.pinimg.com/originals/87/e4/40/87e440a832ceb59304edc1f673a64f98.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)


#Lists
years = []
brands = []
year = auto.year.tolist()
#manufacturer = auto.manufacturer.tolist()
#model = auto.model.tolist()

#Years
year1 = [int(x) for x in year if math.isnan(x) == False]
year2 = [str(x) for x in year1]
for x in year2:
    if x not in years:
        years.append(x)
    else:
        pass
years.sort(reverse= True)
st.title('Used cars for sale on Craigslist')
st.sidebar.title('Navigation')
year_option = st.sidebar.selectbox("Years",years)

#Brands
brand1 = auto['manufacturer'][auto['year'] == float(year_option)].values
brand2 = [x for x in brand1 if pd.isnull(x) == False]
for x in brand2:
    if x not in brands:
        brands.append(x)
    else:
        pass
brands.sort()
brands_option = st.sidebar.selectbox("Brands",brands)

#Models
model = auto['model'][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))].tolist()
model_option = st.sidebar.selectbox("Model",model)

def car(variable,number):
    vehicle = auto[variable][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))& (auto['model'] == str(model_option))].values[number]
    return vehicle
def howmany():
    number = auto["year"][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))& (auto['model'] == str(model_option))].count()
    return number

for x in range(howmany()):
    st.subheader("Price:")
    st.text(car("price",x))
    st.subheader("Odometer:")
    st.text(car("odometer",x))
    st.subheader("Title Status:")
    st.text(car("title_status",x))
    st.subheader("Transmission:")
    st.text(car("transmission",x))
    st.subheader("Drive:")
    st.text(car("drive",x))
    st.subheader("Fuel:")
    st.text(car("fuel",x))
    st.subheader("Paint Color:")
    st.text(car("paint_color",x))
    st.subheader("Description:")
    st.text(car("description",x))
    st.subheader("State:")
    st.text(car("state",x))
    st.subheader("Picture:")
    st.image(f"{car('image_url',x)}",width=600)
    st.text("_"*95)

#The Map
view_state = pdk.ViewState(
    latitude=map_data["lat"].mean(),
    longitude=map_data['lon'].mean(),
    zoom=6,
    pitch=0)

layer1 = pdk.Layer('ScatterplotLayer',
                  map_data,get_position='[lon, lat]',
                  get_radius=150,
                  get_color=[0,0,255],
                  pickable=True
                  )
tool_tip = {"html": "Url Name:<br/> <b>{url}</b> ",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}
          }

map1 = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',initial_view_state=view_state,layers=[layer1],tooltip= tool_tip)
st.pydeck_chart(map1)
st.text("_"*95)
#Other options/stats
options = st.sidebar.multiselect("Items you want to know",['VIN',"url",'type'])
table = pd.pivot_table(data=auto,index=options).head(10)
st.table(table)
st.text("_"*95)

st.subheader("Some Facts About This DataSet:")
total = auto["id"].count()
brands_number = auto.groupby('manufacturer')['id'].count().to_dict()
def read_dic(brands_number):
    st.subheader("Number of cars in each brands")
    for k,v in brands_number.items():
        st.write(f'{k:<20}  : {v:>15}')
read_dic(brands_number)
average_price = auto['price'].mean()
min_price = auto['price'].min()
max_price = auto['price'].max()
st.write(f'The dataset contains {total} row of information. The car price range between {min_price} and {max_price}. The average price of the cars is {average_price}.')


count = auto["price"][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))].count()
price = auto["price"][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))].values
odometer = auto["odometer"][(auto['year']== float(year_option))& (auto['manufacturer'] == str(brands_option))].values

#graph
def bar_chart_1():
    st.subheader("Model vs. price in the same year and brands")
    chart_data = pd.DataFrame(price,model)
    st.bar_chart(chart_data)
def bar_chart_2():
    st.subheader("Model vs. Odometer in the same year and brands")
    chart_data1 = pd.DataFrame(odometer,model)
    st.bar_chart(chart_data1)
def scatter():
    st.write("Price vs. Odometer for Entire Dataset")
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.scatter(
        auto["price"],
        auto["odometer"],
        )

    ax.set_xlabel("price")
    ax.set_ylabel("Odometer")
    ax.ticklabel_format(useOffset=False, style='plain')
    st.write(fig)

bar_chart_1()
bar_chart_2()
scatter()
