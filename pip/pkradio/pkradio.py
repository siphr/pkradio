#!/usr/bin/python

def get_version():
    return "0.1"

def get_media_player() -> str:
    import os
    _players = ['mpv', 'mplayer', 'vlc']

    for p in _players:
        if (os.system(f'which {p}') == 0):
            return p

    raise Exception('This program relies on the MPV media player. Please ensure that it is installed. Alternatively you can try the Linux package which takes care of all dependencies.')

def load_stations() -> dict:
    import os
    import json
    return json.load(open(
        f'{os.path.dirname(__file__)}/stations.json'))

def _list_stations(_stations):
    for (k,v) in _stations.items():
        print(f'\033[2m{k}\033[0m: {v}')

def play_radio_uri(player: str, station_name: str):
    import os
    import json

    #print(f'playing station: {station_name}')

    print(os.path.dirname(__file__))
    try:
        _stations = json.load(open(f'{os.path.dirname(__file__)}/stations.json'))
    except:
        raise Exception('Cannot load stations.')

    try:
        uri:str = _stations[station_name]
    except KeyError:
        raise Exception(f'Unknown station {station_name}.')
    except:
        raise Exception('Unknown error.')

    res = os.system(f'{player} {uri}')
    if res != 0:
        raise Exception(f'There was an unknown problem playing {uri} with {player}. Maybe the player does not support streaming?')

def _parser():
    import argparse

    parser = argparse.ArgumentParser(description='Pakistani radio station player.')

    parser.add_argument('station', nargs='?', metavar='STATION', type=str, default=None,
            help='Station to play.')
    parser.add_argument('-l', '--list', action=argparse.BooleanOptionalAction, default=False,
            help='List all available stations.')
    parser.add_argument('-v', '--version', action=argparse.BooleanOptionalAction, default=False,
            help='Show application version.')

    args = parser.parse_args()
    return args

def _main():
    args = _parser()
    
    _stations = load_stations()
    if args.version:
        print(f'\033[1m{get_version()}\033[0m')
    elif args.list or args.station is None:
        _list_stations(_stations)
    else:
        if not args.station in _stations.keys():
            raise Exception(f'Not a valid station. Use -l."{args.station}" radio station.')

        _player = get_media_player()

        play_radio_uri(_player, args.station)
        

if __name__ == '__main__':
    _main()
