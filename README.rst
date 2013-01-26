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


You'll end up with something like this::

    Code Ownership (top 25 users by lines of code)
    ----------------------------------------------------------------------------------
    1  dcramer              71734        19.3%
    2  anton                47572        12.8%
    3  ben                  47135        12.7%
    4  joshua               33467        9.0%
    5  brett                20320        5.5%
    6  dz                   17809        4.8%
    7  jason                15267        4.1%
    8  chris                13780        3.7%
    9  george               11427        3.1%
    10 gab                  11316        3.0%
    11 ted                  10675        2.9%
    12 daniel               8753         2.4%
    13 jeff.pollard         8254         2.2%
    14 byk                  7816         2.1%
    15 steven               7483         2.0%
    16 andrew               6530         1.8%
    17 devin                6089         1.6%
    18 mike                 5913         1.6%
    19 matt                 3627         1.0%
    20 john                 2661         0.7%
    21 dlorenc              2430         0.7%
    22 karen                2381         0.6%
    23 vagrant              1658         0.4%
    24 adam                 1598         0.4%
    25 sean                 1250         0.3%

    File Ownership (top 25 files by number of lines)
    ----------------------------------------------------------------------------------
    1  ..emplates/embed/next/views.js      ben                  3840         63.4%
    2  ..squs/media/styles/global.css      jason                3523         94.3%
    3  ../src/embed/custom/actions.js      anton                2995         90.0%
    4  ..lounge/theme/less/theme.less      anton                2836         75.6%
    5  ..squs/media/css/next/home.css      joshua               2814         95.3%
    6  ..us/media/css/next/global.css      joshua               2581         100.0%
    7  ..edia/js/tests/next/lounge.js      ben                  2573         38.3%
    8  ..rc/embed/next/embed-ender.js      ben                  2553         92.7%
    9  ../disqus/media/css/admin2.css      dcramer              2329         99.9%
    10 ..disqus/media/css/landing.css      joshua               2149         100.0%
    11 ..a/js/src/embed/next/vglnk.js      gab                  2114         100.0%
    12 ..us/media/css/invite-next.css      joshua               2035         100.0%
    13 ..es/dtpl/defaults.toolbar.css      ben                  1986         83.9%
    14 ..squs/disqus/forums/models.py      dcramer              1975         39.0%
    15 ..qus/contrib/BeautifulSoup.py      andrew               1864         91.6%
    16 ..styles/v3/dc-application.css      daniel               1818         76.3%
    17 ../sexyapi/controller/tests.py      dcramer              1788         84.0%
    18 ..dia/styles/dtpl/defaults.css      ben                  1772         71.7%
    19 ..t/disqus/media/css/admin.css      chris                1749         72.8%
    20 ..ia/js/src/host/commentbox.js      george               1553         74.0%
    21 ..squs/forums/api/endpoints.py      dcramer              1451         75.7%
    22 ..media/less/layouts/home.less      steven               1307         91.4%
    23 ..n/disqus/admin/json/tests.py      devin                1251         88.0%
    24 ..a/css/v5/admin/analytics.css      ben                  1239         95.7%
    25 ../media/css/next/override.css      joshua               1238         100.0%
