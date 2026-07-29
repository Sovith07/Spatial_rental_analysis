import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv(r'D:\vs code projects\rental_analysis\app\data_viz1.csv')
feature_text = pickle.load(open(r'D:\vs code projects\rental_analysis\app\feature_text.pkl','rb'))
wordcloud_df=pd.read_csv(r'D:\vs code projects\rental_analysis\app\wordcloud.csv')

group_df = new_df.groupby('sector')[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

sector = sorted(wordcloud_df['sector'].unique().tolist())
sector.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector)
st.header('Features Wordcloud')

if selected_sector == 'overall':
  main = []
  for item in wordcloud_df['features'].dropna().apply(ast.literal_eval):
    main.extend(item)
  feature_text = ' '.join(main)
  plt.rcParams["font.family"] = "Arial"   
  wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = set(['s']),  # Any stopwords you'd like to exclude
                        min_font_size = 10).generate(feature_text)
  
     
  # Create figure
  fig, ax = plt.subplots(figsize=(8, 8))
  
  # Display word cloud
  ax.imshow(wordcloud, interpolation="bilinear")
  ax.axis("off")
  
  # Remove extra padding
  fig.tight_layout(pad=0)
  
  # Display in Streamlit
  st.pyplot(fig)

else:
  def wordcloud_bysector(sector):
   
    main = []
    for item in wordcloud_df[(wordcloud_df['features'].notna() ) & (wordcloud_df['sector']==sector)]['features'].dropna().apply(ast.literal_eval):
     main.extend(item)

    feature_text = ' '.join(main)
    plt.rcParams["font.family"] = "Arial"

    wordcloud = WordCloud(width = 800, height = 800, 
                      background_color ='white', 
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

   
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display word cloud
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    # Remove extra padding
    fig.tight_layout(pad=0)

    # Display in Streamlit
    st.pyplot(fig)
  wordcloud_bysector(selected_sector)  


st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig3)