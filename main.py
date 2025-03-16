import tkinter as tk
import random
import string
import time
import subprocess
import webbrowser as wb
from PIL import ImageTk, Image

def open_website():
    wb.open("https://cornhub.website/")


STRING_LENGTH = 100  # Length of the random string
popups = [
    ["YOU JUST WON $1000000 DOLLARS", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/sunset.png"],
    ["YOU ARE THE 1000000 VISITOR", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/sunset.png"],
    ["YOU JUST WON A FREE IPHONE", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/smiley.png"],
    ["YOU JUST WON A FREE MACBOOK", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/smiley.png"],
    ["YOU JUST WON A FREE CAR", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/smiley.png"],
    ["YOUR COMPUTER HAS A VIRUS!", "CLICK HERE TO FIX IT", "./images/hacer.png"],
    ["YOUR COMPUTER HAS BEEN HACKED!", "CLICK HERE TO FIX IT", "./images/hacer.png"],
    ["YOU JUST WON A FREE TRIP TO HAWAII", "CLICK HERE TO CLAIM YOUR PRIZE", "./images/sunset.png"],
]
words = [
    # Short uncommon words (3-5 letters)
    "quid", "zarf", "wisp", "jape", "mote", "pyre", "whet", "glib", "tome", "lilt", 
    "nix", "ruck", "vex", "cusp", "yore", "fawn", "serf", "lurk", "bask", "zeal", 
    "smog", "pith", "limn", "scry", "husk", "brim", "chum", "whim", "grit", "brio",

    # Medium uncommon words (6-8 letters)
    "gloam", "mirth", "squib", "brogue", "lollop", "tenebr", "choler", "gadfly", "sachet", "votary",
    "purvey", "sallow", "quahog", "cairns", "frisson", "dormer", "shrike", "megrim", "turgid", "warren",
    "charnel", "lissome", "kith", "dreich", "spangle", "flotsam", "jetsam", "whorl", "sward", "askance",

    # Long uncommon words (9+ letters)
    "ebullience", "gloaming", "chiaroscuro", "ephemeral", "sesquipedalian", "threnody", "sibilance", "perdition", "obfuscate", "ineluctable",
    "vexillology", "lambent", "lugubrious", "mellifluous", "redolent", "cynosure", "halcyon", "cachinnate", "petrichor", "aestivate",
    "apoplectic", "catafalque", "susurration", "recondite", "fulminate", "uxorious", "antediluvian", "perspicacious", "ostensible", "rhododendron",
    "absquatulate", "prevaricate", "oneirology", "effulgent", "quixotic", "mendacity", "insouciant", "chthonic", "opprobrium", "surreptitious"
]


brightness = 25

def generate_random_string():
    return ' '.join(random.sample(words, 10))

def start_typing():
    global start_time, target_string, typed_string
    target_string = generate_random_string()
    typed_string = ""
    target_label.config(text=target_string)
    entry_var.set("")
    start_time = time.time()
    result_label.config(text="")

def check_typing(event):
    global typed_string
    typed_string = entry_var.get()
    if typed_string == target_string:
        elapsed_time = time.time() - start_time
        wpm = (len(target_string) / 5) / (elapsed_time / 60)  # Estimate WPM
        result_label.config(text=f"Completed! Speed: {wpm:.2f} WPM", fg="green")
    elif not target_string.startswith(typed_string):
        result_label.config(text="Error! Restarting...", fg="red")
        brightness = 100
        subprocess.run(f"powershell (Get-WmiObject -namespace root/wmi -class WmiMonitorBrightnessMethods).wmisetbrightness(1,{brightness})")
        brightness = 25
        start_typing()


def update():
    global brightness
    typed_string = entry_var.get()
    elapsed_time = time.time() - start_time
    wpm = 0 if elapsed_time == 0 else (len(typed_string) / 5) / (elapsed_time / 60)  # Estimate WPM
    # brightness = max(0, min(100, int(wpm)))
    # print(wpm, brightness)
    if wpm < 10:
        brightness -= 5
    if wpm < 20:
        [title, button_text, img] = random.choice(popups)
        popup = tk.Tk()
        popup.title(title)
        popup.geometry("350x200")
        popup.configure(bg="red")
        # image = Image.open(img)
        # image2 = ImageTk.PhotoImage(image)
        # imglabel = tk.Label(popup, image=image2)
        # imglabel.pack()
        label = tk.Label(popup, text=title)
        label.pack(pady=10)
        button = tk.Button(popup, text=button_text, command=open_website)
        button.pack(pady=10)
    if wpm > 40:
        brightness += 1
        open_website()
    brightness = max(0, min(100, int(brightness)))
    subprocess.run(f"powershell (Get-WmiObject -namespace root/wmi -class WmiMonitorBrightnessMethods).wmisetbrightness(1,{brightness})")
    root.after(1000, update)

# GUI Setup
root = tk.Tk()
root.title("Typing Practice")
root.geometry("1920x1080")

instruction_label = tk.Label(root, text="Type the following string:")
instruction_label.pack()

target_label = tk.Label(root, text="", font=("Courier", 14, "bold"))
target_label.pack()

entry_var = tk.StringVar()
typing_entry = tk.Entry(root, textvariable=entry_var, font=("Courier", 14))
typing_entry.pack()
typing_entry.bind("<KeyRelease>", check_typing)

type_button = tk.Button(root, text="Start", command=start_typing)
type_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()


start_typing()
update()
root.mainloop()

