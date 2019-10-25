import nlp
import pandas as pd
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAlvT9QoXecXq_WFfd4_slajtCnMJBXB6Y')

dataframe = pd.read_csv('isthisarealjob_table_posts.csv')
dataframe = dataframe.drop(['3', '4', '2018-02-28 00:14:37', '2018-02-28 00:14:37.1', 'hello-world-071235157V21576', 'world,good', 'Unnamed: 9', 'NULL', 'NULL.1'], axis= 1)
dataframe = dataframe[['danny', '#world is greater than #good things', 'Hello World']]
dataframe_address = dataframe['#world is greater than #good things']
dataframe_address = dataframe_address.dropna()

#checking if the address actually exist
for address in dataframe_address:
    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    if geocode_result != '[]':
        print('1')
    else:
        print('0')
    # print(geocode_result)
