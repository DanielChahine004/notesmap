# notesmap

Research-programme notes, written in LaTeX, shown as a live world map (or a
board). Each programme is a panel at its place on the map, with a lead line,
an image and a row of paper cards; click a card to unfold its note.
Cross-references become arrows captioned by the sentence that makes them. The
same `.tex` builds as a PDF, and every open map updates within seconds of an edit.

Built on [danvas](https://github.com/DanielChahine004/danvas). Written for a
PhD review of PET detector programmes, hence the PET examples; nothing depends
on the field.

## Quick start

Install [uv](https://docs.astral.sh/uv/), which brings Python with it
(Windows: `winget install astral-sh.uv`; macOS/Linux:
`curl -LsSf https://astral.sh/uv/install.sh | sh`). Then:

```
uv tool install git+https://github.com/DanielChahine004/notesmap
notesmap init notes        # notes/main.tex, notes/notesmap.sty, ./notesmap.toml
notesmap serve --map       # opens the map; edit notes/main.tex and watch it update
notesmap check             # missing images, dangling refs, unplaced programmes
```

`check --gaps` also lists unfinished notes; `--strict` exits non-zero on a
problem, for CI.

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
| `[map]` | the map image (any equirectangular image) and its width |
| `[tables.<Key>]` | turns a programme's tabulars into a sortable table panel, or a radar (`view = "radar"` or `"detectors"`) |
| `[server]` | port and the companion editor link |

**Macros:** `[latex.macros]` takes templates (`kg = "{1} kg"`); for anything
more, a plugin module with `register(converter)`.

**Not LaTeX?** `[source] parser = "mynotes:parse"` points at a Python function
that returns the notes; `examples/markdown/` is a working one.

Table and radar panels, custom parsers and scripted board checks are in
[docs/advanced.md](docs/advanced.md).

## Citing and licence

MIT (`LICENSE`); `CITATION.cff` has the citation. notesmap depends on danvas,
which is AGPL-3.0, so serving the map to others over a network brings danvas's
terms into play.
