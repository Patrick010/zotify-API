import datetime
import json
from pathlib import Path
from time import sleep

import requests
from librespot.audio.decoders import VorbisOnlyAudioQuality

from zotify import OAuth, Session
from zotify.config import Config
from zotify.const import (ITEMS, LIMIT, OFFSET, PLAYLIST_READ_PRIVATE, PREMIUM,
                          TYPE, USER_FOLLOW_READ, USER_LIBRARY_READ,
                          USER_READ_EMAIL)
from zotify.termoutput import Loader, PrintChannel, Printer


class Zotify:
    SESSION: Session = None
    DOWNLOAD_QUALITY = None
    CONFIG: Config = Config()
    DATETIME_LAUNCH = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    TOTAL_API_CALLS = 0

    def __init__(self, args):
        Zotify.CONFIG.load(args)
        with Loader(PrintChannel.MANDATORY, "Logging in..."):
            Zotify.login(args)

    @classmethod
    def login(cls, args):
        """Authenticates and saves credentials to a file"""
        # Create session
        if args.username not in {None, ""} and args.token not in {None, ""}:
            oauth = OAuth(args.username, *cls.CONFIG.get_oauth_addresses())
            oauth.set_token(args.token, OAuth.RequestType.REFRESH)
            cls.SESSION = Session.from_oauth(
                oauth, cls.CONFIG.get_credentials_location(), cls.CONFIG.get_language()
            )
        elif (
            cls.CONFIG.get_credentials_location()
            and Path(cls.CONFIG.get_credentials_location()).exists()
        ):
            cls.SESSION = Session.from_file(
                cls.CONFIG.get_credentials_location(),
                cls.CONFIG.get_language(),
            )
        else:
            username = args.username
            if not username:
                username = Printer.get_input("Username: ")
            oauth = OAuth(username, *cls.CONFIG.get_oauth_addresses())
            auth_url = oauth.auth_interactive()
            Printer.new_print(
                PrintChannel.MANDATORY,
                f"Click on the following link to login:\n{auth_url}",
            )
            cls.SESSION = Session.from_oauth(
                oauth, cls.CONFIG.get_credentials_location(), cls.CONFIG.get_language()
            )

    @classmethod
    def get_content_stream(cls, content_id, quality):
        try:
            return cls.SESSION.content_feeder().load(
                content_id, VorbisOnlyAudioQuality(quality), False, None
            )
        except RuntimeError as e:
            if "Failed fetching audio key!" in e.args[0]:
                gid, fileid = e.args[0].split("! ")[1].split(", ")
                Printer.hashtaged(
                    PrintChannel.ERROR,
                    "FAILED TO FETCH AUDIO KEY\n"
                    + "MAY BE CAUSED BY RATE LIMITS - CONSIDER INCREASING `BULK_WAIT_TIME`\n"
                    + f"GID: {gid[5:]} - File_ID: {fileid[8:]}",
                )
            else:
                raise e

    @classmethod
    def __get_auth_token(cls):
        return (
            cls.SESSION.tokens()
            .get_token(
                USER_READ_EMAIL,
                PLAYLIST_READ_PRIVATE,
                USER_LIBRARY_READ,
                USER_FOLLOW_READ,
            )
            .access_token
        )

    @classmethod
    def get_auth_header(cls):
        return {
            "Authorization": f"Bearer {cls.__get_auth_token()}",
            "Accept-Language": f"{cls.CONFIG.get_language()}",
            "Accept": "application/json",
            "app-platform": "WebPlayer",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        }

    @classmethod
    def invoke_url(
        cls, url: str, _params: dict | None = None, expectFail: bool = False
    ) -> tuple[str, dict]:
        headers = cls.get_auth_header()

        tryCount = 0
        while tryCount <= cls.CONFIG.get_retry_attempts():
            response = requests.get(url, headers=headers, params=_params)
            cls.TOTAL_API_CALLS += 1

            try:
                responsetext = response.text
                responsejson = response.json()
                if not responsejson:
                    raise json.decoder.JSONDecodeError
                # responsejson = {"error": {"status": "Unknown", "message": "Received an empty response"}}
            except json.decoder.JSONDecodeError:
                responsejson = {
                    "error": {
                        "status": "Unknown",
                        "message": "Received an empty response",
                    }
                }

            if not responsejson or "error" in responsejson:
                if not expectFail:
                    Printer.hashtaged(
                        PrintChannel.WARNING,
                        f"API ERROR (TRY {tryCount}) - RETRYING\n"
                        + f'{responsejson["error"]["status"]}: {responsejson["error"]["message"]}',
                    )
                sleep(5 if not expectFail else 1)
                tryCount += 1
                continue
            else:
                return responsetext, responsejson

        if not expectFail:
            Printer.hashtaged(
                PrintChannel.API_ERROR,
                f"API ERROR (TRY {tryCount}) - RETRY LIMIT EXCEDED\n"
                + f'{responsejson["error"]["status"]}: {responsejson["error"]["message"]}',
            )

        return responsetext, responsejson

    @classmethod
    def invoke_url_with_params(cls, url, limit, offset, **kwargs):
        params = {LIMIT: limit, OFFSET: offset}
        params.update(kwargs)

        _, responsejson = cls.invoke_url(url, params)
        return responsejson

    @classmethod
    def invoke_url_nextable(
        cls,
        url: str,
        response_key: str = ITEMS,
        limit: int = 50,
        stripper: str | None = None,
        offset: int = 0,
    ) -> list:
        resp = cls.invoke_url_with_params(url, limit=limit, offset=offset)
        if stripper is not None:
            resp = resp[stripper]
        items: list = resp[response_key]

        while resp["next"] is not None:
            (raw, resp) = Zotify.invoke_url(resp["next"])
            items.extend(resp[response_key])
        return items

    @classmethod
    def invoke_url_bulk(
        cls, url: str, bulk_items: list[str], stripper: str, limit: int = 50
    ) -> list:
        items = []
        while len(bulk_items):
            items_batch = "%2c".join(bulk_items[:limit])
            bulk_items = bulk_items[limit:]

            (raw, resp) = Zotify.invoke_url(url + items_batch)
            items.extend(resp[stripper])
        return items

    @classmethod
    def check_premium(cls) -> bool:
        return cls.SESSION.get_user_attribute(TYPE) == PREMIUM
