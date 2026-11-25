# Configuration file for the Sphinx documentation builder.

import glob
import io
import os

# Build-time assets for the PDF (needs cairosvg + Pillow, both in
# requirements.txt). Only the SVGs are committed sources:
#  - the navy cover logo is derived from the white HTML logo;
#  - each SVG figure gets a PDF twin, because pdflatex cannot include SVG.
#    Figures are referenced as ``_static/name.*`` so HTML picks the .svg and
#    LaTeX picks the .pdf.
try:
    import cairosvg
    from PIL import Image
except ImportError as e:
    raise RuntimeError(
        "The docs build needs cairosvg and Pillow to generate the PDF assets; "
        "install them with: pip install -r requirements.txt"
    ) from e

_static = os.path.join(os.path.dirname(__file__), '_static')
with open(os.path.join(_static, 'cryptnox-logo.svg'), encoding='utf-8') as f:
    _svg = f.read()
_png = cairosvg.svg2png(
    bytestring=_svg.replace('fill="white"', 'fill="#101f2e"').encode(),
    output_width=1200, output_height=226,
)
Image.open(io.BytesIO(_png)).save(
    os.path.join(_static, 'cryptnox-logo-dark.png'), dpi=(400, 400)
)
for _fig in glob.glob(os.path.join(_static, '*.svg')):
    if os.path.basename(_fig) == 'cryptnox-logo.svg':
        continue
    cairosvg.svg2pdf(url=_fig, write_to=_fig[:-4] + '.pdf')

# -- Project information -----------------------------------------------------

project = 'Cryptnox Shamir'
copyright = '2026, Cryptnox SA'
author = 'Cryptnox'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx_sitemap',
]

# Prefix section labels with the document name to avoid clashes
autosectionlabel_prefix_document = True
suppress_warnings = ['autosectionlabel.*']

# Number figures ("Fig. 1", "Fig. 2", ...) and let them be cross-referenced
numfig = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- SEO meta tags -----------------------------------------------------------

html_baseurl = 'https://docs.cryptnox.com/cryptnox-shamir/'
html_title = 'Cryptnox Shamir'
sitemap_url_scheme = "{link}"

