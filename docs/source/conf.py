# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path -------------------------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Work Time Tracker'
copyright = '2023, Uras Ayanoglu, Sebastian Sopola, Jan-Krister Helenius'
author = 'Uras Ayanoglu, Sebastian Sopola, Jan-Krister Helenius'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    #'sphinxcontrib.plantuml' # This line supposedly enables plantuml , but it doesn't work
]

# This is the plantuml path on my computer, after installing plantumlyou should change it to yours
#plantuml = 'java -jar /home/uras/plantuml/plantuml.jar'

autodoc_mock_imports = ['tkcalendar', 'userdatabase', 'day_stats', 'work_day']


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
