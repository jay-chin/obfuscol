import random
import csv
import string
import json
import argparse
import sys

# https://github.com/pereorga/csvshuf/blob/master/setup.py
rot13 = lambda x: x.encode('rot_13')  # Hail Caeser !

def randomize_chars(word):
    '''
    Replace characters a-zA-Z with a random lowercase character. 
    '''
    charset = string.ascii_lowercase
    res = []
    for char in word:
        if char.isalpha(): # We only randomize letters, retain the rest
            res.append(random.choice(charset))
        else:
            res.append(char)
    return ''.join(res)

def obfs_word(word, encode_func=randomize_chars):
    '''
    obfuscate word with using an encoding function
    '''
    return encode_func(word) 

def obfs_host(hostname, obfs_domain=False):
    '''
    obfuscate hostname
    '''
    if not hostname:
        return 'Null'

    if obfs_domain or '.' not in hostname:
        return obfs_word(hostname)
    else:
        hostname, domain = hostname.split('.', 1)
        return ".".join([obfs_word(hostname), domain])

def obfs_file(infile, outfile, hostcol, csvheader=False):
    '''
    Reads csv data from infile, obfuscates host column and 
    writes it to outfile.
    Returns a json mapping file that maps hostname to its
    obfuscated hostname
    '''
    host_mapping = dict() 
    with open(infile, 'r') as csvfile, open(outfile, 'w') as resfile:
        datareader = csv.reader(csvfile, delimiter=',')
        if csvheader: # Don't obfuscate first header row
            resfile.write(','.join(datareader.next()) + '\n')
        for row in datareader:
            hostname = row[hostcol]
            try: # Get obfuscated hostname from mapping cache
                obfs_hostname = host_mapping[hostname]
            except KeyError:
                obfs_hostname = obfs_host(hostname)
                host_mapping[hostname] = obfs_hostname
            row[hostcol] = obfs_hostname
            resfile.write(','.join(row) + '\n')
    return host_mapping

def restore_file(obfsfile, outfile, mappingfile, hostcol, csvheader=False):
    '''
    Restore obfuscated hostname file to outfile from
    the json mapping file
    '''
    with open(mappingfile, 'r') as jsonfile:
        jsonmap = json.load(jsonfile) 

    # Reverse the map so we have keys = obfuscated hostname
    host_mapping = { v: k for k, v in jsonmap.iteritems() }

    with open(obfsfile, 'r') as infile, open(outfile, 'w') as resfile:
        datareader = csv.reader(infile, delimiter=',')
        if csvheader: # Leave header line as is 
            resfile.write(','.join(datareader.next()) + '\n')
        for row in datareader:
            obfsname = row[hostcol]
            try: # Get obfuscated hostname from mapping cache
                row[hostcol] = host_mapping[obfsname]
            except KeyError:
                print("Unable to match %s to hostname in map file"  \
                        % obfsname)
                row[hostcol] = obfsname
            resfile.write(','.join(row) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Obfuscate hostnames in a CSV file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', action='store_true', dest='obfuscate',
                        help='Obfuscate mode' )
    group.add_argument('-r', action='store_true', dest='restore',
                        help='Restore mode' )
    parser.add_argument('-i', action='store', dest='infile', required=True,
                        help='Input file in csv format')
    parser.add_argument('-o', action="store", dest="outfile", required=True,
                        help='Output file in csv format')
    parser.add_argument('-c', action="store", dest="host_col",
                        type=int, required=True,
                        help='Column/Field number that corresponds to hostnames ')
    parser.add_argument('-j', action="store", dest="map_file", required=True,
                        help='Mapping file in json format')
    parser.add_argument('-e', action="store_true", dest="csv_header",
                        default=False,
                        help='Input file contains CSV header fields')
    args = parser.parse_args()

    if not args.obfuscate and not args.restore:
        print "You need to specify a mode : obfuscate(-b) or restore(-r)"
        sys.exit(1)

    if args.obfuscate:
        # Humans starts column count with 1
        # csv reader column count starts from 0
        print "Creating obfuscated csv file : %s" % args.outfile
        host_mapping = obfs_file(args.infile, args.outfile, 
                                args.host_col - 1, csvheader=args.csv_header)

        # Write mapping file        
        with open(args.map_file, 'w') as mapfile:
            print "Generating map file to : %s" % args.map_file
            json.dump(host_mapping, mapfile)
    elif args.restore:
        print "Restoring %s from mapfile %s" % (args.outfile, args.map_file)
        restore_file(args.infile, args.outfile, args.map_file, 
                    args.host_col - 1, csvheader=args.csv_header)

if __name__ == '__main__':
    main()


