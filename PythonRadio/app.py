import customtkinter
from pyradios import RadioBrowser
import vlc
import time


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

rb = RadioBrowser()

def searchForStation(stationName):
    info = rb.search(name=stationName, name_exact=False)
    radio_name = info[0] # Number corresponds with country

    radioNameLabel = customtkinter.CTkLabel(master=frame, text="Staion name: " + radio_name["name"])
    radioNameLabel.pack(pady=12, padx=10)

    radioCountryLabel = customtkinter.CTkLabel(master=frame, text="Country of origin: " + radio_name["country"], wraplength=290)
    radioCountryLabel.pack(pady=12, padx=10)

    url = radio_name['url']

    #define VLC instance
    instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

    #Define VLC player
    player=instance.media_player_new()

    #Define VLC media
    media=instance.media_new(url)

    #Set player media
    player.set_media(media)

    #Play the media
    player.play()
    
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand = True)

label = customtkinter.CTkLabel(master=frame, text="Enter the name of a radio station")
label.pack(pady=12, padx=10)

stationNameInput = customtkinter.CTkEntry(master=frame, placeholder_text=" ")
stationNameInput.pack(pady = 12, padx = 10)

button = customtkinter.CTkButton(master=frame, text="Search", command=lambda: searchForStation(stationNameInput.get()))
button.pack(pady = 12, padx = 10)

root.mainloop()