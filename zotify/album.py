from zotify.const import (ALBUM_TYPE, ALBUM_URL, ARTIST_URL, ARTISTS,
                          COMPILATION, DISC_NUMBER, ID, ITEMS, NAME)
from zotify.termoutput import Loader, PrintChannel, Printer
from zotify.track import download_track
from zotify.utils import fix_filename
from zotify.zotify import Zotify


def get_album_info(album_id: str) -> tuple[str, str, list[dict], int, bool]:
    """Returns album info and tracklist"""

    (raw, resp) = Zotify.invoke_url(f"{ALBUM_URL}/{album_id}")

    album_name = fix_filename(resp[NAME])
    album_artists = [artist[NAME] for artist in resp[ARTISTS]]
    compilation = resp[ALBUM_TYPE] == COMPILATION

    tracks = Zotify.invoke_url_nextable(f"{ALBUM_URL}/{album_id}/tracks", ITEMS)

    total_discs = tracks[-1][DISC_NUMBER]

    return album_name, album_artists, tracks, total_discs, compilation


def get_artist_album_ids(artist_id):
    """Returns artist's albums"""
    with Loader(PrintChannel.PROGRESS_INFO, "Fetching artist information..."):
        # excludes "appears_on" and "compilations"
        url = f"{ARTIST_URL}/{artist_id}/albums?include_groups=album%2Csingle"
        simple_albums = Zotify.invoke_url_nextable(url, ITEMS)

    return [album[ID] for album in simple_albums]


def download_artist_albums(artist, pbar_stack: list | None = None):
    """Downloads albums of an artist"""
    album_ids = get_artist_album_ids(artist)

    pos, pbar_stack = Printer.pbar_position_handler(5, pbar_stack)
    pbar = Printer.pbar(
        album_ids,
        unit="album",
        pos=pos,
        disable=not Zotify.CONFIG.get_show_artist_pbar(),
    )
    pbar_stack.append(pbar)

    for album_id in pbar:
        download_album(album_id, pbar_stack)
        pbar.set_description(get_album_info(album_id)[0])
        Printer.refresh_all_pbars(pbar_stack)


def download_album(
    album_id: str, pbar_stack: list | None = None, M3U8_bypass: str | None = None
) -> bool:
    """Downloads songs from an album"""
    album_name, album_artists, tracks, total_discs, compilation = get_album_info(
        album_id
    )
    char_num = max({len(str(len(tracks))), 2})

    if Zotify.CONFIG.get_skip_comp_albums() and compilation:
        Printer.hashtaged(
            PrintChannel.SKIPPING,
            "ALBUM IS A COMPILATION\n"
            + f"Album_Name: {album_name} - Album_ID: {album_id}",
        )
        return False
    elif Zotify.CONFIG.get_regex_album():
        regex_match = Zotify.CONFIG.get_regex_album().search(album_name)
        if regex_match:
            Printer.hashtaged(
                PrintChannel.SKIPPING,
                "ALBUM MATCHES REGEX FILTER\n"
                + f"Album_Name: {album_name} - Album_ID: {album_id}\n"
                + (
                    f"Regex Groups: {regex_match.groupdict()}\n"
                    if regex_match.groups()
                    else ""
                ),
            )
            return False

    pos, pbar_stack = Printer.pbar_position_handler(3, pbar_stack)
    pbar = Printer.pbar(
        tracks, unit="song", pos=pos, disable=not Zotify.CONFIG.get_show_album_pbar()
    )
    pbar_stack.append(pbar)

    for n, track in enumerate(pbar, 1):

        extra_keys = {
            "album_num": str(n).zfill(char_num),
            "album_artists": album_artists,
            "album": album_name,
            "album_id": album_id,
            "total_discs": total_discs,
        }

        if M3U8_bypass is not None:
            extra_keys["M3U8_bypass"] = M3U8_bypass

        download_track("album", track[ID], extra_keys, pbar_stack)
        pbar.set_description(track[NAME])
        Printer.refresh_all_pbars(pbar_stack)
    return True
