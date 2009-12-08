#!/bin/sh
FILE="$1"

BLOCKS=$(metaflac --list --block-type=VORBIS_COMMENT "$FILE" | grep "METADATA block #" | cut -d"#" -f2 | tr '\n' ' ')
CNT=$(echo "$BLOCKS" | tr -d " \n" | wc -c)

if [ "$CNT" -gt 1 ]
then
    EXTRAS=$(echo "$BLOCKS" | cut -d" " -f 2- | rev)
else
    echo "Nothing to be done."
    exit
fi

for NUM in $EXTRAS
do 
    metaflac --preserve-modtime --remove --block-number="$NUM" "$FILE"
done
