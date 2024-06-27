#!/bin/bash

set -euxo pipefail

OUTPUT_ZIP="broadcastdates.zip"

mkdir -p _build
rm -Rf _build/broadcastdates
mkdir -p _build/broadcastdates
cp __init__.py  _build/broadcastdates/

#rm _build/"$OUTPUT_ZIP"
(cd _build && zip "$OUTPUT_ZIP"  broadcastdates/*)
