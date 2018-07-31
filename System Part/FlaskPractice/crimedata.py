import pandas as pd
import numpy as np

crime = pd.read_hdf('crime.h5')

temp = crime[['OFFENSE_TYPE_ID', 'GEO_LON', 'GEO_LAT']]
crime2 = temp.head(100)

centre = crime2[['GEO_LON', 'GEO_LAT']].apply(np.mean, axis=0)
x = crime2.to_records(index=False)


marker = []
for i in x:
    item = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        'lat': i[2],
        'lng': i[1],
        'infobox': i[0]
    }
    marker.append(item)
