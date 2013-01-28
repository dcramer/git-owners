from __future__ import division

from fnmatch import fnmatch
from collections import defaultdict
import cPickle
import json
import os
import subprocess
import sys

DEFAULT_INCLUDE = ['*.php', '*.java', '*.c', '*.h', '*.py', '*.js', '*.html', '*.less', '*.css', '*.m']
DEFAULT_BRANCH = 'master'


def scrape(root='.', branch=None):
    if branch is None:
        branch = 'master'

    # filename -> author -> # lines
    files = defaultdict(lambda: defaultdict(int))

    for filename in subprocess.check_output(['git', 'ls-tree', '--full-tree', '--name-only', '-r', branch],
            cwd=root).splitlines():
        filename_lower = filename.lower()

        # exclude binary filetypes
        if filename_lower.endswith(('.png', '.jpeg', '.jpg', '.gif', '.icon', '.jar', '.ttf')):
            continue

        sys.stdout.write('.')
        try:
            result = subprocess.check_output(['git', 'blame', '--line-porcelain', filename],
                cwd=root)
        except Exception, e:
            if getattr(e, 'returncode', None) != 128:
                print 'Error:', e
            continue

        for line in result.splitlines():
            if line.startswith('author-mail'):
                email = line.split('author-mail <', 1)[-1][:-1]
                files[filename][email] += 1

    return dict((k, dict(v)) for k, v in files.iteritems())


def main(argv=None):
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('--reset', dest='reset', action='store_true', default=False)
    parser.add_option('--config', dest='config_name')
    parser.add_option('--cache-name', dest='cache_name', default='.gitowners-cache')
    parser.add_option('--exclude', dest='exclude', action='append', default=())
    parser.add_option('--include', dest='include', action='append', default=DEFAULT_INCLUDE)
    parser.add_option('--branch', dest='branch')
    parser.add_option('--drop-domains', dest='drop_domains', action='store_true', default=True,
        help='Remove domains from email addresses.')

    (options, args) = parser.parse_args(argv)

    if not args:
        paths = ['.']
    else:
        paths = args

    options.aliases = {}
    if options.config_name:
        with open(options.config_name) as fp:
            for key, value in json.loads(fp.read()).iteritems():
                setattr(options, key, value)

    # sum of all lines owned by a user
    # username -> number of lines
    user_stats = defaultdict(int)

    # the user who owns the most lines in a file
    # filename -> (username, number of lines)
    file_stats = defaultdict(int)

    # number of lines in a file
    # filename -> number of lines
    file_lines = defaultdict(int)

    print

    for path in paths:
        cache_path = os.path.join(path, options.cache_name)

        path_stats = None
        if not options.reset and os.path.exists(cache_path):
            path_stats = cPickle.load(open(cache_path))

        if not path_stats:
            print 'Generating statistics for %r' % (path,)

            path_stats = scrape(
                root=path,
                branch=options.branch,
            )
            cPickle.dump(path_stats, open(cache_path, 'w'))
        else:
            print 'Using cache for %r' % (path,)

        for filename, user_list in path_stats.iteritems():
            filename_lower = filename.lower()

            if options.include and not any(fnmatch(filename_lower, p) for p in options.include):
                continue

            if any(fnmatch(filename_lower, p) for p in options.exclude):
                continue

            # coerce aliases
            for email in user_list.keys():
                new_email = email
                if email in options.aliases:
                    new_email = options.aliases[email]
                if options.drop_domains:
                    new_email = new_email.split('@', 1)[0]

                if new_email != email:
                    if new_email not in user_list:
                        user_list[new_email] = 0
                    user_list[new_email] += user_list.pop(email)

            for email, lines_owned in user_list.iteritems():
                user_stats[email] += lines_owned

            full_path = os.path.join(path, filename)
            file_stats[full_path] = sorted(user_list.items(), key=lambda x: -x[-1])[0]
            file_lines[full_path] = sum(path_stats[filename].itervalues())

    print
    print "Code Ownership (top 25 users by lines of code)"
    print "-" * 100

    total_lines = sum(user_stats.itervalues())
    for num, (user, lines_owned) in enumerate(sorted(user_stats.items(), key=lambda x: -x[-1])[:25]):
        percent = lines_owned / total_lines * 100
        print "%-2d %-20s %-12s %.1f%%" % (num + 1, user, lines_owned, percent)

    def trim(filename):
        if len(filename) > 30:
            return '..%s' % filename[-28:]
        return filename

    print
    print "File Ownership (top 25 files by number of lines)"
    print "-" * 100
    for num, (filename, (user, lines_owned)) in enumerate(sorted(file_stats.iteritems(), key=lambda x: -x[-1][-1])[:25]):
        percent = lines_owned / file_lines[filename] * 100
        print "%-2d %-35s %-20s %-12s %.1f%%" % (num + 1, trim(filename), user, lines_owned, percent)


if __name__ == '__main__':
    main()
