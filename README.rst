docs.json
=========

``docs.json`` is a format for indexing documentation content.

It will be used as an interchange format for documentation content between services.
The main goal is to maintain a search index,
so the format must include full text content.
It also maintains metadata that can be used for faceting the results.

Field Explanations
------------------

* ``title`` - The Title of the page. A string that contains a human readable title.
* ``slug`` - The slug of a page, generally used for URLs. Should be alphanumeric with dashes for sperators.
* ``url`` - The canonical URL for the page content.
* ``language`` - The language code for the content. As specified by http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes.
* ``content`` - The HTML content of the page. Stripped of any non-content markup.
* ``sections`` - The HTML content of the main sections of a page. The section content should include all relevent HTML that could be included in the ``content`` section. 
* ``tags`` - The Tag data associated with the page. This will be used for faceting.
* ``translations`` - Versions of this document translated into another language.

``content`` or ``sections`` are required,
depending on the granularity of your content.

Structure
---------

The general idea is there will be an endpoint that returns this data for a specific URL::

    GET /api/docs_json/?url=https://www.pip-installer.org/en/latest/installation-instructions.html

It might also be implemented as a .json extension on a documentation page::

    GET https://www.pip-installer.org/en/latest/installation-instructions.html.json

Discovery
---------

If you want your ``docs.json`` file to be easily discovered,
you should place a reference to it in your HTML page::

    <link rel="docs.json" href="https://www.pip-installer.org/en/latest/installation-instructions.html.json">
    <link rel="docs.json" href="https://readthedocs.org/api/docs_json/?url=https://www.pip-installer.org/en/latest/installation-instructions.html">

Example
-------

Page Object
~~~~~~~~~~~

::

    {
        "title": "Installation Instructions",
        "slug": "installation-instructions",
        "url": "https://www.pip-installer.org/en/latest/installation-instructions.html",
        "language": "en",
        "content": "HTML",
        "sections": {
            "Install": {
                "slug": "install",
                "content": "HTML",
            }
            "With Setuptools": {
                "slug": "with-setuptools",
                "content": "HTML",
            }
            "With Setuptools": "<html..",
        }
        "tags": [
            "pip",
            "python",
            "installer",
        ],
        "translations" {
            "en": "http://pip.readthedocs.org/en/latest/installation-instructions.html",
            "es": "http://pip.readthedocs.org/es/latest/installation-instructions.html",
        }
    }


