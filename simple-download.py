from  pytube import Playlist
from pytube import YouTube
import os
import json

dl_path = r"D:\PC Sync\Musik\Musikbibliothek"

prefix=True

def main():
    #Menü
    while True:
        print("[1] Link hinzufügen")
        print("[2] Download starten")
        print("[3] Einstellungen")
        print("[4] Programm beenden")

        
        choice = input("Auswahl: ")
        
        if choice == "1":
            add_link()
        elif choice == "2":
            download_queue()
        elif choice == "3":
            settings()
        elif choice == "4":
            break

def settings():
    while True:
        print("[1] Download-Pfad ändern")
        print("[2] Prefix aktivieren/deaktivieren")
        print("[3] Zurück")
        choice = input("Auswahl: ")

        if choice == "1":
            change_download_path()
        elif choice == "2":
            change_prefix_mode()
        elif choice == "3":
            break

def change_download_path():
    global dl_path
    print(f"Der aktuelle Download-Pfad ist {dl_path}")
    new_path = input("Neuer Download-Pfad: ")
    dl_path = new_path

def change_prefix_mode():
    global prefix
    while True:
        choice = input("Prefix aktivieren? [y/n]: ")
        
        if choice == "y":
            prefix = True
            print("Prefix aktiviert.")
            break

        elif choice == "n":
            prefix = False
            print("Prefix deaktiviert.")
            break

def add_link():
    link = input("Link: ")
    
    if "/watch?v=" in link:
        download_video(link, dl_path)
    elif "/playlist?list=" in link:
        add_playlist_to_queue(link)
    else:
        print("Ungültiger Link.")  

def download_queue():
    queue = load_queue()
    print("Starting download...")
    for playlist_name in queue:
        playlist_path = create_playlist_folder(playlist_name)
        print(f"Downloading {playlist_name}...")
        for link in queue[playlist_name]:
            download_video(link, path=playlist_path)
        print(f"Downloaded {playlist_name} to {playlist_path}")
    print("Download finished.")

    #remove downloaded playlists from queue
    save_queue({})

def show_queue():
    queue = load_queue()
    for link in queue:
        print(link)

def add_playlist_to_queue(link):
    pl = Playlist(link)

    queue = load_queue()
    queue[pl.title] = []

    print(f"Adding videos from {pl.title} to queue...")
    for video in pl.videos:
        queue[pl.title].append(video.watch_url)
        print(f"Added {video.title} to queue")

    save_queue(queue)

def create_data_file():
    try:
        with open("data.json", "r") as file_data:
            pass
    except FileNotFoundError:
        with open("data.json", "w") as file_data:
            json.dump({}, file_data)

def load_queue():
    with open("data.json", "r") as file_data:
        queue = json.load(file_data)
        return queue
    
def save_queue(queue: dict):
    with open("data.json", "w") as file_data:
        json.dump(queue, file_data)

def download_video(link, path):
    video = YouTube(link)
    print(f"Downloading '{video.author} - {video.title}'...")
    try:
        if prefix:
            video.streams.get_highest_resolution().download(path, filename_prefix=f"{video.author} - ")
        else:
            video.streams.get_highest_resolution().download(path)
        print("done.")
    except:
        print("failed.")

def create_playlist_folder(playlist_name):
    path = os.path.join(dl_path, playlist_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

if __name__ == "__main__":
    main()