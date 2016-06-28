#!/bin/bash

FILE=/tmp/phogo_users

CREATE_SHORT_OPT="u:p:"
CREATE_LONG_OPT="user:,password:,help"

CLEAN_SHORT_OPT="ah"
CLEAN_LONG_OPT="all,home"

function usage() {
	echo "Usage: phogo create [OPTIONS] num_users"
	echo "       phogo clean"
	echo ""
	echo "phogo create : adds num_users to the system, using the options provided"
	echo "phogo clean  : removes the users added by create"
	echo ""
	echo "OPTIONS for create:"
	echo "  -u, --user       The name given to the users (default: tortoise). It will be appended with an ordinal."
	echo "  -p, --password   The password for the users added (default: crm-uam)"
}

function create() {

	if [ -f $FILE ]; then
		echo "There are probably phogo users in this system already."
		echo "  Use or remove them before adding new ones."
		echo "  Or delete the file $FILE if they don't exist anymore."
		exit 1
	fi
	
	echo "$T_USER" >> $FILE

	for i in $(seq $NUM_USERS); do
		echo -e "\n\n\n\n\n\n\n" | adduser $T_USER$i
		echo -e "$T_PASS\n$T_PASS" | passwd $T_USER$i

		#adding PYTHONPATH
		echo -e "\nexport PYTHONPATH=$(pwd)/pylib:$PYTHONPATH" >> "/home/$T_USER$i/.profile"
	done
}

function del_users_starting_by() {
	local PREFIX=$1
	local res=0 

	for user in $(awk -F':' '{ print $1}' /etc/passwd | grep -e ^"$PREFIX"); do
		deluser --remove-home $user
		let "res &= $?"
	done
	return $res
}

function delete() {

	local all_OK=0

	if ! [ -f $FILE ]; then
		echo "No users created by phogo on this system"
		exit 0
	fi

	while IFS='' read -r line || [[ -n "$line" ]]; do
    	del_users_starting_by "$line"
    	let "all_OK &= $?"
	done < "$FILE"

	if [ $all_OK ]; then
		rm "$FILE"
	else
		echo "Some users were not removed from the system."
	fi
}

if [ "$(id -u)" != "0" ]; then
	echo "This script must be run as root" 1>&2
	exit 1
fi

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

	echo "T_USER: $T_USER, T_HOME: $T_HOME, T_PASS: $T_PASS, NUM_USERS: $NUM_USERS"

elif [ "$1" == "clean" ]; then

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

else
	usage
fi

