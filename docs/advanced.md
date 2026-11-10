# Advanced configuration

## Table and radar panels

| Key | What it does |
|---|---|
| `[tables.<Key>]` | turns that programme's tabulars into one sortable, filterable table panel at `at`; `flags` spells out a letter after a number (`1.4 p`) as a basis column, `derive` adds category columns from keywords; each row links to its paper's DOI and PDF, found from its first cell read as "Surname Year" (`keys` maps any other first cell to a note key) |
| `[tables.<Key>] view = "radar"` | instead of a table: two row sets on shared numeric axes (`demand`, `supply` name their headings) drawn as a radar for a chosen pair, with a fit grid for every pair |
| `[tables.<Key>] view = "detectors"` | the rows of a table panel on a radar of chosen lower-is-better columns (`axes` maps column to label), each linear in its own units from 0 to `max` at the rim; `reference` names the set drawn as dotted outlines, `simulated` the set drawn dashed, `alternates` an axis a button swaps, `initial` the rows drawn at first. `selector` names the table panel whose tick boxes choose what is drawn; that table also gets a Star column (the row's size on these axes) |
| `[tables.<Key>] reference_label` | the label on the radar's tick box for the `reference` set; defaults to the set's name |
| `[tables.<Key>] panel` | the programme panel shows only these paragraphs (by heading); the rest stays in the PDF |

## Your own parser

The map, the watcher and the live updates don't depend on LaTeX. Any Python
function that turns your files into notes can drive them:

```toml
[source]
path = "notes/index.md"          # where your files live
parser = "mynotes:parse"         # mynotes.py, beside notesmap.toml
```

```python
from notesmap.parse import Entry, Location, Notes

def parse(source, cfg):
    text = source.read_text("programmes/ghent.md")     # read through source...
    files = source.listdir("programmes")               # ...so edits reach the map
    prog = Entry("programme", "Ghent MEDISIP", "Ghent", given={
        "location": Location(51.05, 3.72, "Ghent"),
        "lead": "One line for the panel.",
        "full": "The **programme note**, in Markdown.",
        "thumb": "img/ghent.png", "link": "https://...", "refs": ["Pisa"],
    })
    prog.papers.append(Entry("paper", "España et al. 2014 -- DigiPET", "Espana2014",
                             given={"year": 2014, "lead": "...", "full": "...", "link": "https://doi.org/..."}))
    return Notes([prog])
```

- **Reading files.** Read them through `source`: use `read_text`, `read_bytes`
  or `listdir`, with paths relative to the main file's folder. The watcher
  follows everything read this way, including files added to a listed
  folder.
- **Entry fields.** `Entry.given` holds what the map shows. The keys are
  `thumb`, `images`, `link`, `location`, `year`, `lead`, `full` (both
  Markdown), `refs`, and `reasons`, which holds the arrow captions. See the
  `Entry` docstring.
- **Errors.** A parser that raises keeps the last good version on screen, and
  the error is printed once.
- **What doesn't apply.** `[publish]` hiding works on LaTeX bodies, so a
  parser of your own decides for itself what to leave out.

`examples/markdown/` is a working example: one Markdown file per programme.
Run it from that folder with `uv run --project ../.. notesmap serve --map`.

## Checking the board from a script

`serve --qc DIR` answers requests written to `DIR/request`, so a script or an agent can check the
board without driving a browser:

```bash
notesmap serve --map --qc qc &                         # in one shell
echo layout > qc/request                              # -> qc/layout.json
echo "shot Example" > qc/request                       # -> qc/layout.json + qc/shot.png
```

`layout.json` holds every panel's measured box, each map pin, and the leaders that
cross or run under a panel; `DIR/done` appears when it is written. A shot uses
danvas's `canvas.screenshot`, which needs a board tab open and in front; frame one
or two panels, since the whole canvas makes a very large image. The capture
renders panels without per-viewer browser state (a ticked box, a selection), so
use it for layout and look, not for that state.
