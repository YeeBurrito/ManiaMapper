from pathlib import Path
import dotenv
import os
from ossapi import Ossapi, BeatmapsetSearchMode, BeatmapsetSearchCategory, BeatmapsetSearchExplicitContent
import requests
import urllib
import re
import zipfile

def get_client():
    file_exists = os.path.exists('.env')
    if file_exists:
        dotenv.load_dotenv('.env')
    else:
        dotenv.load_dotenv(dotenv_path = Path('../.env'))
    
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    api = Ossapi(client_id, client_secret)
    return api

def get_desired_mapsets(api, query):
    search = api.search_beatmapsets(query, mode=BeatmapsetSearchMode.MANIA, category=BeatmapsetSearchCategory.HAS_LEADERBOARD, explicit_content=BeatmapsetSearchExplicitContent.SHOW)
    sets = search.beatmapsets

def get_beatmapset(api, mapset_id):
    r = requests.get("https://api.chimu.moe/v1/download/" + str(mapset_id), stream=True)
    if r.headers['Content-Type'] != 'application/octet-stream':
        return None
    d = r.headers['Content-Disposition']
    filename = urllib.parse.unquote(d.split("filename=")[1])
    filename = re.sub(r'[\/\\\*:\?"\<>\|]', "", filename)
    filename = filename.replace(".osz", ".zip")
    with open(os.path.join("./Beatmaps/", filename), "wb") as f:
        for chunk in r.iter_content(4096):
            f.write(chunk)
    # with zipfile.ZipFile(os.path.join("./Beatmaps/", filename), 'r') as zip_ref:
    #     zip_ref.extractall(os.path.join("./Beatmaps/", filename.replace(".zip", "")))
    # os.remove(os.path.join("./Beatmaps/", filename))
    # banned_key_list = ["1k", "2k", "3k", "5k", "6k", "7k", "8k", "9k", "10k", "1K", "2K", "3K", "5K", "6K", "7K", "8K", "9K", "10K"]
    # for file in os.listdir(os.path.join("./Beatmaps/", filename.replace(".zip", ""))):
    #     if file.endswith(".osu") and [key for key in banned_key_list if key in file]:
    #         os.remove(os.path.join("./Beatmaps/", filename.replace(".zip", ""), file))
    return filename

def get_beatmap_difficulty(api, map_id):
    try :
        beatmap = api.beatmap_attributes(map_id)
    except:
        return None
    #returns beatmap as Ossapi object
    #get the star_rating attribute to get the star rating of the beatmap
    return beatmap.attributes.star_rating

def main():
    api = get_client()

if __name__ == '__main__':
    main()
