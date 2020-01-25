#!/bin/bash
PROXY=$([ "$(hostname)" == "deathstar" ] && echo "gamma.ndr.md" || echo "localhost")

# Squash all HTML for each URL into a single line, streaming fashion
# It also prefixes with the URL

page_per_line () {
  curl -s --connect-to "::${PROXY}:8080" $1 | tr -d "\n\r" | tr -d '\n' | sed "s/^/$0 /" | sed -e '/.$/a\'
}

export -f page_per_line

# xargs:
# add `-t` for debugging
cat ./urls.txt | xargs -0 -d '\n' -n 1 bash -c 'page_per_line "$@"'
