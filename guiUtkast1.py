import tkinter as tk

# Variabler som gjenbrukes i gui
bredde = 0

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
    canvas.create_polygon(points, smooth=True, **kwargs)

# Create the main window
root = tk.Tk()
root.title("Haugesund Gjestebrygge")


# Create a canvas with full HD size (1920x1080)
canvas = tk.Canvas(root, width=1920, height=1080, bg='light grey')
canvas.pack()

draw_rounded_rectangle(canvas, 619, 50, 1300, 155, 20, fill='gray12', outline='gray22', width=2) # Title box

label = tk.Label(root, text="Haugesund Gjestebrygge", bg='gray12', fg='azure', font=("Calibri", 46))
canvas.create_window(643, 60, anchor='nw', window=label)

# Draw a rounded rectangle for 'hav'
draw_rounded_rectangle(canvas, 99, 200, 1819, 980, 20, fill='#9ACBFF', outline='gray22', width=25)



# Utstikkere
draw_rounded_rectangle(canvas, 205, 595, 220, 750, 10, fill='gray46', outline='gray12', width=0)
draw_rounded_rectangle(canvas, 475, 595, 490, 750, 10, fill='gray46', outline='gray12', width=0)
draw_rounded_rectangle(canvas, 745, 595, 760, 750, 10, fill='gray46', outline='gray12', width=0)
draw_rounded_rectangle(canvas, 1015, 595, 1030, 750, 10, fill='gray46', outline='gray12', width=0)
draw_rounded_rectangle(canvas, 1285,595, 1300, 750, 10, fill='gray46', outline='gray12', width=0)

# Draw a rounded rectangle for 'brygge'
draw_rounded_rectangle(canvas, 200, 500, 1655, 600, 15, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1555, 500, 1655, 968, 15, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1554, 501, 1560, 599, 0, fill='gray76', outline='gray76', width=0)

# Rektangler for øvre store p-plasser
guiP1 = draw_rounded_rectangle(canvas, 330, 330, 830, 480, 60, fill='#D4EAFF', outline='#D4EAFF', width=3)
draw_rounded_rectangle(canvas, 1000, 330, 1500, 480, 60, fill='#D4EAFF', outline='#D4EAFF', width=3)

# Nedre P-plasser
draw_rounded_rectangle(canvas, 230, 610, 335, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 360, 610, 465, 830, 65, fill='#2EC729', outline='#2EC729', width=bredde)
draw_rounded_rectangle(canvas, 500, 610, 605, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 630, 610, 735, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 770, 610, 875, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 900, 610, 1005, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
guiP2 = draw_rounded_rectangle(canvas, 1040, 610, 1145, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 1170, 610, 1275, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 1310, 610, 1415, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)
draw_rounded_rectangle(canvas, 1440, 610, 1545, 830, 65, fill='#D4EAFF', outline='#D4EAFF', width=bredde)

# Create and place the buttons
button1 = tk.Button(canvas, text="", bg='#D4EAFF', activebackground='#D0E5FA', bd=0, command=lambda: function("input"))
button1_window = canvas.create_window(340, 340, anchor='nw', window=button1, width=480, height=130)
button2 = tk.Button(canvas, text="", bg='#D4EAFF', activebackground='#D0E5FA', bd=0, command=lambda: function("input"))
button2_window = canvas.create_window(1050, 620, anchor='nw', window=button2, width=85, height=200)


def function(verdi1):
    print(verdi1)
    ankomstP1()
    ankomstP2()

def ankomstP1():
    canvas.itemconfig(guiP1, fill='yellow')
    button1.config(bg='yellow')
def ankomstP2():
    canvas.itemconfig(guiP2, fill='yellow')
    button2.config(bg='yellow')



# Start the Tkinter main loop
root.mainloop()
