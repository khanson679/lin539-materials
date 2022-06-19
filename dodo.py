"""
Doit task definition file for LIN 539 course notes.
"""

from pathlib import Path
from itertools import chain
from doit.tools import title_with_actions

DOIT_CONFIG = {"default_tasks": ["test_chapter"],
               "check_file_uptodate": "timestamp"}
# DOIT_CONFIG = {"action_string_formatting": "new"}

TIKZ2SVG = "scripts/tikz2svg.sh"

LATEX_TEMPLATE = "templates/latex-custom.tex"
# LATEX_BOOK_TEMPLATE = "templates/full-book.tex"
# LATEX_CH_TEMPLATE = "templates/single-chapter.tex"

CSTM_BLKS = "filters/custom-blocks.lua"
INCL_FILE = "filters/include-file.lua"
LATEX_TIPA = "filters/latex-tipa.lua"
STRIP_CODE = "filters/remove_code.lua"
EDGEMARKERS = "filters/edgemarkers.lua"

MYCOMMANDS = Path("includes/mathcommands.md")
LATEX_PREAMBLE = Path("includes/preamble.tex")
# YAMLHEADER = Path("includes/format.yaml")
WEBCSS = Path("includes/web-custom.css").resolve()  # must be absolute to load locally
MATHJAXCALL = Path("includes/include-mathjax.html")

SRCDIR = Path("source")
MD_EXTS = (".mdown", ".md")
SRC_MD = sorted(f for f in SRCDIR.glob('**/*') if f.suffix in MD_EXTS
                and "old" not in f.parts
                and "solutions" not in f.parts)
TIKZ_EXTS = (".tikz", ".forest")
SRC_TIKZ = sorted(f for f in SRCDIR.glob('**/*') if f.suffix in TIKZ_EXTS)

BUILDDIR = Path("build")
IMGDIR = BUILDDIR / "images"
TEXDIR = BUILDDIR / "latex"
PDFDIR = BUILDDIR / "pdf"
PDFBUILDDIR = BUILDDIR / "pdfbuild"
HTMLDIR = BUILDDIR / "html"
MODCMDS = BUILDDIR / "mathcommands-preproc.md"

TEX_BOOK = TEXDIR / "full-book.tex"
PDF_BOOK = PDFDIR / "full-book.pdf"

LATEX_DEPS = [CSTM_BLKS, INCL_FILE, LATEX_TIPA, EDGEMARKERS,
              LATEX_TEMPLATE, LATEX_PREAMBLE, MODCMDS]
HTML_DEPS = [CSTM_BLKS, INCL_FILE,
             WEBCSS, MATHJAXCALL, MODCMDS]

# options shared by all Pandoc commands
PANDOC_OPTS = (
    "-f markdown-implicit_figures"
    f" --metadata-file={SRCDIR}/metadata.yaml"
    # " -V showanswers"
    f" -L {CSTM_BLKS} -L {INCL_FILE}")

# options for LaTeX/PDF only
LATEX_OPTS = (
    f" -H {LATEX_PREAMBLE} -H {MODCMDS}"
    f" --template {LATEX_TEMPLATE}"
    f" -L {LATEX_TIPA}"
    f" -L {EDGEMARKERS}")

# options for HTML only
HTML_OPTS = (
    f"--shift-heading-level-by=1 -c {WEBCSS}"
    f" --mathjax -Vmath='' -H {MATHJAXCALL}"
    f" {MODCMDS}")

# BOOK_OPTIONS = "--toc-depth"

# source directories
BOOK_CHAPS = ["01_intro", "02_n-grams", "03_universals", "04_representations",
              "05_automata"]
BOOK_CHAPS += [f"background/{subch}" for subch in
               ["algebra", "functions", "general", "graphs", "logic", "multisets",
                "posets", "relations", "sets", "strings", "tuples"]]
# BOOK_CHAPS += ["solutions/01_intro", "solutions/02_n-grams",
#                "solutions/03_universals", "solutions/04_representations",
#                "solutions/05_automata"]
# BOOK_CHAPS += [f"solutions/background/{subch}" for subch in
#                ["functions", "general", "graphs", "logic", "multisets",
#                 "posets", "relations", "sets", "strings", "tuples"]]


