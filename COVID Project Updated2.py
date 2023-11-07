#!/usr/bin/env python
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

messagebox.showinfo(title="Loading...", message="The COVID-19 analysis program is running, please give it time to load...")

import ctypes, math, requests, io, webbrowser
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from io import BytesIO

excluded = ["OWID_ENG", "OWID_EUN", "OWID_HIC", "HKG", "OWID_LIC", "OWID_LMC", "OWID_NIR", "OWID_SCT", "TWN", "TKM", "OWID_UMC"]
dfurl = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
dfdownload = requests.get(dfurl).content
df = pd.read_csv(io.StringIO(dfdownload.decode('utf-8')))
df = df[~df["iso_code"].isin(excluded)]

gfurl = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
gfdownload = requests.get(gfurl).content
gf = pd.read_csv(io.StringIO(gfdownload.decode('utf-8')))
gf = gf[~gf["iso_code"].isin(excluded)]

def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier

def load_image(url, size):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    img = Image.open(image_data)
    img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def gotolocationselect():
    global row, datalocation, location
    datalocation = location.get()
    row = df[df["location"] == datalocation].index[0]
    datadisplay_frame.pack_forget()
    graph_frame.pack_forget()
    locationselect_frame.pack(fill=BOTH, expand=True)

def gotodata():
    global row, datalocation, location, dataloctitle,info
    datalocation = location.get()
    row = df[df["location"] == datalocation].index[0]
    dataloctitle.config(text=f"COVID Data for {datalocation}")
    info.delete(0, END)
    for column in df:
        if "smokers" in column or "age" in column:
            del df[column]
        else:
            temp = str(column).replace("_"," ").title()
            temp = temp.replace("Gdp","GDP")
            temp = temp.replace("Icu","ICU")
            temp = temp.replace("Hosp","Hospital")
            temp = temp.replace("Cardiovasc","Cardiovascular")
            temp = temp.replace("Capita","Capital")
            temp = temp.replace("Iso","ISO")
            if str(df[column][row]) != "nan":
                info.insert(END, f"{temp}: {df[column][row]}")
    locationselect_frame.pack_forget()
    graph_frame.pack_forget()
    datadisplay_frame.pack(fill=BOTH, expand=True)

def gotograph():
    global graphdata, dates, total_cases, subplt
    locationselect_frame.pack_forget()
    datadisplay_frame.pack_forget()
    subplt.clear()

    graphdata = gf[gf["location"] == datalocation]
    dates = pd.to_datetime(graphdata["date"])
    total_cases = graphdata["total_cases"]
    max_total_cases = total_cases.max()

    subplt.bar(dates, total_cases, width=5, color='b', alpha=0.7)
    subplt.set_title(f"Total COVID-19 Cases in {datalocation}")
    subplt.set_xlabel("Date")
    subplt.set_ylabel("Total Cases")
    subplt.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
    subplt.xaxis.set_major_locator(mdates.DayLocator(interval=50))
    if max_total_cases/1e6 <= 5:
        y_ticks = [0, round_up(max_total_cases,-3)*.25, round_up(max_total_cases,-3)*.5, round_up(max_total_cases,-3)*.75, round_up(max_total_cases,-3)]
        y_tick_labels = ["0M", f"{int(round_up(max_total_cases,-3)*.25/1e3)}K", f"{int(round_up(max_total_cases,-3)*.5/1e3)}K", f"{int(round_up(max_total_cases,-3)*.75/1e3)}K", f"{int(round_up(max_total_cases,-3)/1e3)}K"]
    else:
        y_ticks = [0, round_up(max_total_cases,-6)*.25, round_up(max_total_cases,-6)*.5, round_up(max_total_cases,-6)*.75, round_up(max_total_cases,-6)]
        y_tick_labels = ["0M", f"{int(round_up(max_total_cases,-6)*.25/1e6)}M", f"{int(round_up(max_total_cases,-6)*.5/1e6)}M", f"{int(round_up(max_total_cases,-6)*.75/1e6)}M", f"{int(round_up(max_total_cases,-6)/1e6)}M"]
    subplt.set_yticks(y_ticks)
    subplt.set_yticklabels(y_tick_labels)
    subplt.tick_params(axis='x', rotation=45)

    subplt.grid(False)
    fig.tight_layout()
    canvas.draw()
    graph_frame.pack(fill=BOTH, expand=True)

master = Tk()
master.title("COVID-19 Data Analysis")
master.geometry("1500x600")
locationselect_frame = Frame(master)
datadisplay_frame = Frame(master)
graph_frame = Frame(master)
#backarrow_image = load_image("https://lh3.googleusercontent.com/drive-viewer/AITFw-zF4hMnp311E8TDp9wpc9v12Aj---a545znq0gboPCuMs-NCUlZl4dmXfWgaCF1l2Sv_DPhiykiA0EsZQHiyT7rnFYEDA=s2560",(32,32))
#graph_image = load_image("https://lh3.googleusercontent.com/drive-viewer/AITFw-zuK9Ct2lq-gO2mQVSOXFNa1wLyiCFHTA-_RJMHev9miQVJSQVIoeiZsChx5BHBm60WiIEkXblxjv0813NOrcHxlvOwPw=s2560",(32,32))
#location_image = load_image("https://lh3.googleusercontent.com/drive-viewer/AITFw-xN-7ObeLP6KBLMj7T7FMFlX-d_izXIR908OdUbwkVz-u9L0gNd6ukm7zuvh3toLeAucbUv6V58wK4jbRZR2hvy5sXmMA=s2560",(32,32))


