# notesmap in depth

The notes format, Zotero, public and published maps, shared editing, and every
setting. The [README](../README.md) has the quick start.

## Writing notes

```latex
\usepackage{notesmap}

\begin{programnote}{Group -- what they build}{GroupKey}
\location{51.05}{3.72}{Ghent, Belgium}   % the pin; [dx,dy] fixes the panel's offset
\thumb{img/group.png}
\paragraph{What it is}                   % becomes the lead line
...
\paragraph{Why it matters here}
Shares a detector with \ref{prog:OtherKey}.   % an arrow, captioned by this sentence

\begin{papernote}{Author et al.\ 2023 -- Title}{Author2023}   % the year orders the cards
Journal 1:2, \doi{10.xxxx/yyyy}.                               % the card's link
\paragraph{Summary}
... \gap{still to check}
\end{papernote}
\end{programnote}

\begin{confnote}{IEEE NSS/MIC 2027 -- Pasadena}{NSSMIC2027}   % a conference panel
\location{34.15}{-118.14}{Pasadena, USA}
\dates{2027-10-30}{2027-11-06}
\deadline[abstracts]{2027-05-12T23:59:59+02:00}               % counts down live
\end{confnote}
```

Put each `\begin` and `\end` on its own line. The text before ` -- ` is the
name a `\ref` shows. Panels without an offset are placed near their pin,
keeping leaders from crossing. On the map, drag a panel's corner square to
move it and its bottom-right grip to resize it.

## With Zotero

Use each paper's Zotero citation key as its note key, then point notesmap at
what Zotero keeps on disk:

```toml
[check]
bib = "library.bib"       # Better BibTeX export with "Keep updated" ticked
[pdfs]
dir = "papers"            # where ZotMoov files PDFs, renamed to {{ citationKey }}
url = "https://github.com/you/papers/blob/main/{key}.pdf"
```

`check` then flags a note whose DOI Zotero holds under another key, and each
card links to its PDF. Keeping `papers/` in a private git repo puts the PDFs
online without Zotero's storage limit.

## Public maps

The PDF keeps everything; the map can leave your own working out. Under
`[publish]`: `hide_sections` drops `\paragraph`s by heading (e.g. "why it
matters"), `hide_gaps` drops `\gap{}`, `hide_programmes` drops whole
programmes. `\aside{...}` marks a single sentence to keep off the map. An arrow
survives only if a shown sentence still makes the reference.

## Publishing the map without a server

The map can be a link instead of a running `notesmap serve`: danvas's static
page builds it in each reader's browser from the notes in your repository, and
redraws within a minute of a push. Add a `danvas.toml` beside `notesmap.toml`:

```toml
[app]
entry = "notesmap.static:app"
requires = ["github:DanielChahine004/notesmap@main"]   # this repo; pin a tag or commit to hold a version
files = ["notesmap.toml"]                              # notesmap reads the rest from it
```

and open `https://danielchahine004.github.io/danvas/?repo=you/your-notes`. To run
a copy of notesmap you have changed, keep it in your repository and replace
`requires` with `paths = ["path/to/notesmap/src"]`. Each reader sees their own
copy of the board (what they draw stays in their browser), and the companion
editor link is dropped when it points at your own machine. A private repository
needs a GitHub token for now; see danvas's
[web/README.md](https://github.com/DanielChahine004/danvas/blob/main/web/README.md).

## Sharing and editing

- **Split the notes.** `\input{programmes/ghent}` per programme; notesmap
  follows `\input`, so people editing different programmes never collide.
- **Shared storage.** `[source] path` takes a local path (a checkout, Dropbox,
  a synced bucket) or an http(s) URL. Changes are read only once they settle
  and parse; a `.lock` file beside `main.tex` holds the last good version.
- **Live co-editing.** JupyterLab with `jupyter-collaboration` writes every
  keystroke to the file the map watches. Set `[server] edit_url` to link it
  from the map. It saves with LF line endings.

## Configuration

Everything lives in `notesmap.toml`; `notesmap init` writes an annotated copy.

| Section | Controls |
|---|---|
| `[source]` | where the notes are, polling, lock files, a custom parser |
| `[latex]` | environment names, the lead-line heading, your macros and plugins |
| `[board]` | row order, links not to draw, the shelf for loose papers |
| `[publish]` | what the map leaves out |
| `[check]` | the bibliography to cross-check |
| `[pdfs]` | folder of `<key>.pdf` and the URL a card links to |
| `[claims]` | annotation files and a viewer URL: `\claim{Key/id}` after a sentence links it to the quote that backs it ([paperstore](https://github.com/DanielChahine004/paperstore)), and `check` fails on one that is missing; `figures` (a folder of `<Key>/<id>.png`, e.g. a paperstore's `figures/`) lets `\claimfig{Key/id}` show a box annotation's picture with its label and page |
| `[map]` | the map image (any equirectangular image) and its width |
| `[tables.<Key>]` | turns a programme's tabulars into a sortable table panel, or a radar (`view = "radar"` or `"detectors"`) |
| `[server]` | port and the companion editor link |

**Macros:** `[latex.macros]` takes templates (`kg = "{1} kg"`); for anything
more, a plugin module with `register(converter)`.

**Not LaTeX?** `[source] parser = "mynotes:parse"` points at a Python function
that returns the notes; `examples/markdown/` is a working one.

Table and radar panels, custom parsers and scripted board checks follow.

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
