# importing modules and packages
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
from Semester26_Model import  predict_price
import matplotlib.patheffects as pe   

#draws the bergen map
def draw_the_map():
    #displays image, and cla clears?
    ax_map.cla()
    ax_map.imshow(img, extent=(0, 100, 0, 100), aspect='auto')

    #sets x,y as the marked point
    x,y = marked_point

    print(f"marked_point: {marked_point}")
    if marked_point == (0, 0):
        return

    m2_price:float = predict_price(x, y, m2, house_type, standard_type) / m2
    price = f"{round(m2_price * 1000, -2):,.0f}"

    m2list = [50,100,150,200]
    price_m2 = [predict_price(x, y,  _m2, house_type, standard_type)/_m2 for _m2 in m2list]
    #tidligere fargekode(beholder,hvis noe skjer)
        # m2_price = totalpris / 1000 rounded
        # cursor_color decides color displayed on text and marker
        #if m2_price >= 70.00:
            #cursor_color = 'red'
        #elif m2_price >= 55.00:
            #cursor_color = 'yellow'
        #else:
            #cursor_color = 'green'

        #sets marker on x, y and color
        #ax_map.scatter(x, y, marker='+', c=cursor_color, s=200)
        #ax_map.text(x + 3, y - 1, price, color=cursor_color, fontsize=15)
    #slutt av tidligere kode

    #farge for chart
    bar_color = standard_farge[standard_type]
    ax_map.scatter(x, y, marker='+', c=bar_color, s=200)
    ax_map.text(x + 3, y - 1, price, color=bar_color, fontsize=15)

    ax_history.cla()
    #lager chart
    ax_history.bar(m2list, price_m2, color=bar_color, width=5)
    
    #pris per m2 for huspå100 m2
    ref_price = price_m2[m2list.index(100)]
    ax_history.axhline(ref_price, color='black', linestyle='--', linewidth=1, label=f"100 m2: {round(ref_price * 1000, -2):,.0f}")

    #grid, for oppgaven
    ax_history.set_axisbelow(True)
    ax_history.grid(axis='y', linestyle=':', alpha=0.6)
    

    ax_history.set_xticks(m2list)
    ax_history.set_xlabel("størrelse (m2)")
    ax_history.set_ylabel("pris per m2")
     
    ax_history.legend()

    #apply changes to existingmap
    plt.draw()

#activates on click of the map
def on_click_map(event) :
    global marked_point
    #if click is off the map it wont register
    if event.inaxes != ax_map:
        return

    #set
    marked_point = (event.xdata, event.ydata)
    draw_the_map()
    return

#changes house type form enebolig, Rekke, Leiglighet
def on_house_type(key):
    global house_type
    house_type = house_types[key]
    draw_the_map()

#changes the standerds form: Dårlig, God, Meget god, Luksus
def on_standard(key):
    global standard_type
    standard_type = standard_types[key]
    draw_the_map()

#definde housetypes, enebloig as the number 1, rekke as 2 and leilhet as 3
house_types = {
    'Enebolig': 1,
    'Rekke': 2,
    'Leilighet': 3
}

#defines standertypes as numbers also
standard_types = {
    'Dårlig': 1,
    'God': 2,
    'Meget God': 3,
    'Luksus': 4
}
standard_farge = {
    1:'red',
    2:'gold',
    3:'green',
    4:'blue',
}

#Set the defualt types for first run
house_type = 1
standard_type = 1
m2 = 100
marked_point = (43,57)

# Create the figures
fig = plt.figure(figsize=(8.0, 8.0),facecolor='lightgray')  # type: ignore[arg-type]
fig.suptitle("Hus priser Bergen (per m2)", fontsize=20, y=0.95)

ax_map = fig.add_axes((0.4, 0.05, 0.50, .85))
ax_radio_house_type = fig.add_axes((0.05, 0.75, 0.30, .15))
ax_radio_standard = fig.add_axes((0.05, 0.57, 0.30, .15))
ax_history = fig.add_axes((0.05, 0.05, 0.30, .50))
ax_radio_house_type.set_facecolor('lightgray')
ax_radio_standard.set_facecolor('lightgray')

radio_button_category = RadioButtons(ax_radio_house_type, list(house_types.keys()))
radio_button_standard = RadioButtons(ax_radio_standard, list(standard_types.keys()))
radio_button_category.on_clicked(on_house_type)
radio_button_standard.on_clicked(on_standard)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0) # Adjust the figure to fit the image
ax_map.margins(x=0.01, y=0.01)  # Adjust x and y margins
img = mpimg.imread('Semester26_Bergen.jpg')
ax_map.imshow(img, aspect='auto')

#draws the map with defualts for first run
draw_the_map()
plt.connect('button_press_event', on_click_map)

#opens the program, and waita on input
plt.show()