#Location Select Frame
locationselect_frame.pack(fill=BOTH, expand=True)
location = StringVar(locationselect_frame)
location.set(df["location"][0])
Label(locationselect_frame,text="Location Select",font=("Comfortaa",50,"bold")).pack()
ttk.Combobox(locationselect_frame, textvariable=location, values=df["location"].to_list(), state="readonly",width=50,font=("Comfortaa",15,"bold")).pack()
Label(locationselect_frame,text="Last Updated on (yyyy-mm-dd): {}".format(df["last_updated_date"][0]),font=("Comfortaa",15,"bold")).pack()
Button(locationselect_frame,text="Choose",font=("Comfortaa",25,"bold"),fg="green",command=gotodata).pack()
Label(locationselect_frame,text="The special additions in the list are: Africa, Asia, Europe, North America, Oceania, South America, and World (data of the whole world).",font=("Comfortaa",16,"bold"),wraplength=1300).pack(side="bottom")
Label(locationselect_frame,text="England, Hong Kong, Northern Ireland, Scotland, Taiwan, and Turkmenistan are currently not available.",font=("Comfortaa",16,"bold"),wraplength=1300).pack(side="bottom")
datalocation = location.get()


#Data Display Frame
ddftoolbar = Frame(datadisplay_frame)
ddftoolbar.pack(fill=X)
#, image=backarrow_image
Button(ddftoolbar, text="Back", compound="left", font=("Comfortaa", 12, "bold"), command=gotolocationselect, padx=10).pack(side=LEFT, padx=10, pady=0)
#, image=graph_image
Button(ddftoolbar, text="View Data Graph", compound="left", font=("Comfortaa", 12, "bold"), command=gotograph,padx=10).pack(side=LEFT, padx=10, pady=0)

row = df[df["location"] == datalocation].index[0]
dataloctitle = Label(datadisplay_frame,text=f"COVID Data for {datalocation}",font=("Comfortaa",50,"bold"))
dataloctitle.pack(pady=0)
scrollbar = Scrollbar(datadisplay_frame)
scrollbar.pack(side=RIGHT,fill=Y)
info = Listbox(datadisplay_frame,yscrollcommand=scrollbar.set,font=("Comfortaa",12,"bold"),borderwidth=0,bg=master["bg"],justify=CENTER)

info.pack(fill=BOTH,expand=True)
link = Label(datadisplay_frame,text="Info from: https://github.com/owid/covid-19-data",font=("Comfortaa",15,"bold"),borderwidth=0,bg=master["bg"],justify=CENTER,fg="blue",cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e:
webbrowser.open("https://github.com/owid/covid-19-data"))
scrollbar.config(command=info.yview)


#Graph Display Frame
gftoolbar = Frame(graph_frame)
gftoolbar.pack(fill=X)
#, image=backarrow_image
Button(gftoolbar, text="Back", compound="left", font=("Comfortaa", 12, "bold"), command=gotodata, padx=10).pack(side=LEFT, padx=10, pady=0)
#, image=location_image
Button(gftoolbar, text="Go to Location Select", compound="left", font=("Comfortaa", 12, "bold"), command=gotolocationselect,padx=10).pack(side=LEFT, padx=10, pady=0)

graphdata = gf[gf["location"] == datalocation]
dates = pd.to_datetime(graphdata["date"])
total_cases = graphdata["total_cases"]
max_total_cases = total_cases.max()
fig = Figure(figsize=(12,6), dpi=100)
subplt = fig.add_subplot(111)
subplt.bar(dates, total_cases, width=5, color='b', alpha=0.7)
subplt.set_title(f"Total COVID-19 Cases in {datalocation}")
subplt.set_xlabel("Date")
subplt.set_ylabel("Total Cases")
subplt.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
subplt.xaxis.set_major_locator(mdates.DayLocator(interval=50))
if max_total_cases/1e6 <= 5:
    y_ticks = [0, round_up(max_total_cases,-3)*.25, round_up(max_total_cases,-3)*.5, round_up(max_total_cases,-3)*.75, round_up(max_total_cases,-3)]
    y_tick_labels = ["0M", f"{int(round_up(max_total_cases,-3)*.25/1e3)}K", f"{int(round_up(max_total_cases,-3)*.5/1e3)}K", f"{int(round_up(max_total_cases,-3)*.75/1e3)}K", f"{int(round_up(max_total_cases,-3)/1e3)}K"]
else:
    y_ticks = [0, round_up(max_total_cases,-6)*.25, round_up(max_total_cases,-6)*.5, round_up(max_total_cases,-6)*.75, round_up(max_total_cases,-6)]
    y_tick_labels = ["0M", f"{int(round_up(max_total_cases,-6)*.25/1e6)}M", f"{int(round_up(max_total_cases,-6)*.5/1e6)}M", f"{int(round_up(max_total_cases,-6)*.75/1e6)}M", f"{int(round_up(max_total_cases,-6)/1e6)}M"]
subplt.set_yticks(y_ticks)
subplt.set_yticklabels(y_tick_labels)
subplt.tick_params(axis='x', rotation=45)

subplt.grid(False)
fig.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=BOTH, expand=True)

mainloop()