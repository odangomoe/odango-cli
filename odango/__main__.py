from .title import Title
from .torrent import Torrent
from colorama import Fore
import sys

import re


def write(text, end='\n'):
    print(text, end=end, file=sys.stderr, flush=True)

def main():
    while True:
        write(Fore.RESET + 'Please enter an anime title: ' + Fore.GREEN, end='')
        result = str(sys.stdin.readline()[:-1])
        resp = Title.search(result.strip())
        if len(resp['result']) > 0:
            break

        write(Fore.RED + 'No results found' + Fore.RESET)

    write(Fore.RESET)

    i = 0
    nr = 0
    if len(resp['result']) > 1:
        for title in resp['result']:
            write(
                '[%s%s%s] %s%s%s (%s%s%s)' % (
                    Fore.CYAN,
                    i,
                    Fore.RESET,
                    Fore.BLUE,
                    title['title'],
                    Fore.RESET,
                    Fore.RED,
                    title['main'],
                    Fore.RESET
                )
            )
            i += 1

        write('')

        while True:
            write(Fore.RESET + 'Please select correct title: ' + Fore.GREEN, end='')
            nr = sys.stdin.readline().strip()
            if nr.isnumeric() and int(nr) < len(resp['result']):
                break

        nr = int(nr)

        write(Fore.RESET)

    id = resp['result'][nr]['id']
    sets = Torrent.by_anime(id)

    write('Selected: ' + Fore.BLUE + resp['result'][nr]['title'] + Fore.RESET + ' AniDB id: ' + Fore.CYAN + str(
        id) + Fore.RESET)
    write('Also known as: ' + Fore.RED + (Fore.RESET + ', ' + Fore.RED).join(sets['anime']['alternatives']) + Fore.RESET)
    write('')

    i = 0

    torrentSets = list(sets['torrent-sets'])

    if len(torrentSets) == 0:
        write(Fore.RED + 'No torrents found for this anime' + Fore.RESET)
        exit(1)


    def get_key(set):
        res = set['metadata']['resolution'] if set['metadata']['resolution'] is not None else '0'
        nr = re.match(r"(.*[^0-9])?(\d+)", res).group(2)

        return [
            set['metadata']['group'] if set['metadata']['group'] is not None else 'ZZZZZZZZZZZ',
            'unofficial' in set['torrents'][0]['title'].lower(),
            -int(nr),
            set['metadata']['type'] if set['metadata']['type'] is not None else 'ZZZZZZZZZZZ',
            len(set['torrents'])
        ]


    torrentSets.sort(key=get_key)

    for set in torrentSets:

        metadata = set['metadata']
        tags = []

        if metadata['group']:
            tags.append(Fore.MAGENTA + metadata['group'] + Fore.RESET)

        if metadata['resolution']:
            tags.append(metadata['resolution'])

        spoiler = ''

        if 'unofficial' in set['torrents'][0]['title'].lower():
            spoiler = Fore.RED + '[UNOFFICIAL]' + Fore.RESET

        write(
            '[%s%s%s] %s / %s%s%s / %s%d torrents%s %s' % (
                Fore.CYAN,
                i,
                Fore.RESET,
                ' / '.join(tags),
                Fore.RED,
                set['metadata']['type'],
                Fore.RESET,
                Fore.YELLOW,
                len(set['torrents']),
                Fore.RESET,
                spoiler
            )
        )

        i += 1

    write('')

    while True:
        write(Fore.RESET + 'Select torrent set: ' + Fore.GREEN, end='')
        nr = sys.stdin.readline().strip()
        if nr.isnumeric() and int(nr) < len(torrentSets):
            break

    nr = int(nr)
    write('', end=Fore.RESET)

    selectedSet = torrentSets[nr]

    for torrent in selectedSet['torrents']:
        print(torrent['nyaa']['torrent'])

if __name__ == "__main__":
    main()
