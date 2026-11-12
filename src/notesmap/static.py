"""notesmap as a static danvas app: the map, built in the reader's browser.

Shown by danvas's static page, with no server: a repository holding notes
says in its danvas.toml:

    [app]
    entry = "notesmap.static:app"
    requires = ["github:DanielChahine004/notesmap@<tag>"]   # the shared notesmap
    # paths = ["tools/notesmap/src"]                          # or a copy of its own
    files = ["notesmap.toml"]

`files()` tells the page what else to fetch (read from notesmap.toml); `app()`
builds the board as `notesmap serve --map` does and returns the reload hook the
page calls when a new commit brings new files.
"""
from __future__ import annotations

import asyncio
import posixpath
import tomllib
from pathlib import Path
from types import SimpleNamespace

CONFIG = "notesmap.toml"


def files(config: str = CONFIG) -> list[str]:
    """What the board reads, as paths or folder/ prefixes relative to the config's folder."""
    cfg = tomllib.loads(Path(config).read_text("utf-8")) if Path(config).exists() else {}
    src = cfg.get("source", {}).get("path", "notes/main.tex")
    folder = posixpath.dirname(src)
    out = [config, folder + "/" if folder else src]
    out.append(cfg.get("map", {}).get("image"))
    out.append(cfg.get("check", {}).get("bib"))
    claims = cfg.get("claims", {}).get("dir")
    out.append(claims + "/" if claims else None)
    for spec in (cfg.get("source", {}).get("parser"), *cfg.get("latex", {}).get("plugins", [])):
        if spec:
            out.append(spec.split(":")[0].replace(".", "/") + ".py")
    return [p for p in out if p]


def app(config: str = CONFIG, map: bool = True):
    import danvas

    from .cli import _setup
    from .render import Board

    cfg, src, conv, parser = _setup(SimpleNamespace(config=config))
    # a companion editor on the author's own machine is no use to a reader
    if cfg.edit_url and any(h in cfg.edit_url for h in ("127.0.0.1", "localhost")):
        cfg.edit_url = None
    _no_thread_timers(Board)
    canvas = danvas.Canvas()
    board = Board(canvas, cfg, src, conv, map)
    notes = parser(src, cfg)
    for w in notes.warnings:
        print(f"[notesmap] warning: {w}")
    print(f"[notesmap] {board.apply(notes)}")
    w = cfg.map_width
    view = {"grid": False, "zoom": 0.2, "x": w / 2, "y": w / 4} if map else {"grid": True, "zoom": 0.5}
    canvas.serve(view=view, ui_inspector=False)
    return lambda: board.apply(parser(src, cfg))


def _no_thread_timers(Board) -> None:
    """The board paces its re-stacking with sleeping threads; in a browser there
    are none, so the same delays go on the event loop."""
    loop = asyncio.get_event_loop()

    def later(fn, *delays):
        for d in delays:
            loop.call_later(d, fn)

    def on_layout(self, comp):
        if getattr(comp, "_auto_h", True) is False:
            comp.h = "auto"
        self._tick += 1
        mine = self._tick
        loop.call_later(0.4, lambda: self._tick == mine and self.settle())

    Board.later = staticmethod(later)
    Board._on_layout = on_layout
