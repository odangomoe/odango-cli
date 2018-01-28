import requests

class Torrent:
    @staticmethod
    def by_anime(id):
        return requests.get('https://odango.moe/api/torrent/by-anime/' + str(id)).json()