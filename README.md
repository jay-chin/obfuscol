obfuscol
=======

Obfuscate hostname columns in CSV files. Typical use case is for heavily regulated organizations (e.g. Banks) that have a security requirement to obfuscate any internal hostnames in files that are sent to 3rd party vendors for analysis or debugging.


Usage
-----

Obfuscate file test.csv into output.csv. We specify the hostname column with the -c switch and resulting map.json file with -j.

    python obfuscol.py -b -i test.csv -o output.csv -c 2 -j map.json

Restore obfuscated file from mappings in map.json

    python obfuscol.py -r -i output.csv -o result.csv -c 2 -j map.json

Use the -e switch to ignore CSV files that have headers (first line) in them

    python obfuscol.py -b -i test.csv -o output.csv -c 2 -j map.json -e



