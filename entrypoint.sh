#!/usr/bin/env sh

set -e

printf "The Stockfish software is licensed under GPL v3.
The full source code for the version of the software used in this project can be found here:
https://github.com/official-stockfish/Stockfish/tree/sf_16.1
The following is its license text:\n"

cat /usr/share/doc/stockfish/COPYING

printf "\n"

exec "$@"
