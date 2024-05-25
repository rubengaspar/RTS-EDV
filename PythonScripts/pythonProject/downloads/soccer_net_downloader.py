from SoccerNet.Downloader import SoccerNetDownloader

# Initialize the downloader
myDownloader = SoccerNetDownloader(LocalDirectory="../downloads/")
myDownloader.password = "s0cc3rn3t"


# myDownloader.downloadGames(files=["1_720p.mkv", "2_720p.mkv"],
#                            split=["train","valid","test","challenge"])

myDownloader.downloadGames(files=["1_224p.mkv", "2_224p.mkv"],
                           split=["train","valid","test","challenge"])
