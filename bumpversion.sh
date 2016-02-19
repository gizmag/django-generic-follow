#!/bin/sh
set -e
cd "${0%/*}"
OLD="$( python setup.py --version )"
NEW="$( git rev-parse --abbrev-ref HEAD | cut -d / -f 2 )"
echo "Bumping version ${OLD} -> ${NEW}...\n"
sed -e "s/^    version='${OLD}'/    version='${NEW}'/" setup.py > .setup.py
mv .setup.py setup.py
git diff setup.py
