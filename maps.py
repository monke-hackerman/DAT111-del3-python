from geopy.geocoders import Nominatim


# Initialize geolocator (user_agent can be any custom string for your app)
geolocator = Nominatim(user_agent="student_assignment_project")

#senterpossisjon: -29533.35, 6731520.12
#60.3703, 5.3688 -> 50 x, 50 y

# 60.5229907010787, 5.090456376615228 -> 1.0 x, 100 y
# 60.5229907010787, 5.558965846770228 -> 100 x, 100 y
# 60.19622704750549, 5.090456376615228 -> 1x , 1 y
# 60.19622704750549, 5.558965846770228 -> 100 x, 1 y

def latlon_to_xy(lat, lon):
    # Definer ytterpunktene (Bounding Box) fra hjørnene
    lat_min = 60.19622704750549  # Venstre/Høyre nederst
    lat_max = 60.5229907010787   # Venstre/Høyre øverst
    lon_min = 5.090456376615228  # Venstre øverst/nederst
    lon_max = 5.558965846770228  # Høyre øverst/nederst
    
    # Skalaen kartet bruker (1 til 100)
    x_min, x_max = 1.0, 100.0
    y_min, y_max = 1.0, 100.0
    
    # Beregn x og y basert på hvor punktet ligger i forhold til grensene
    x = x_min + (lon - lon_min) / (lon_max - lon_min) * (x_max - x_min)
    y = y_min + (lat - lat_min) / (lat_max - lat_min) * (y_max - y_min)
    
    return round(x), round(y)

try:
    location = geolocator.geocode("Myrdalskogen 22, 5118 Ulset")

    if location:
        print(f"Latitude: {location.latitude}")
        print(f"Longitude: {location.longitude}")
        x_pos, y_pos = latlon_to_xy(location.latitude, location.longitude)
        print(f"Posisjon -> X: {x_pos}, Y: {y_pos}")
        
    else:
        print("No results found.")

except Exception as e:
    print(f"An error occurred: {e}")