html_meta = {
    'description': 'Operating documentation for the Cryptnox Shamir card system: '
                   'split a master secret across smart cards with Shamir Secret Sharing, '
                   'run the key ceremony, test backups and recover with a k-of-n quorum.',
    'keywords': 'Cryptnox, Shamir Secret Sharing, SSS, k-of-n, smart card, key ceremony, '
                'institutional custody, Bitcoin treasury, HSM backup, disaster recovery, '
                'documentation',
    'author': 'Cryptnox',
    'robots': 'index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large',
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_last_updated_fmt = '%Y-%m-%d'  # visible page dates — AI answers prefer dateable sources
html_logo = '_static/cryptnox-logo.svg'
html_favicon = '_static/favicon.png'

html_css_files = [
    'custom.css',
]

html_theme_options = {
    'analytics_id': 'GT-PJ7HDFB',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#101f2e',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 2,
    'includehidden': True,
    'titles_only': False,
}

html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False

# -- Options for PDF (LaTeX) output ------------------------------------------
# Built by CI with pdflatex; same cover and page layout as the
# cryptnox-hardware-wallet manual. Output: cryptnox-shamir.pdf

latex_engine = 'pdflatex'
latex_logo = '_static/cryptnox-logo-dark.png'  # generated above; the white logo is invisible on the white cover
latex_domain_indices = False  # no module index in the PDF (kept in HTML)
latex_documents = [
    ('index', 'cryptnox-shamir.tex',
     'Cryptnox Shamir — Operating Manual', author, 'manual'),
]
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'figure_align': 'H',
    'sphinxsetup': 'pre_border-radius=0pt',  # sharp rectangle corners on code-block frames
    'extraclassoptions': 'oneside,openany',  # no blank filler pages (web PDF)
    'printindex': '',  # no general Index in the PDF
    'fncychap': '',  # no fancy chapter rules; titlesec styles chapters instead
    'preamble': r'''
% Box-drawing characters in the ASCII diagrams (pdflatex has no glyphs for them)
\usepackage{pmboxdraw}
\DeclareUnicodeCharacter{256D}{\textSFi}% rounded corners -> square ones
\DeclareUnicodeCharacter{256E}{\textSFiii}
\DeclareUnicodeCharacter{2570}{\textSFii}
\DeclareUnicodeCharacter{256F}{\textSFiv}
% Symbols used in prose
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\le}}
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
\DeclareUnicodeCharacter{200B}{}
% Left-align body text (ragged right instead of justified)
\usepackage[document]{ragged2e}
% Drop the "(continues on next page)" / "(continued from previous page)" labels on code blocks
\AtBeginDocument{\renewcommand*\sphinxstylecodecontinued[1]{}\renewcommand*\sphinxstylecodecontinues[1]{}}
% Whole document in the sans font (TeX Gyre Heros)
\renewcommand{\familydefault}{\sfdefault}
% Literals, tables and code blocks in DejaVu Sans Mono instead of Sphinx's default txtt;
% scaled down since DejaVu runs large next to Heros
\usepackage[scaled=0.82]{DejaVuSansMono}
% Sans-serif TOC entries
\AtBeginDocument{\addtocontents{toc}{\protect\sffamily}}
% Left-aligned chapter headings
\usepackage{titlesec}
\titleformat{\chapter}[hang]{\sffamily\bfseries\huge}{\thechapter}{1em}{}
\titlespacing*{\chapter}{0pt}{0pt}{20pt}
\usepackage{fancyhdr}
\def\headruleskip{4pt}\def\footruleskip{4pt}% gap between header/footer text and rule
\makeatletter
% Centered page header (doc title) + copyright footer
\AtBeginDocument{%
  \fancypagestyle{normal}{%
    \fancyhf{}%
    \fancyhead[C]{\sffamily\nouppercase{\@title}}%
    \fancyfoot[L]{\sffamily\copyright{} 2026 Cryptnox SA}%
    \fancyfoot[R]{\sffamily\thepage}%
    \renewcommand{\headrulewidth}{0.4pt}%
    \renewcommand{\footrulewidth}{0.4pt}%
  }%
  \fancypagestyle{plain}{%
    \fancyhf{}%
    \fancyfoot[L]{\sffamily\copyright{} 2026 Cryptnox SA}%
    \fancyfoot[R]{\sffamily\thepage}%
    \renewcommand{\headrulewidth}{0pt}%
    \renewcommand{\footrulewidth}{0.4pt}%
  }%
  \pagestyle{normal}%
}
% Cover page: logo, title, release and date; no author line (the logo brands it)
\renewcommand{\sphinxmaketitle}{%
  \let\sphinxrestorepageanchorsetting\relax
  \ifHy@pageanchor\def\sphinxrestorepageanchorsetting{\Hy@pageanchortrue}\fi
  \hypersetup{pageanchor=false}%
  \begin{titlepage}%
    \let\footnotesize\small \let\footnoterule\relax
    \begingroup
      \def\endgraf{ }\def\and{\& }%
      \pdfstringdefDisableCommands{\def\\{, }}%
      \hypersetup{pdfauthor={\@author}, pdftitle={\@title}}%
    \endgroup
    \noindent\rule{\textwidth}{1pt}\par
    \begin{flushright}%
      \vskip 1em%
      \includegraphics[width=7cm]{cryptnox-logo-dark}\par
      \vskip 2em%
      {\LARGE\py@HeaderFamily \@title \par}%
      \vskip 0.5em%
      {\large\itshape \py@release\releaseinfo \par}%
      \vfill
      {\large \@date \par}%
    \end{flushright}%
    \@thanks
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  \clearpage
  \ifdefined\sphinxbackoftitlepage\sphinxbackoftitlepage\fi
  \if@openright\cleardoublepage\else\clearpage\fi
  \sphinxrestorepageanchorsetting
}
\makeatother
''',
}
