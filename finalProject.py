import streamlit as st
import numpy as np
import pandas as pd
import csv
from emoji import emojize #new module not used in class



def processDataFiles():
    fileName = 'Skyscrapers2021(1).csv'
    with open(fileName) as f:
        reader = csv.reader(f)
        skyscraperlist = list(reader)
    f.close()
    return skyscraperlist

#title of the page
st.title('Skyscraper Data Around the World')
st.write('This app shows data for skyscrapers around the world. Using the selection boxes and sliders  you can see the '
         'locations, names, and other fun facts about these skyscrapers!')

st.write("Hello :wave:") #using new emoji module
radio = st.radio('Select a unit of measure', ['Feet','Meters'])



def maps(pdskyscraperlist):
    import streamlit as st
    import pydeck as pdk
    import pandas as pd

    #reading the skyscraper data
    df = pd.read_csv("Skyscrapers2021(1).csv", usecols=['NAME', 'CITY', 'latitude', 'longitude','Feet', 'Meters'])
    print(df)
    st.title("Skyscraper's Around the World")
    st.dataframe(df)


    #filtering out city to use in a selectbox
    city_select = st.selectbox("Choose a city", pd.unique(df['CITY']))
    filtered_city = df[df["CITY"] == city_select]
    st.write('You selected:', city_select)
    st.write('This map shows locations of all the sky scrapers in', city_select)

    #creating the first map showing city based on selectbox selection
    st.map(filtered_city)


    #filtering out feet data to use with a slider
    st.write('Use this slider to select the height range (in Feet) of skyscrapers you want to see')
    feetData = df[['NAME','Feet', 'CITY', 'latitude','longitude']] #call the data
    feetDF = pd.DataFrame(feetData) #change to a dataframe
    newheight = [x[:-3] for x in feetData['Feet']] #removing the 'ft' string
    newheight = [int(x.replace(',', '')) for x in newheight] #replacing old feet list with new
    feetDF.Feet = newheight #same naming convention

    #creating the slider using flitered data for feet
    feet = feetDF['Feet'] #naming the feet column
    feetOption = st.slider('Choose height in feet:', min(feet), max(feet))
    filteredList = feetDF[feetDF['Feet']<=feetOption] #creating a filtered list based on slider
    # if radio == 'Feet':
    #     feetOption = st.slider('Height', df['Feet'])
    # else:
    #     feetOption = st.slider('Height', df['Meters'])

    #creating the second map that shows information about each skyscraper
    map_data = pd.DataFrame(filteredList)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=map_data,
                       get_position='[longitude, latitude]',
                       get_radius=150000,
                       get_color="blue",
                       pickable=True)

    tool_tip = {"html": "<b>Skyscraper:</b> {NAME}"
                "<br/> <b>City:</b> {CITY}"
                "<br/> <b>Height (ft):</b> {Feet}",
                "style": { "backgroundColor": "purple",
                          "color": "white"}}

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=df["latitude"].mean(), #default to center of map
            longitude=df["longitude"].mean(),
            zoom=1,
            pitch=20),
        layers=[layer1],
        tooltip=tool_tip))


    #THIS is my something cool
    #I found this gridLayer map that visually shows the elevation. So I thought it would be a cool way to show the heights
    #of each skyscraper
    st.write("Grid Layer Map")
    st.write('This map shows a visual of the heights of the skyscrapers around the world')
    gf = pd.read_csv("Skyscrapers2021(1).csv", usecols=['NAME', 'latitude', 'longitude', 'Feet', 'Meters'])
    st.dataframe(gf)

    #code to try and get the elevation range for each skyscraper

    #height_of_skyscraper = gf.loc[:,'Feet']
    #sky = height_of_skyscraper.values
    #str(sky)
    #unit ='ft'
    #res = re.findall('\d+', ' '.join(sky))
    #print(str(res))
    #numpy_array = np.genfromtxt("Skyscrapers2021(1).csv", delimiter=";", skip_header=1)
    #Feet = np.arange(float(min('Feet')), float(max('Feet')))
    layer = pdk.Layer(
        "GridLayer", data=gf, pickable=True, extruded=True, cell_size=200, elevationRange=[1000, 10000], elevation_scale=4, get_position='[longitude, latitude]',
    )
    tool_tip1 = {"html": "Skyscraper Name:<br/> <b>{NAME}</b> "
                "<br/> <b>Height (ft):</b> {Feet}",
                "style": { "backgroundColor": "steelblue",
                            "color": "white"}
              }

    view_state1 = pdk.ViewState(latitude=gf["latitude"].mean(), longitude=df["longitude"].mean(), zoom=11, bearing=0, pitch=45)

    # shows the gridlayer map
    r = pdk.Deck(layers=[layer], initial_view_state=view_state1, tooltip=tool_tip1)
    st.pydeck_chart(r)


