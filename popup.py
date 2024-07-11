import tkinter as tk
from PIL import Image, ImageTk

# Function to draw a rounded rectangle
def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
        x1 + radius, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)
def bigboat_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        #x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        #x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
        x1 + radius, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Function to draw a rounded rectangle
def draw_boat_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        #x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        #x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
        x1 + radius, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Create the main window
root = tk.Tk()
root.title("Båtdeteksjon")

# Create a canvas with full HD size (1920x1080)
canvas = tk.Canvas(root, width=1920, height=1080, bg='light grey')
canvas.pack()


# Draw main components
draw_rounded_rectangle(canvas, 510, 50, 1390, 165, 20, fill='gray12', outline='gray22', width=2)
label = tk.Label(root, text="Haugesund Gjestekai Oversikt", bg='gray12', fg='azure', font=("Calibri", 52))
canvas.create_window(530, 60, anchor='nw', window=label)
hav =draw_rounded_rectangle(canvas, 99, 200, 1819, 980, 20, fill='DeepSkyBlue2', outline='gray22', width=25)

image = Image.open("ocean.jpg")
image = image.resize((1800 - 105, 960 - 202))
photo = ImageTk.PhotoImage(image)

# Create an image item on the canvas to cover 'hav'
canvas.create_image(112, 212, anchor='nw', image=photo)




# Utstikkere
utstikkere_pos = [(205, 595, 220, 750), (475, 595, 490, 750), (745, 595, 760, 750), (1015, 595, 1030, 750), (1285, 595, 1300, 750)]
for pos in utstikkere_pos:
    draw_rounded_rectangle(canvas, *pos, 10, fill='gray46', outline='gray46', width=0)

# Brygge
draw_rounded_rectangle(canvas, 190, 500, 1655, 600, 56, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1555, 500, 1655, 968, 56, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1554, 501, 1580, 599, 0, fill='gray76', outline='gray76', width=0)

# Øvre store p-plasser
"""


rect1 = bigboat_rectangle(canvas, 330, 330, 830, 480, 77, fill='white', outline='white', width=3) # P1!
rect2 = bigboat_rectangle(canvas, 1000, 330, 1500, 480, 77, fill='white', outline='white', width=3)

canvas.create_oval(1440, 610, 1545, 830, fill='red', outline='red', width=2)
canvas.create_oval(1440, 610, 1545, 830, fill='red', outline='red', width=2)



rect3 = draw_boat_rectangle(canvas, 230, 610, 335, 850, 56, fill='snow2', outline='snow2', width=3)
rect4 = draw_boat_rectangle(canvas, 360, 610, 465, 850, 56, fill='snow2', outline='snow2', width=3)
rect5 = draw_boat_rectangle(canvas, 500, 610, 605, 850, 56, fill='gray90', outline='gray90', width=3)
rect6 = draw_boat_rectangle(canvas, 630, 610, 735, 850, 56, fill='gray90', outline='gray90', width=3)
rect7 = draw_boat_rectangle(canvas, 770, 610, 875, 850, 56, fill='white', outline='white', width=3)
rect8 = draw_boat_rectangle(canvas, 900, 610, 1005, 850, 56, fill='white', outline='white', width=3)
rect9 = draw_boat_rectangle(canvas, 1040, 610, 1145, 850, 56, fill='white', outline='white', width=3) # P2!
rect10 = draw_boat_rectangle(canvas, 1170, 610, 1275, 850, 56, fill='white', outline='white', width=3)
rect11 = draw_boat_rectangle(canvas, 1310, 610, 1415, 850, 56, fill='white', outline='white', width=3)
#rect12 = draw_rounded_rectangle(canvas, 1440, 610, 1545, 830, 65, fill='white', outline='white', width=3)
"""


boat1= canvas.create_oval(280, 330, 780, 480, fill='', outline='', width=2) #P1
boat2= canvas.create_oval(1020, 330, 1520, 480, fill='', outline='', width=2)

boat3 = canvas.create_oval(230, 610, 335, 850, fill='', outline='', width=2)
boat4 = canvas.create_oval(360, 610, 465, 850, fill='', outline='', width=2)
boat5 = canvas.create_oval(500, 610, 605, 850, fill='', outline='', width=2)
boat6 = canvas.create_oval(630, 610, 735, 850, fill='', outline='', width=2)
boat7 = canvas.create_oval(770, 610, 875, 850, fill='', outline='', width=2)
boat8 = canvas.create_oval(900, 610, 1005, 850, fill='', outline='', width=2)
boat9 = canvas.create_oval(1040, 610, 1145, 850, fill='', outline='', width=2) #P2
boat10 = canvas.create_oval(1170, 610, 1275, 850, fill='', outline='', width=2)
boat11 = canvas.create_oval(1310, 610, 1415, 850, fill='', outline='', width=2)
boat12 = canvas.create_oval(1440, 610, 1545, 850, fill='', outline='', width=2)

# Create and place the buttons
#button1 = tk.Button(canvas, text="", bg=None, activebackground=None, bd=0, highlightthickness=0, command=lambda: display_time("10:00"))
#button1_window = canvas.create_window(340, 340, anchor='nw', window=button1, width=380, height=130)

#button2 = tk.Button(canvas, text="", bg="white", activebackground="gray98", bd=0, command=lambda: display_time("11:30"))
#button2_window = canvas.create_window(1010, 340, anchor='nw', window=button2, width=380, height=130)

#button3 = tk.Button(canvas, text="", bg="white", activebackground="gray98", bd=0, command=lambda: display_time("13:15"))
#button3_window = canvas.create_window(1050, 620, anchor='nw', window=button3, width=85, height=150)



# Label for displaying time
time_label = tk.Label(canvas, text="", font=("Calibri", 20), bg="light gray")
time_label_window = canvas.create_window(120, 140, anchor='nw', window=time_label)

# Function to display time amount
def signal():
    test1 = input()
    if test1=="a":
        canvas.itemconfig(boat9, fill='green2', outline='green2')
        button9 = tk.Button(canvas, text="", bg="green2", activebackground='lime green', bd=0)
        button9_window = canvas.create_window(1053, 656, anchor='nw', window=button9, width=81, height=150)
    test2 = input()
    if test2 == "a":
        canvas.itemconfig(boat9, fill='red', outline='red')
        button9.config(bg='red', activebackground='red2')

signal()

# Start the Tkinter main loop
root.mainloop()