git-owners
==========

A script which scrapes your git repositories (locally) and shows you statistics on the amount of ownership
individuals have over coded (e.g. git blame).

Usage:

::

    python generate.py path/to/repo path/to/other/repo

You can also pass numerous options, but you'll likely want consisten options, so stick them in a JSON file:

::

    {
        "include": ["*.php", "*.java", "*.c", "*.h", "*.py", "*.js", "*.html", "*.less", "*.css"],
        "exclude": ["media/js/src/lib/*", "*.min.js", "media/build/*", "media/js/tests/externals/*"],
        "aliases": {
            "david@disqus.com": "dcramer@gmail.com"
        },
        "drop_domains": true
    }

And pass them as --config::

    python generate.py path/to/repo --config=disqus.json
