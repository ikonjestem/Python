import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
apps = []

if os.path.isfile('save.txt'):
    with open('save.txt', 'r') as f:
        tempApps = f.read()
        tempApps = tempApps.split(',')
        apps = [x for x in tempApps if x.strip()]


def addApp():

    for widget in frame.winfo_children():    #po dodaniu kolejneg pliku czysci widoczne sciezki
        widget.destroy()


    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                        filetypes=(("executables","*.exe"),("all files",".")))
    apps.append(filename)
    print(filename)
    for app in apps: #pokazuje sciezke pliku
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()


def runApps(): #otwiera dodany plik
    for app in apps:
        os.startfile(app)


canvas = tk.Canvas(root, height=500, width=500, bg="#263D42")  #tło
canvas.pack()  #odpala tło

frame = tk.Frame(root, bg="white")    #ramka
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

openfile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", 
                    bg="#263D42", command=addApp)
openfile.pack()

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="white",
                     bg="#263D42", command=runApps)
runApps.pack()


for app in apps: #przy uruchmoeiniu pokazuje zapisane w save sciezki
    label = tk.Label(frame, text=app)
    label.pack()

root.mainloop()

with open("save.txt", "w") as f: #zapisuje dodane programy w pliku txt
    for app in apps:
        f.write(app + ',')