def task_test_chapter():
    """Compile just one chapter to PDF."""
    chname = "02_n-grams"
    srcsubdir = SRCDIR / chname
    infiles = sorted(str(f) for f in srcsubdir.glob("*.md"))
    outfile = f"{PDFDIR}/test/{chname}.pdf"
    cmd = (
        f"TEXINPUTS=.:{srcsubdir}:"
        f" pandoc -s -t pdf {PANDOC_OPTS} {LATEX_OPTS}"
        " --toc --toc-depth 1"
        " -M singlechapter"
        f" --metadata-file={srcsubdir}/metadata.yaml"
        " --verbose"
        f" {' '.join(infiles)} -o {outfile}"
    )
    return {
        "targets": [outfile],
        "file_dep": [*infiles, *LATEX_DEPS],
        "actions": [f"mkdir -p $(dirname {outfile})", cmd],
        "clean": True}


def task_test_section():
    """Compile just one section to PDF."""
    chname = "02_n-grams"
    secname = "00_ngrams"
    srcsubdir = SRCDIR / chname
    infile = f"{SRCDIR}/{chname}/{secname}.md"
    outfile = f"{PDFDIR}/test/{chname}/{secname}.pdf"
    cmd = (
        f"TEXINPUTS=.:{srcsubdir}:"
        f" pandoc -s -t pdf {PANDOC_OPTS} {LATEX_OPTS}"
        " --shift-heading-level-by=-1"
        " -M singlesection"
        f" --metadata-file={srcsubdir}/metadata.yaml"
        " --verbose"
        f" {infile} -o {outfile}"
    )
    return {
        "targets": [outfile],
        "file_dep": [infile, *LATEX_DEPS],
        "actions": [f"mkdir -p $(dirname {outfile})", cmd],
        "clean": True}


#
# Pre-processing
#

def task_mathcommands():
    """
    Preprocess custom command file for PDF (LaTeX) and HTML conversion.

    At present, simply removes surrounding $ signs, which are needed
    for Jupyter only, and commented lines, which interfere with non-LaTeX
    build paths.
    """
    return {
        "targets": [MODCMDS],
        "file_dep": [MYCOMMANDS],
        "actions": [
            f"mkdir -p $(dirname {MODCMDS})",
            ("sed -e 's/\\(^\\$\\|\\$$\\)//g' -e '/^%%/d'"
             f" {MYCOMMANDS} > {MODCMDS}")],
            "clean": True}


#
# PDF/LaTeX build path
#

def task_latex_book():
    """
    Build entire book as LaTeX using Pandoc.
    """
    srcsubdirs = [SRCDIR / ch for ch in BOOK_CHAPS]
    infiles = sorted(str(f)
                     for f in chain.from_iterable(subdir.glob("*.md")
                                                  for subdir in srcsubdirs))
    outfile = TEX_BOOK
    cmd = (
        f"TEXINPUTS=.:{':'.join(str(sd) for sd in srcsubdirs)}:"
        f" pandoc -s -t latex {PANDOC_OPTS} {LATEX_OPTS}"
        " --toc --toc-depth 1"
        f" {' '.join(infiles)} -o {outfile}"
    )
    return {
        "targets": [outfile],
        "file_dep": [*infiles, *LATEX_DEPS],
        "actions": [f"mkdir -p $(dirname {outfile})", cmd],
        "clean": True}


def task_pdf_book():
    """
    Build entire book as PDF.

    If intermediate LaTeX is needed, use "latex_book" instead.
    """
    srcsubdirs = [SRCDIR / ch for ch in BOOK_CHAPS]
    infile = TEX_BOOK
    outfile = PDF_BOOK
    buildfile = PDFBUILDDIR / outfile.relative_to(PDFDIR)
    cmd = (
        f"TEXINPUTS=.:{':'.join(str(sd) for sd in srcsubdirs)}:"
        f" pdflatex -interaction nonstopmode"
        f" -output-directory $(dirname {buildfile}) {infile}"
        f" && mv {buildfile} {outfile}"
    )
    return {
        "targets": [outfile],
        "file_dep": [infile],
        "actions": [f"mkdir -p $(dirname {outfile})", cmd],
        "clean": True}


def task_latex_chaps():
    """
    Build LaTeX standalone chapters with Pandoc.
    """
    for ch in BOOK_CHAPS:
        srcsubdir = SRCDIR / ch
        infiles = [str(f)
                   for f in sorted(srcsubdir.glob("*.md"))]
        outfile = f"{TEXDIR}/chapters/{ch}.tex"
        cmd = (
            f"pandoc -t latex {PANDOC_OPTS} {LATEX_OPTS}"
            " -M singlechapter"
            f" --metadata-file={srcsubdir}/metadata.yaml"
            f" {' '.join(infiles)} -o {outfile}"
        )
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [*infiles, *LATEX_DEPS],
            "actions": [f"mkdir -p $(dirname {outfile})", cmd],
            "clean": True}


