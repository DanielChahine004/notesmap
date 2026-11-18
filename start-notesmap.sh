#!/bin/sh
# Opens your notes as a live map (macOS and Linux). On a Mac, double-click
# "Start notesmap.command" instead, which runs this. The first run downloads
# what it needs (a few minutes); later runs start at once. Everything it
# downloads stays in this folder's .notesmap and .venv folders.
cd "$(dirname "$0")" || exit 1
here=$(pwd)

if command -v uv >/dev/null 2>&1; then
    UV=uv
else
    UV="$here/.notesmap/uv/uv"
    if [ ! -x "$UV" ]; then
        echo "Setting up notesmap for the first time. This needs the internet and takes a few minutes."
        echo
        if command -v curl >/dev/null 2>&1; then
            curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$here/.notesmap/uv" sh
        else
            wget -qO- https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$here/.notesmap/uv" sh
        fi
    fi
fi
if ! "$UV" --version >/dev/null 2>&1; then
    echo "Could not set up uv (see the messages above)."
    exit 1
fi

echo "Your notes are in the \"notes\" folder: edit notes/main.tex and the map updates as you save."
case "$(uname)" in
    Darwin) open "$here/notes" ;;
    *) command -v xdg-open >/dev/null 2>&1 && xdg-open "$here/notes" >/dev/null 2>&1 & ;;
esac
echo "The map opens in your browser. Keep this window open while you use it; close it to stop."
echo
exec "$UV" run --no-dev --frozen notesmap serve --map
