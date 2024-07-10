import tkinter as tk

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

# Create the main window
root = tk.Tk()
root.title("Båtdeteksjon")

# Create a canvas with full HD size (1920x1080)
canvas = tk.Canvas(root, width=1920, height=1080, bg='light grey')
canvas.pack()


# Draw main components
draw_rounded_rectangle(canvas, 780, 50, 1150, 165, 20, fill='gray12', outline='gray22', width=2)
label = tk.Label(root, text="OVERSIKT", bg='gray12', fg='azure', font=("Calibri", 52)).place(x=820, y=60)
draw_rounded_rectangle(canvas, 99, 200, 1819, 980, 20, fill='DeepSkyBlue2', outline='gray22', width=25)

# Utstikkere
utstikkere_pos = [(205, 595, 220, 750), (475, 595, 490, 750), (745, 595, 760, 750), (1015, 595, 1030, 750), (1285, 595, 1300, 750)]
for pos in utstikkere_pos:
    draw_rounded_rectangle(canvas, *pos, 10, fill='gray46', outline='gray46', width=0)

# Brygge
draw_rounded_rectangle(canvas, 200, 500, 1655, 600, 15, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1555, 500, 1655, 968, 15, fill='gray76', outline='gray22', width=2)
draw_rounded_rectangle(canvas, 1554, 501, 1560, 599, 0, fill='gray76', outline='gray76', width=0)

# Øvre store p-plasser
rect1 = draw_rounded_rectangle(canvas, 330, 330, 830, 480, 60, fill='white', outline='white', width=3) # P1!
rect2 = draw_rounded_rectangle(canvas, 1000, 330, 1500, 480, 60, fill='white', outline='white', width=3)

rect3 = draw_rounded_rectangle(canvas, 230, 610, 335, 830, 65, fill='white', outline='white', width=3)
rect4 = draw_rounded_rectangle(canvas, 360, 610, 465, 830, 65, fill='white', outline='white', width=3)
rect5 = draw_rounded_rectangle(canvas, 500, 610, 605, 830, 65, fill='white', outline='white', width=3)
rect6 = draw_rounded_rectangle(canvas, 630, 610, 735, 830, 65, fill='white', outline='white', width=3)
rect7 = draw_rounded_rectangle(canvas, 770, 610, 875, 830, 65, fill='white', outline='white', width=3)
rect8 = draw_rounded_rectangle(canvas, 900, 610, 1005, 830, 65, fill='white', outline='white', width=3)
rect9 = draw_rounded_rectangle(canvas, 1040, 610, 1145, 830, 65, fill='white', outline='white', width=3) # P2!
rect10 = draw_rounded_rectangle(canvas, 1170, 610, 1275, 830, 65, fill='white', outline='white', width=3)
rect11 = draw_rounded_rectangle(canvas, 1310, 610, 1415, 830, 65, fill='white', outline='white', width=3)
rect12 = draw_rounded_rectangle(canvas, 1440, 610, 1545, 830, 65, fill='white', outline='white', width=3)


# Create and place the buttons
button1 = tk.Button(canvas, text="", bg="white", activebackground="gray98", bd=0, command=lambda: display_time("10:00"))
button1_window = canvas.create_window(340, 340, anchor='nw', window=button1, width=480, height=130)

button2 = tk.Button(canvas, text="", bg="white", activebackground="gray98", bd=0, command=lambda: display_time("11:30"))
button2_window = canvas.create_window(1010, 340, anchor='nw', window=button2, width=480, height=130)

button3 = tk.Button(canvas, text="", bg="white", activebackground="gray98", bd=0, command=lambda: display_time("13:15"))
button3_window = canvas.create_window(1050, 620, anchor='nw', window=button3, width=85, height=200)



# Label for displaying time
time_label = tk.Label(canvas, text="", font=("Calibri", 20), bg="light gray")
time_label_window = canvas.create_window(120, 140, anchor='nw', window=time_label)

# Function to display time amount
def display_time(time_amount):
    time_label.config(text=f"Time selected: {time_amount}")
    test = input()
    if test=='a':
        button3.config(bg="green2", activebackground="green3")
        canvas.itemconfig(rect9, fill='green2', outline='green2')

# Start the Tkinter main loop
root.mainloop()