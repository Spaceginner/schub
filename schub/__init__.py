import json
import os
from typing import Annotated

from sypy import Server
from sypy.http import HTTPException, HTTPStatus, Headers
from sypy.parameters import Body, Depends, Header

from .davult import Shortcut


_EDIT_CODE_ENVVAR_NAME = 'SCHUB_EDIT_CODE'
EDIT_CODE = os.environ.get(_EDIT_CODE_ENVVAR_NAME, None)


server = Server()


@server.get('/')
def show_the_way(d: str = None) -> str:
    if d is None:
        return ("you been travelling a lot, traveller.\n"
                "so lot, not even knowing what is the place you want to go to next.\n"
                "sit down here, and get some rest.")

    try:
        the_way = Shortcut.find(d).resolve()
    except KeyError:
        raise HTTPException(HTTPStatus.NotFound, "the place you want is unknown for me, traveller.") from None
    except RecursionError:
        raise HTTPException(HTTPStatus.InternalServerError, "my map shows too convoluted path to the place, traveller.") from None
    else:
        raise HTTPException(HTTPStatus.PermanentRedirect, "follow that way, traveller.", Headers(location=the_way))


def unlock_map(the_key: Annotated[str, Header]) -> None:
    if EDIT_CODE is None:
        raise HTTPException(HTTPStatus.Unauthorized, "the map is locked on an impossible key.")

    if the_key != EDIT_CODE:
        raise HTTPException(HTTPStatus.Unauthorized, "your key is for another lock.")


@server.post('/')
def mark_a_place(_: Annotated[None, Depends(unlock_map)], position_raw: Annotated[str, Body]) -> None:
    try:
        # as of 0.0.2, there is no support for JSON or even just dict, so we gotta do this way...
        shortcut = Shortcut(**json.loads(position_raw))
    except (TypeError, ValueError):
        raise HTTPException(HTTPStatus.UnprocessableContent, "i dont understand where the place is") from None
    else:
        shortcut.create()


@server.get('/map')
def show_all_of_map() -> str:
    # TODO make it disablable
    return f"i see you quite curious, traveller...\n\n{'\n'.join(map(str, Shortcut.get_all()))}"
