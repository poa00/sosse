#!/usr/bin/bash
set -e
CODE_BLOCK_FILE="$1"
DOC_SRC="$2"

code_length="$(jq --arg SRC "$DOC_SRC" '[.[] | select(.src == $SRC and (.lang == "shell" or .lang == "default"))] | length' < "$CODE_BLOCK_FILE")"

function code_no() {
    jq -r --arg IDX "$1" --arg SRC "$DOC_SRC" '[.[] | select(.src == $SRC and (.lang == "shell" or .lang == "default"))][$IDX|tonumber].code' < "$CODE_BLOCK_FILE"
}

if [ "$code_length" == "0" ]
then
    echo "No step to perform" >&2
    exit 1
fi

block_no=0
while [ "$block_no" -lt "$code_length" ]
do
    code="$(code_no "$block_no")"
    if echo "$code" | grep -q "nano .*"
    then
        filename="$(echo "$code" | sed 's/^nano //')"

        block_no=$(($block_no + 1))
        code_no "$block_no" > "$filename"
    else
        _code="$(echo "$code"|grep -v ^systemctl ||:)"
        if [ "$_code" != "" ]
        then
            IFS=$'\n'; for line in $_code
            do
                echo "----- $line"
                eval "$line"
            done
        fi
    fi
    block_no=$(($block_no + 1))
done
