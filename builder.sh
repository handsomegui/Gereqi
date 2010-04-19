#!/bin/sh
# A script

CONTROL="$1"
DEBNAME="$2"
python setup.py clean
python setup.py build

rm -rfv debs/
mkdir -pv debs/DEBIAN
mkdir -pv debs/usr/local/bin
mkdir -pv debs/usr/local/lib/python2.6/dist-packages/gereqi
mkdir -pv debs/usr/share/applications/
mkdir -pv debs/usr/share/pixmaps/

cp -v "$CONTROL"    debs/DEBIAN/
cp -v build/scripts*/*  debs/usr/local/bin/
cp -v build/lib*/gereqi/*   debs/usr/local/lib/python2.6/dist-packages/gereqi/
cp -v gereqi/data/gereqi.desktop    debs/usr/share/applications/
cp -v gereqi/data/gereqi.png    debs/usr/share/pixmaps/

dpkg -b debs/ "$DEBNAME"

