# importing modules and packages
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
from Semester26_Model import  predict_price as predict_price_mod1
from Semester26_finnoModel import predict_price as predict_price_mod2

# draws the bergen map
def draw_the_map():
    # displays image, and cla clears?
    ax_map.cla()
    ax_map.imshow(img, extent=(0, 100, 0, 100), aspect='auto')

    # sets x,y as the marked point
    x,y = marked_point

    print(f"marked_point: {marked_point}")
    if marked_point == (0, 0):
        return
    if mod_type == 1:
        m2_price:float = predict_price_mod1(x, y, m2, house_type, standard_type) / m2
        price = f"{round(m2_price * 1000, -2):,.0f}"
        m2list = [50,100,150,200]
        price_m2 = [predict_price_mod1(x, y,  _m2, house_type, standard_type)/_m2 for _m2 in m2list]
    elif mod_type == 2:
        m2_price:float = predict_price_mod2(x, y, m2, house_type, standard_type) / m2
        price = f"{round(m2_price * 1000, -2):,.0f}"
        m2list = [50,100,150,200]
        price_m2 = [predict_price_mod2(x, y,  _m2, house_type, standard_type)/_m2 for _m2 in m2list]

    # m2_price = totalpris / 1000 rounded
    # cursor_color decides color displayed on marker
    # tekst_color decides clor displayed by tekst
    if m2_price >= 70.00:
        tekst_color = 'orangered'
    elif m2_price >= 55.00:
        tekst_color = 'yellow'
    else:
        tekst_color = 'lime'

    # Find better colors later
    if house_type == 1:
        cursor_color = 'blue'
    elif house_type == 2:
        cursor_color = 'darkviolet'
    else:
        cursor_color = 'indigo'

    # Sets marker on x, y and color
    ax_map.scatter(x, y, marker='+', c=cursor_color, s=200)
    ax_map.text(x + 3, y - 1, price, color=tekst_color, fontsize=15,  bbox=dict(
        facecolor='black',      
        alpha=0.5,            
        edgecolor='none',     
        boxstyle='round,pad=0.2'
    ))
    ax_history.cla()

    # Makes the chart
    ax_history.bar(m2list, price_m2, color=cursor_color, width=5)
    ax_history.legend(["pris per m2"])

    # Apply changes to existingmap
    plt.draw()

# Activates on click of the map
def on_click_map(event) :
    global marked_point
    #if click is off the map it wont register
    if event.inaxes != ax_map:
        return

    #set
    marked_point = (event.xdata, event.ydata)
    draw_the_map()
    return

# Changes house type form: Enebolig, Rekke, Leiglighet
def on_house_type(key):
    global house_type
    house_type = house_types[key]
    draw_the_map()

# Changes the standerds form: Dårlig, God, Meget god, Luksus
def on_standard(key):
    global standard_type
    standard_type = standard_types[key]
    draw_the_map()

# Changes the model type form: mod1 (the og), mod2 (Finno model)
def on_mod_type(key):
    global mod_type
    mod_type = mod_types[key]
    print(f"Mod type changed to: {mod_type}")
    draw_the_map()

# Definde housetypes, Enebloig as the number 1, Rekke as 2 and Leilhet as 3
house_types = {
    'Enebolig': 1,
    'Rekke': 2,
    'Leilighet': 3
}

# Defines standertypes as numbers 1-4 also
standard_types = {
    'Dårlig': 1,
    'God': 2,
    'Meget God': 3,
    'Luksus': 4
}

# Defines the diffrent model types as numbers 1-2
mod_types = {
    'mod1': 1,
    'mod2': 2
}

# Set the defualt types for first run
house_type = 1
standard_type = 1
mod_type = 1
mod_type = 1
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

# Added axis for model buttons at the top right
ax_radio_mod = fig.add_axes((0.75, 0.88, 0.15, 0.08))
ax_radio_mod.set_facecolor('lightgray')

radio_button_category = RadioButtons(ax_radio_house_type, list(house_types.keys()))
radio_button_standard = RadioButtons(ax_radio_standard, list(standard_types.keys()))
radio_button_mod = RadioButtons(ax_radio_mod, list(mod_types.keys()))

radio_button_category.on_clicked(on_house_type)
radio_button_standard.on_clicked(on_standard)
radio_button_mod.on_clicked(on_mod_type)

fig.subplots_adjust(left=0, right=1, top=1, bottom=0) # Adjust the figure to fit the image
ax_map.margins(x=0.01, y=0.01)  # Adjust x and y margins
img = mpimg.imread('Semester26_Bergen.jpg')
ax_map.imshow(img, aspect='auto')

#draws the map with defualts for first run
draw_the_map()
plt.connect('button_press_event', on_click_map)

#opens the program, and waita on input
plt.show()