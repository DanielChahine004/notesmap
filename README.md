# notesmap

Research notes written in LaTeX, shown as a live world map. Each programme is
a panel at its place, with a picture and a row of paper cards;
cross-references become arrows. The same `.tex` builds as a PDF, and the map
updates within seconds of each save. Built on
[danvas](https://github.com/DanielChahine004/danvas).

[![Download the template, open the folder in the browser, edit main.tex: the map follows](demo/notesmap-demo.gif)](demo/notesmap-demo.mp4)

## In the browser, nothing to install

1. Download [the template folder](https://raw.githubusercontent.com/DanielChahine004/notesmap/main/notesmap-notes.zip)
   and unzip it, or get your Overleaf notes with **Menu → Download → Source**.
2. Open [the notesmap page](https://danielchahine004.github.io/danvas/?local=DanielChahine004/notesmap)
   and choose the folder.
3. Edit `main.tex` and save. Chrome and Edge follow each save; in other
   browsers, drop the folder on the map again.

Nothing is uploaded. The template's `main.tex` shows everything the notes can
hold; pictures go in `img/` as PNG or JPEG.

## On your computer

Download this repository (**Code → Download ZIP**) and double-click
**`Start notesmap.bat`** (Windows) or **`Start notesmap.command`** (Mac; on
Linux run `start-notesmap.sh`). The first start downloads what it needs; then
the map opens and `notes/main.tex` is yours to edit. Everything stays inside
the folder. If Windows warns, choose **More info → Run anyway**; if a Mac
refuses, **System Settings → Privacy & Security → Open Anyway**.

With [uv](https://docs.astral.sh/uv/) on the command line:

```
uv tool install git+https://github.com/DanielChahine004/notesmap
notesmap init notes        # notes/main.tex, notes/notesmap.sty, ./notesmap.toml
notesmap serve --map       # opens the map; edit notes/main.tex and watch it update
notesmap check             # missing images, dangling refs, unplaced programmes
```

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

## More

Zotero, public maps, publishing a map as a link, shared editing and every
setting are in [docs/advanced.md](docs/advanced.md).

## Citing and licence

MIT (`LICENSE`); `CITATION.cff` has the citation. notesmap depends on danvas,
which is AGPL-3.0, so serving the map to others over a network brings danvas's
terms into play.
