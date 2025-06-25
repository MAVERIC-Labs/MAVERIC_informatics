project = 'MAVERIC Informatics'
author = 'Benjamin Bolduc'
release = '1.0.0'
copyright = '2019, Benjamin Bolduc'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',     # Auto-generate documentation from docstrings
    'sphinx.ext.napoleon',    # Support for Google/NumPy-style docstrings
    'sphinx.ext.viewcode',    # Adds "view source" links
    'myst_parser',            # Optional Markdown (.md) support
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # 'nature' 'sphinx_rtd_theme'
html_static_path = ['_static']

language = 'en'

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'