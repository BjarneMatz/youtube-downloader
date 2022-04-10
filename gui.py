import tkinter as tk
import webbrowser
from tkinter import filedialog
from tkinter import ttk as ttk

import downloader


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        # setting up window
        self.title("DD YouTube Downloader")
        self.resizable(False, False)
        ttk.Style().theme_use("clam")

        # setting up frames
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack()
        self.inputframe = ttk.Frame(self.mainframe)
        self.inputframe.grid(column=0, row=1, pady=20)
        self.tutorialframe = ttk.Frame(self.mainframe)
        self.tutorialframe.grid(column=1, row=1, pady=20, padx=50)

        # youtube link entry box
        self.linkentry = ttk.Entry(self.mainframe, width=100)
        self.linkentry.grid(column=0, row=0, columnspan=2)
        self.linkentry.focus()

        # optional feature check boxes
        self.prefix = tk.IntVar()
        ttk.Checkbutton(self.inputframe, text="Setze YT-Kanal als Prefix", variable=self.prefix).pack(anchor="nw")

        self.audioonly = tk.IntVar()
        ttk.Checkbutton(self.inputframe, text="Nur Audio herunterladen", variable=self.audioonly).pack(anchor="nw")

        self.playlistPrefix = tk.IntVar()
        ttk.Checkbutton(self.inputframe, text="Playlist & Channel Ordner mit Prefix versehen",
                        variable=self.playlistPrefix).pack(anchor="nw")

        # how to use / quick manual
        ttk.Label(self.tutorialframe,
                  text="1. YT-Link in Textbox einfügen. Kanal-, Playlist- oder Videolinks werden akzeptiert.").pack(
            anchor="nw")
        ttk.Label(self.tutorialframe,
                  text='2. Spezielle Funktionen wie z.B. "Nur Audio herunterladen" auswählen.').pack(anchor="nw")
        ttk.Label(self.tutorialframe,
                  text="3. Download Knopf drücken und Download-Ordner auswählen.").pack(anchor="nw")

        ttk.Button(self.mainframe, text="Download", command=self.getpath, width=100).grid(row=2, column=0, columnspan=2,
                                                                                          pady=10)

        # main tkinter loop
        self.mainloop()

    def getpath(self):
        """function gets path for the download process and hands over needed parameters to download module"""

        # ask user to which path to download to
        self.path = tk.filedialog.askdirectory()

        # hand over parameters to download module
        x = downloader.VideoDownloader(self.linkentry.get(), self.path, self.audioonly.get(), self.prefix.get(),
                                       self.playlistPrefix.get)
        # after download is finished: open download folder
        webbrowser.open(self.path)


if __name__ == "__main__":
    app = Gui()
