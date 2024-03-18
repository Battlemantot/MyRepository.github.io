import customtkinter as ctk
from pyradios import RadioBrowser
import os
from PIL import Image, ImageTk
import requests
import vlc
from urllib.request import urlopen

import re
import struct
import sys
import urllib.request as urllib2

rb = RadioBrowser()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mountain Radio")
        # self.geometry("700x450")
        self.minsize(290, 450)
        self.maxsize(940, 1000)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left Navigation bar
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        nav_frame_label_bg = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "Images")

        # Set the image at the top of the navigation
        nav_image = ctk.CTkImage(Image.open(
            os.path.join(nav_frame_label_bg, "poster.jpeg")), size=(250, 75))

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Mountain Radio", image=nav_image,
                                                   compound="center", font=ctk.CTkFont(size=30, weight="bold", slant="italic"), text_color="black")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Find Stations",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.favourites_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Favourites",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     anchor="w", command=self.favourites_frame_button_event)
        self.favourites_frame_button.grid(row=2, column=0, sticky="ew")

        self.settings_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.settings_frame_button_event)
        self.settings_frame_button.grid(row=3, column=0, sticky="ew")

        # Theme options menu
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=[
            "Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

        # ___Home frame
        self.home_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=1)

        # Input for radio name
        self.home_radioName_input = ctk.CTkEntry(self.home_frame)
        self.home_radioName_input.insert(ctk.END, "Enter station name")
        self.home_radioName_input.grid(
            row=0, column=1, padx=20, pady=20)
        self.home_radioName_input.bind(
            "<Button-1>", lambda a: self.home_radioName_input.delete(0, ctk.END))

        # --Search button
        self.home_searchButton = ctk.CTkButton(
            self.home_frame, text="Search", compound="right", command=lambda: self.searchForStation(self.home_radioName_input.get()))
        self.home_searchButton.grid(row=0, column=2, padx=0, pady=20)
        
        self.home_stationImage = ctk.CTkLabel(
            self.home_frame, text="Radio image here", image=None)
        self.home_stationImage.grid(row=1, column=2, padx=20, pady=10)

        self.home_stationName = ctk.CTkLabel(
            self.home_frame, text="Station name: ", compound="left")
        self.home_stationName.grid(row=2, column=1, padx=20, pady=10, sticky='w')

        self.home_stationSong = ctk.CTkLabel(
            self.home_frame, text="Current song: ", compound="right")
        self.home_stationSong.grid(row=3, column=1, padx=20, pady=10, sticky='w')

        self.home_stationCountry = ctk.CTkLabel(
            self.home_frame, text="Country: ", compound="right", wraplength=200)
        self.home_stationCountry.grid(row=4, column=1, padx=20, pady=10, sticky='w')

        self.home_startButton = ctk.CTkButton(
            self.home_frame, text="Start", compound="top", command=lambda: player.play())
        self.home_startButton.grid(
            row=6, column=1, padx=0, pady=10, sticky="s")
        
        self.home_favButton = ctk.CTkButton(
            self.home_frame, text="Favourite", compound="top", command=lambda: "")
        self.home_favButton.grid(
            row=6, column=2, padx=0, pady=10, sticky="s")

        self.home_stopButton = ctk.CTkButton(
            self.home_frame, text="Stop", compound="top", command=lambda: player.stop())
        self.home_stopButton.grid(
            row=6, column=3, padx=20, pady=10, sticky="s")

        # Favourites frame
        self.second_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        # Settings frame
        self.third_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    # Functions
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")

        self.favourites_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        self.settings_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def favourites_frame_button_event(self):
        self.select_frame_by_name("frame_2")

    def settings_frame_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    # Radio search Function
    def searchForStation(self, stationName):
        # Get the radio station
        info = rb.search(name=stationName, name_exact=False)
        radio_station = info[0]  # Number corresponds with country
        url = radio_station['url']

        # Prepare to play radio through VLC
        # define VLC instance
        global instance
        instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        # Define VLC player
        global player
        player = instance.media_player_new()
        
        # Define VLC media
        global media
        media = instance.media_new(url)
        # Set player media
        player.set_media(media)
        player.audio_set_volume(50)

        # Display radio station information
        self.home_stationName.configure(
            text="Staion name: " + radio_station["name"])
        self.home_stationCountry.configure(
            text="Country: " + radio_station["country"])
        
        # ALL OF THIS, for the song name
        encoding = 'latin1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
        request = urllib2.Request(url, headers={'Icy-MetaData': 1})  # request metadata
        response = urllib2.urlopen(request)
        print(response.headers, file=sys.stderr)
        metaint = int(response.headers['icy-metaint'])
        
        for _ in range(10): # # title may be empty initially, try several times
            response.read(metaint)  # skip to metadata
            metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
            metadata = response.read(metadata_length).rstrip(b'\0')
            print(metadata, file=sys.stderr)
            # extract title from the metadata
            m = re.search(br"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                if title:
                    break
        self.home_stationSong.configure(text="Current song: " + title.decode(encoding, errors='replace'))
        
        # Set the radio station image
        #URL = radio_station["favicon"]
        #print("URL: " + radio_station["favicon"])
        #u = urlopen(URL)
        #raw_data = u.read()
        #u.close()

        #radio_station_image = ImageTk.PhotoImage(data=raw_data)
        #self.home_stationImage.image = radio_station_image
        #self.home_stationImage.configure(image=Image.open(requests.get(radio_image, stream=True).raw))

        # radioCountryLabel = customtkinter.CTkLabel(
        # master=frame, text="Country of origin: " + radio_name["country"], wraplength=290)
        # radioCountryLabel.pack(pady=5, padx=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