def task_pdf_chaps(test=True):
    """
    Build PDF chapters from LaTeX generated by Pandoc.
    """
    for ch in BOOK_CHAPS:
        srcsubdir = SRCDIR / ch
        infile = f"{TEXDIR}/chapters/{ch}.tex"
        buildfile = f"{PDFBUILDDIR}/chapters/{ch}.pdf"
        outfile = f"{PDFDIR}/chapters/{ch}.pdf"
        cmd = (
            f"TEXINPUTS=.:{srcsubdir}:"
            f" pdflatex -interaction nonstopmode"
            f" -output-directory $(dirname {buildfile}) {infile}"
            f" && mv {buildfile} {outfile}"
        )
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [infile],
            "actions": [f"mkdir -p $(dirname {buildfile}) $(dirname {outfile})",
                        cmd],
            "clean": True}


def task_latex_sections():
    for infile in SRC_MD:
        outfile = TEXDIR / "sections" / infile.relative_to(SRCDIR).with_suffix(".tex")
        cmd = (
            f"pandoc -s -f markdown -t latex {PANDOC_OPTS} {LATEX_OPTS}"
            f" {infile} -o {outfile}"
        )
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [infile, *LATEX_DEPS],
            "actions": [f"mkdir -p $(dirname {outfile})", cmd],
            "clean": True}


def task_pdf_sections():
    for srcfile in SRC_MD:
        srcsubdir = srcfile.parent
        infile = TEXDIR / "sections" / srcfile.relative_to(SRCDIR).with_suffix(".tex")
        buildfile = PDFBUILDDIR / infile.relative_to(TEXDIR).with_suffix(".pdf")
        outfile = PDFDIR / infile.relative_to(TEXDIR).with_suffix(".pdf")
        cmd = (
            f"TEXINPUTS=.:{srcsubdir}:"
            f" pdflatex -interaction nonstopmode"
            f" -output-directory $(dirname {buildfile}) {infile}"
            f" && mv {buildfile} {outfile}"
        )
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [infile, *LATEX_DEPS],
            "actions": [f"mkdir -p $(dirname {buildfile}) $(dirname {outfile})",
                        cmd],
            "clean": True}


#
# HTML Build Path
#

def task_html_chaps():
    """
    Build HTML chapters using Pandoc.

    MODCMDS is inserted in the HTML body so that Pandoc will correctly add
    MathJax delimiters (it will not change included headers).

    Problem: the --mathjax command performs preprocessing, then inserts the
    MathJax script *only if* LaTeX math is detected. This means that in a file
    with no math, the custom commands that we insert will appear as raw text.
    The author of Pandoc has refused to change this. As a workaround, we
    use -Vmath='' to manually clear the internal variable where Pandoc records
    whether math was detected, and insert the script ourselves.
    """
    for ch in BOOK_CHAPS:
        infiles = sorted(str(f)
                         for f in Path(f"{SRCDIR}/{ch}").glob("*.md"))
        incl_images = sorted(HTMLDIR / img.relative_to(SRCDIR).with_suffix(".svg")
                             for img in SRC_TIKZ)
        outfile = Path(f"{HTMLDIR}/{ch}/index.html")
        cmd = (
            f"pandoc -t html {PANDOC_OPTS} {HTML_OPTS}"
            f" --metadata title={ch}"
            f" {' '.join(infiles)} -o {outfile}"
        )
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [*infiles, *incl_images, *HTML_DEPS],
            "actions": [f"mkdir -p $(dirname {outfile})",
                        cmd],
            "clean": True}


def task_html_images():
    """
    Copy pre-converted SVG images to proper directory.
    """
    for img in SRC_TIKZ:
        src = IMGDIR / img.relative_to(SRCDIR).with_suffix(".svg")
        dest = HTMLDIR / src.relative_to(IMGDIR)
        yield {
            "name": dest,
            "targets": [dest],
            "file_dep": [src],
            "actions": [
                f"mkdir -p $(dirname {dest})",
                f"cp {src} {dest}"],
            "clean": True}


def task_images():
    """
    Convert TikZ diagrams to SVG for HTML inclusion.
    """
    for infile in SRC_TIKZ:
        outfile = IMGDIR / infile.relative_to(SRCDIR).with_suffix(".svg")
        yield {
            "name": outfile,
            "targets": [outfile],
            "file_dep": [infile],
            "actions": [
                f"mkdir -p $(dirname {outfile})",
                f"{TIKZ2SVG} {infile} {outfile}"],
            "clean": True}