def construction(pdskyscraperlist):
    import streamlit as st
    import pydeck as pdk
    import pandas as pd
    import matplotlib.pyplot as plt

    #showing the construction information for each skyscraper in a dataframe
    st.title('Skyscraper Construction Information')
    st.text('Construction Information')
    cf = pd.read_csv("Skyscrapers2021(1).csv", usecols = ['NAME','latitude', 'longitude', 'Meters', 'Feet', 'Height', 'FLOORS', 'COMPLETION','MATERIAL'])
    print(cf)
    #dataframe of construction information
    st.dataframe(cf)
    tf = pd.read_csv("Skyscrapers2021(1).csv", usecols = ['NAME','latitude', 'longitude', 'Meters', 'Feet', 'Height', 'FLOORS', 'COMPLETION','MATERIAL'])

    #creating a checkbox to show the data
    is_check = st.checkbox("Display Data")
    if is_check:
        st.table(tf)

    #creating a sidebar with multiselect optins
    columns = st.sidebar.multiselect("Enter a skyscraper element", tf.columns)

    #creating side bar filters with multiselect options based on the data selected
    sidebars = {}
    #for loop creating the sidebar and multiselect options
    for y in columns:
        ucolumns=list(tf[y].unique())
        print(ucolumns)

        sidebars[y] = st.sidebar.multiselect('Filter '+y, ucolumns)
    #if showing the second sidebar
    if bool(sidebars):
        L = [tf[k].isin(v) if isinstance(v, list)
             else tf[k].eq(v)
             for k, v in sidebars.items() if k in tf.columns]

        df1 = tf[np.logical_and.reduce(L)]
        st.table(df1)

    #Pie chart showing the percentage of materials used to construct the skyscrapers
    #filtering out the material from the data frame
    material_count = cf.groupby(by = 'MATERIAL').count() #getting a count of materials
    #st.write(material_count)
    #st.write(material_count.sum())
    filtered_materials = pd.unique(cf['MATERIAL']) #grabbing each unique material so they don't repeat
    #st.write(filtered_materials)
    print(material_count, filtered_materials)
    st.write("This pie chart shows the percentage of each material used to construct all 100 skyscrapers!")
    #getting each total number of material and dividing by 100 for percentage
    composite = (material_count.iloc[0,0])/100
    concrete = (material_count.iloc[1,0])/100
    steel = (material_count.iloc[2,0])/100
    steel_concrete = (material_count.iloc[3,0])/100


    #creating pie chart
    fig1, ax1 = plt.subplots()
    list_of_materials = [composite, concrete, steel, steel_concrete]
    labels = ["Composite", "Concrete", "Steel", "Steel/Concrete"]
    ax1.pie(list_of_materials, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(labels, loc="best")
    #setting title
    ax1.set_title('Materials by Percent', fontname="Impact")

    plt.show()
    st.pyplot(fig1)
    print(material_count//material_count.sum())

def main():
    pdskyscraperlist = processDataFiles()
    df = pd.read_csv("Skyscrapers2021(1).csv", usecols=['NAME', 'latitude', 'longitude','Feet', 'Meters'])
    processDataFiles()
    maps(pdskyscraperlist)
    construction(pdskyscraperlist)



main()
