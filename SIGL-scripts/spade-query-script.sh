#!/bin/bash

debug=0
spade_bin="./bin/spade"
spade_cfg="./cfg/spade.client.Control.config"
query_file="./cfg/spade.client.CommandLine.config"

clear_spade_cfg(){
  truncate -s 0 "${spade_cfg}"
}

clear_postgresql_storage(){
  ./bin/manage-postgres.sh clear
}


is_spade_running(){
  "${spade_bin}" status | grep -q "Running"
}


stop_spade(){
  "${spade_bin}" stop
}


kill_spade(){
  "${spade_bin}" kill
}


try_stop_kill_spade(){
  #if is_spade_running; then
   # stop_spade
  ##fi
  #sleep 5
  if is_spade_running; then
    kill_spade
  fi
}

start_spade(){
  "${spade_bin}" start
}


send_spade_command(){
  local cmd="${1}"
  echo "${cmd}" | "${spade_bin}" control
  if [ "${debug}" -eq 1 ]; then
  echo "list all" | "${spade_bin}" control
  fi
}

send_query_command(){
  local cmd="${1}"
  echo "${cmd}" | "${spade_bin}" query
  if [ "${debug}" -eq 1 ]; then
  echo "list all" | "${spade_bin}" query
  fi
}


query_writer(){
  query="${1}"
  echo $query >> $query_file
}

check_file_path(){
  local file_path="${1}"
  if [ -f "$file_path" ]; then
   echo false
  else
   echo true
  fi
}


display_help() {
  echo "Usage: ./spade-query-script.sh [Number of Logs] [Software] [Executable Path]"
  echo "This script convert logs using SPADE. Make sure to set up SPADE first."
  echo
  echo "OPTIONS:"
  echo "  -h, --help     Display this help message and exit."
  echo "  -l             List the available software."
  echo
  echo "Arguments:"
  echo "  Number of Logs   Specify the number of logs you want to convert into SIGs."
  echo "  Software         Specify the software for which you want to convert the log."
  echo "  Executable Path  Specify the executable path of the software."
  echo
  echo "Examples:"
  echo "  ./spade-query-script.sh 10 onedrive /usr/bin/onedrive"
}

is_number() {
  if [[ $1 =~ ^[0-9]+$ ]]; then
    echo true
  else
    echo false
  fi
}


parse_commands() {
  total_arguments=$#

  if [[ $total_arguments == 1 && ( $1 == "-h" || $1 == "--help" ) ]]; then
    display_help
  elif [[ $total_arguments == 3 && $(is_number "$1") == "true" ]]; then
    main_function "$1" "$2" "$3"
  elif [[ $total_arguments == 1 && $1 == "-l" ]]; then
    echo -e "Available Softwares:\nOnedrive\nSlack\nSkype\nTeamviewer\nFilezilla\nDropbox\n7zip\nShotcut\nPwsafe\nWinrar\nFirefox"
  else
    # Unrecognized option or argument
    echo "Error: Incorrect arguments passed"
    echo "Use './spade-query-script.sh --help' to display the help message."
    exit 1
  fi
}



main_function() {
  local itr=$1
  local name=$2
  local exec_path=$3

  dir_path="/home/vagrant/sigl_json/"

  # Check if the directory exists
  if [ ! -d "$dir_path" ]; then
    # Directory does not exist, create it
    mkdir -p "$dir_path"
    echo "Directory created: $dir_path"
  else
    echo "Directory already exists: $dir_path"
  fi


  for ((i=1; i<=$itr; i++))
  do
    res=$(check_file_path "/home/vagrant/sigl_logs/$name-audit-$i.log")
    if [ $res == "true" ]; then
      echo "File $name-audit-$i.log does not exist"
      continue
    fi

    cd /home/vagrant/SPADE
    echo "Clearing SPADE config"
    clear_spade_cfg
    sleep 4
    echo "Clearing SPADE manage-postgres"
    clear_postgresql_storage
    sleep 10

    start_spade

    echo "Running SPADE Control"
    send_spade_command "add analyzer CommandLine"
    send_spade_command "add storage PostgreSQL"
    send_spade_command "add filter VersionProcess position=1 versionAnnotationName=VOR_version initialVersion=0 edgeAnnoKey=vor_edge_type edgeAnnoValue=vor_versioning"
    send_spade_command "add reporter Audit inputLog=/home/vagrant/sigl_logs/$name-audit-$i.log"
    send_spade_command "exit"
    send_query_command "set storage PostgreSQL"

    sleep 45

    send_query_command "%file_name = \"path\" == '$exec_path'"
    send_query_command "\$file_v = \$base.getVertex(%file_name)"
    send_query_command "\$lineage_count = \$base.getLineage(\$file_v, 10,'a')"

    sleep 30

    query_writer "list"
    query_writer "export > /tmp/$name-$i.json"
    query_writer "dump all \$lineage_count"

    sleep 10

    send_query_command "exit"

    echo "Stopping SPADE"
    stop_spade

    sleep 15

    cd /home/vagrant/
    cp /tmp/$name-$i.json  /home/vagrant/sigl_json/
  done
}

#main_function $@
parse_commands $@
