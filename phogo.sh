#!/bin/bash

FILE=/tmp/phogo_users

CREATE_SHORT_OPT="u:h:p:"
CREATE_LONG_OPT="user:,home:,password:,help"

CLEAN_SHORT_OPT="ah"
CLEAN_LONG_OPT="all,home"

function usage() {
	echo "Usage: phogo create [OPTIONS] num_users"
	echo "       phogo clean [OPTIONS]"
	echo ""
	echo "OPTIONS for create:"
	echo "  -u, --user       The name given to the users (default: tortoise). It will be appended with a number."
	echo "  -h, --home       Directory to use as $HOME for the users added (default: /home/<user>)"
	echo "  -p, --password   The password for the users added (default: crm-uam)"
	echo ""
	echo "OPTIONS for clean:"
	echo "  -a, --all        Remove everything created (users, home, temporary files)"
	echo "  -h, --home       Keep $HOME directory, don't remove it."
}

function create() {

	if [ -f $FILE ]; then
		read -p "A previous run has left some users undeleted. Continue? " -n 1 -r
		echo    # (optional) move to a new line
		if ! [[ $REPLY =~ ^[Yy]$ ]]; then
			exit 0
		fi
	fi
	
    # do dangerous stuff
	echo "HOME:$T_HOME" >> $FILE

	for i in $(seq $NUM_USERS); do
		echo "USER:$T_USER$i" >> $FILE
		echo -e "\n\n\n\n\n\n" | adduser --disabled-password --home "$T_HOME" $T_USER$i
		echo -e "$T_PASS\n$T_PASS" | passwd $T_USER$i
	done
}

function delete() {

	if ! [ -f $FILE ]; then
		echo "No users created by phogo on this system"
		exit 1
	fi

}

if [ "$1" == "create" ]; then

	shift

	TEMP=$(getopt -o $CREATE_SHORT_OPT -l $CREATE_LONG_OPT -- $@)
	eval set -- "$TEMP"

	while true; do
		case "$1" in
			-u|--user)
				echo "user: $2" >&2
				T_USER=$2
				shift 2
				;;
			-h|--home)
				echo "home: $2" >&2
				T_HOME=$2
				shift 2
				;;
			-p|--password)
				echo "password: $2" >&2
				T_PASS=$2
				shift 2
				;;
			--)
				echo "num_users: $2" >&2
				NUM_USERS="$2"
				break
				;;
			*)
				echo "Invalid option: $1"
				usage
				exit 1
				;;
		esac
	done

	[[ $T_USER != "" ]] || T_USER="tortoise"
	[[ $T_PASS != "" ]] || T_PASS="crm-uam"
	[[ $T_HOME != "" ]] || T_HOME="/home/"$T_USER
	re='^[0-9]+$'
	if ! [[ $NUM_USERS =~ $re ]] ; then
		echo $NUM_USERS
		echo "error: Not a number" >&2;
		exit 1
	fi

	create

fi


echo "T_USER: $T_USER, T_HOME: $T_HOME, T_PASS: $T_PASS, NUM_USERS: $NUM_USERS"

if [ "$1" == "clean" ]; then

	shift

	TEMP=$(getopt -o $CLEAN_SHORT_OPT -l $CLEAN_LONG_OPT -- $@)
	eval set -- "$TEMP"

	while true; do
		case "$1" in
			-a|--all)
				KEEP_HOME=false
				;;
			-h|--home)
				KEEP_HOME=true
				;;
			--)
				break
				;;
			*)
				echo "Invalid option: $1"
				usage
				exit 1
				;;
		esac
	done

	delete

fi

if [ "$(id -u)" != "0" ]; then
	echo "This script must be run as root" 1>&2
	exit 1
fi


