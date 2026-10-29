import csv
from geopy.geocoders import Nominatim
import os

# Initialize geolocator (user_agent can be any custom string for your app)
geolocator = Nominatim(user_agent="Semester_oppgave_DAT111")

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

# Your data: The first sublist represents the headers
header = ["x", "y", "m2", "house_type", "standard", "sales_price"]
data = [
    # Your actual data rows go here:
    # [10, 20, 120, 1, 2.5, 350000],
]
#start loop to add multible rows at a time
adding = True
while adding:
    #Exit only by y or Y
    test = input("Wanna quit [N/y]?")
    if (test == "y" or test == "Y"):
        adding = False
    else:
        #enter data, Exprtion for worng types and value errors
        try:
            noError = True
            next = []
            #Make sure adress can translate to X, Y cordinates, cant have gaps in data
            try:
                location = geolocator.geocode(input("Adresse: "))
                if location:
                    x_pos, y_pos = latlon_to_xy(location.latitude, location.longitude)
                else:
                    print("No results found.")
                    noError = False
            except Exception as e:
                print(f"An error occurred: {e}")
                noError = False
                break

            #append to list next
            next.append(x_pos)
            next.append(y_pos)
            next.append(int(input("m2: ")))
            next.append(int(input("House_type ene: 1, Rekke: 2, legnlighet: 3: ")))
            next.append(float(input("Standard skala 1.0-4.0: ")))
            next.append(int(input("Salgs pris: ")))

        except ValueError:
            print("Oops! That was not a valid number. Try again...")
            noError = False
        except TypeError:
            noError = False
            print("Oops! That was not a valid number. Try again...")

        #Append next into data list rows ONLY when all data has been filled
        if(noError):
            data.append(next)
            print("Line-added")
        else:
            print("nothing added")

#check if output.csv already exsists
file_path = "output.csv"
file_exists = os.path.exists(file_path)

with open(file_path, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    #Write the header ONLY if the file does not exist yet
    if not file_exists:
        writer.writerow(header)

    #Append the rest of the data rows
    writer.writerows(data)
