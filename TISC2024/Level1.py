import h3

//Your H3 indexes
h3_index_1 = '8c1e806a3ca19ff'
h3_index_2 = '8c1e806a3c125ff'
h3_index_3 = '8c1e806a3ca1bff'

//Convert H3 indexes to lat/lng
coord_1 = h3.h3_to_geo(h3_index_1)  # returns (latitude, longitude)
coord_2 = h3.h3_to_geo(h3_index_2)
coord_3 = h3.h3_to_geo(h3_index_3)

print(f"Location 1: {coord_1}")
print(f"Location 2: {coord_2}")
print(f"Location 3: {coord_3}")

//Calculate the centroid (average lat/lng)
centroid_lat = (coord_1[0] + coord_2[0] + coord_3[0]) / 3
centroid_lng = (coord_1[1] + coord_2[1] + coord_3[1]) / 3

print(f"Approximate triangulated location: ({centroid_lat}, {centroid_lng})")
