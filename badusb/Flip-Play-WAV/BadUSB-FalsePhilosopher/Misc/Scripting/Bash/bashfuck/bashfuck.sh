#!/bin/bash

usage(){
    echo "usage: $0 [-h] [-t] [-b] cmd" >&2
}

_help() {
    echo "encode a bash command with charset $()#!{}<\'," >&2
    echo "" >&2
    echo "positional arguments:" >&2
    echo "  cmd" >&2
    echo "" >&2
    echo "optional arguments:" >&2
    echo "  -h, --help  show this help message and exit" >&2
    echo "  -t, --test  test bashfuck and output result" >&2
    echo "  -b, --bash  leaves the default bash string using [bash] chars, but avoids" >&2
    echo "              the usage of \"!\" and uses one byte less. always works." >&2
}

join_by() { local IFS="$1"; shift; echo "$*"; }

n=( )
n[0]="\$#"
n[1]="\${##}"
n[2]="\$((${n[1]}<<${n[1]}))"
n[3]="\$((${n[2]}#${n[1]}${n[1]}))"
n[4]="\$((${n[1]}<<${n[2]}))"
n[5]="\$((${n[2]}#${n[1]}${n[0]}${n[1]}))"
n[6]="\$((${n[2]}#${n[1]}${n[1]}${n[0]}))"
n[7]="\$((${n[2]}#${n[1]}${n[1]}${n[1]}))"

str_to_oct() {
    # Converts a string to its octal representation, enclosed in: $\'STR\'

    s="\$\\'"

    for ((i=0; i<${#1}; i++))
    do
        char="${1:$i:1}"
        oct=$(printf "%03o" \'"${char}")

        e="\\\\"
        for ((j=0; j<${#oct}; j++))
        do
            e+="${n[${oct:$j:1}]}"
        done
        s+="${e}"
    done

    s+="\\'"

    echo "${s}"
}

arg_to_cmd() {
    # Given an array of strings returns the octal representation of every single string,
    # wrapped in '{}' and separated by ','

    for str in "$@"
    do
        OCTAL_STRING_ARR+=( $(str_to_oct "${str}") )
    done

    echo "{$(join_by , "${OCTAL_STRING_ARR[@]}")}"
}

encode(){
    # Given a command returns the bashfuck'd version of it
    CMD=$1
    USE_DEFAULT_BASH_STR=$2

    if [[ ${USE_DEFAULT_BASH_STR} -eq 1 ]]
    then
        SHELL_STR='bash'
    else
        SHELL_STR="\${!#}"
    fi

    ARG=('bash' '-c' "${CMD}")
    ENCODED_CMD=$(arg_to_cmd "${ARG[@]}" )

    PAYLOAD="${SHELL_STR}<<<${ENCODED_CMD}"
    echo "${PAYLOAD}"
}

main(){
    TEST_MODE=0
    USE_DEFAULT_BASH_STR=0

    while [[ "$#" -gt 0 ]]
    do
      case "$1" in
        -b|--bash) USE_DEFAULT_BASH_STR=1; shift 1;;
        -t|--test) TEST_MODE=1; shift 1;;
        -h|--help) usage; echo >&2; _help; exit 1;;
        -*) usage; echo "Unknown option: $1" >&2; exit 1;;
        *) CMD="$*"; break;;
      esac
    done

    if [[ -z "${CMD}" ]]
    then
        usage
        echo "Missing required parameter: cmd" >&2
        exit 1
    fi

    PAYLOAD=$(encode "${CMD}" ${USE_DEFAULT_BASH_STR})
    echo "cmd: \`${CMD}\`"
    echo "result (${#PAYLOAD} byte): ${PAYLOAD}"

    if [[ ${TEST_MODE} -eq 1 ]]
    then
        # Runs a bashfuck'd command
        /bin/bash -c "${PAYLOAD}"
    fi

    exit 0
}

main "$@"