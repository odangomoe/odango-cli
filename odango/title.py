import requests

class Title:
    @staticmethod
    def search(name):
        return requests.get('https://odango.moe/api/title', params={
            'q': name,
        }).json()
