# importing needed modules
import os

from pytube import Channel
from pytube import Playlist
from pytube import YouTube

# don't change or things break
fileTypeAudio = "mp4"
fileTypeVideo = "mp4"


class VideoDownloader:
    def __init__(self, link, path, onlyAudio, prefixVideo, prefixPlaylist):
        # setting local class-variables
        self.link = link
        self.path = path
        self.audioOnly = onlyAudio
        self.prefixVideo = prefixVideo
        self.prefixPlaylist = prefixPlaylist

        # printing some debug output
        print(f"download audio only is set to {str(self.audioOnly)}")
        print(f"set prefix is set to {str(self.prefixVideo)}")
        print(f"path is {self.path}")
        print(f"link is {self.link}")

        # check link type and start downloading function
        if "/watch?v=" in self.link:
            print("detected video link")
            x = YouTube(self.link)
            self.download(x)

        elif "/playlist?list=" in self.link:
            print("detected playlist link")
            playlist = Playlist(self.link)
            if prefixPlaylist:
                try:
                    self.path = self.createDirectory(f"{playlist.owner} - {playlist.title}")
                except IndexError:
                    self.path = self.createDirectory(playlist.title)
            else:
                self.path = self.createDirectory(playlist.title)
            for x in playlist.videos:
                self.download(x)

        elif "/channel/" in self.link:
            print("detected channel link")
            channel = Channel(self.link)
            self.path = self.createDirectory(channel.channel_name)
            for x in channel.videos:
                self.download(x)
        # is
        print("finished downloading all content from supplied link")

    def createDirectory(self, name):
        """function for creating a directory based on given channel or playlist name"""

        finalpath = os.path.join(self.path, self.filterName(name))
        try:
            os.mkdir(finalpath)
            print("created folder")
        except FileExistsError:
            print("folder already existing, skipping mkdir")
        return finalpath

    def download(self, video):
        """actual downloading function with implemented settings like prefixes and stuff"""

        print(f"starting download on {video.title}")
        name = self.filterName(video.title)
        author = self.filterName(video.author)
        if self.prefixVideo:
            if self.audioOnly:
                video.streams.filter(only_audio=True, file_extension=fileTypeAudio) \
                    .desc() \
                    .first() \
                    .download(
                    output_path=self.path,
                    filename=" - " + name + "." + fileTypeAudio,
                    filename_prefix=author)
            else:
                video.streams.filter(progressive=True, file_extension=fileTypeVideo) \
                    .order_by("resolution") \
                    .desc() \
                    .first() \
                    .download(
                    output_path=self.path,
                    filename=" - " + name + "." + fileTypeVideo,
                    filename_prefix=author)

        else:
            if self.audioOnly:
                video.streams.filter(only_audio=True, file_extension=fileTypeAudio) \
                    .desc() \
                    .first() \
                    .download(
                    output_path=self.path,
                    filename=name + "." + fileTypeAudio)
            else:
                video.streams.filter(progressive=True, file_extension=fileTypeVideo) \
                    .order_by("resolution") \
                    .desc() \
                    .first() \
                    .download(
                    output_path=self.path,
                    filename=name + "." + fileTypeVideo)
        print("done...")

    def filterName(self, name):
        name = name.replace('"', "").replace("?", "").replace("|", "").replace("/", "").replace('\\', "").replace("*",
                                                                                                                  "").replace(
            ":", "").replace("<", "").replace(">", "")
        return name
