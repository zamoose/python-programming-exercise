#!/usr/bin/python
#
# proximityscan.py
# Author: Doug Stewart
#
# Simplistically scan through a directory of files
# and scan the files for two words found within a certain
# context or proximity.
#
import argparse
import os.path
import sys
import string

from os import walk

# Parse command line arguments.
parser = argparse.ArgumentParser(prog='proximityscan.py',description='Scan supplied file for words within +/- N words of each other.')
parser.add_argument('dir',
                    help="The directory containing files to scan for strings in context.")
parser.add_argument('word1',
                    help="The first word to scan a file for.")
parser.add_argument('word2',
                    help="The second word to scan a file for.")
parser.add_argument('proximity', type=int,
                    help="The number of words, +/- that word1 and word2 should be within.")
parser.add_argument('-v', '--verbose', action='store_const', const=1,
                    help="Display verbose findings.")

args = parser.parse_args()
searchdir = args.dir
searchw1 = args.word1.lower()
searchw2 = args.word2.lower()
searchprox = args.proximity
verbose = args.verbose
matched_files = 0

if verbose:
    print "\nSearching files in '{}' containing '{}' and '{}' at a word-distance of {}.\n".format(searchdir,searchw1,searchw2,searchprox)

## Define some methods

# Get a list of files in the directory in question
def get_files(dirname):
    f = []
    for (dirpath, dirnames, filenames) in walk(dirname):
        f.extend(filenames)

    # Prepend the dirname to the filenames before we return our list of files.
    g = [dirname + '/' + x for x in f]
    return g

# Yield a list of tokenized words, all lower-cased,
# all stripped of (most punctuation).
def words(strings):
    stream = iter(strings)
    for line in stream:
        for word in line.split():
            transword = word.translate(None, string.punctuation)
            yield transword.lower()

# Get a list of the files to scan
searchfiles = get_files(searchdir)

# Iterate through the files
for scanfile in searchfiles:
    file_index = []
    localmatch = 0

    if verbose:
        print "Scanning {}: \n".format(scanfile)

    # Open the file to be scanned
    with open(scanfile, 'r') as stream:
        # Stream through the file and create an index
        # of words
        for word in words(stream):
            file_index.append(word)

    # Look for the specified words in the files and save their respective
    # indices if found in a list.
    word1indexes = [i for i, x in enumerate(file_index) if x == searchw1]
    word2indexes = [i for i, x in enumerate(file_index) if x == searchw2]

    # Iterate through the search indices
    for x in word1indexes:
        for y in word2indexes:
            if abs(x-y) <= searchprox:
                matched_files += 1
                if verbose:
                    print "'{}' matched! Found '{}' and '{}' at words {}, {}, within proximity of {}.\n"\
                        .format(scanfile, searchw1, searchw2, x, y, searchprox)
                else:
                    if not localmatch:
                        print scanfile
                        localmatch += 1

# Exit with proper return codes to indicate success
# or failure.
if matched_files:
    sys.exit()
else:
    sys.exit(1)
