#!/bin/bash

debug=0
spade_bin="./bin/spade"
spade_cfg="./cfg/spade.client.Control.config"

cmd_bin_logs_dir_path="/home/vagrant/trace_bins"
spade_log_msg_str_that_signals_the_cdm_log_has_been_processed="Finished reading"
dot_output_dir_path="/home/vagrant/trace_dots"


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


install_skype(){
  echo "Installing skype..."
  #wget https://go.skype.com/skypeforlinux-64.deb
  sudo apt install ./skypeforlinux-64.deb -y

  if [ $? -eq 0 ]; then
   echo "Installation of skype was successful."
  else
   echo "Installation of skype for Linux failed."
   exit 1
  fi

  #sudo rm skypeforlinux-64.deb
}

remove_skype(){
  echo "Removing skype..."
  sudo apt remove skypeforlinux -y
  echo "Skype has been removed"
}


install_filezilla(){
  echo "Installing filezilla..."
  sudo apt install filezilla -y

  if [ $? -eq 0 ]; then
   echo "Installation of Teamviewer for Linux was successful."
  else
   echo "Installation of Teamviewer for Linux failed."
   exit 1
  fi

}

remove_filezilla(){
  echo "Removing filezilla..."
  sudo apt remove filezilla -y
  echo "Filezilla has been removed"
}

install_teamviewer(){
  echo "Installing teamviewer..."
  wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb
  sudo apt install ./teamviewer_amd64.deb -y

  if [ $? -eq 0 ]; then
   echo "Installation of Teamviewer for Linux was successful."
  else
   echo "Installation of Teamviewer for Linux failed."
   exit 1
  fi

  sudo rm teamviewer_amd64.deb
}

remove_teamviewer(){
  echo "Remove teamviewer..."
  sudo apt remove teamviewer -y
  sudo apt autoremove teamviewer -y
  echo "Teamviewer has been removed"
}

install_pwsafe(){
  echo "Installing pwsafe..."
  sudo apt install passwordsafe -y
  if [ $? -eq 0 ]; then
    echo "Installation of pwsafe for Linux was successful."
  else
    echo "Installation of pwsafe for Linux failed."
    exit 1
  fi
}

remove_pwsafe(){
  echo "Removing pwsafe..."
  sudo apt remove passwordsafe -y
  sudo apt autoremove -y
  echo "Pwsafe has been removed"
}

install_7zip(){
  echo "Installing 7zip..."
  sudo apt install p7zip-full p7zip-rar -y
  if [ $? -eq 0 ]; then
    echo "Installation of 7zip for Linux was successful."
  else
    echo "Installation of 7zip for Linux failed."
    exit 1
  fi
}

remove_7zip(){
  echo "Removing 7zip..."
  sudo apt remove p7zip -y
  sudo apt autoremove -y
  echo "7zip has been removed"
}

install_dropbox(){
  echo "Installing dropbox..."
  wget -O dropbox.deb https://linux.dropbox.com/packages/ubuntu/dropbox_2019.02.14_amd64.deb
  sudo apt install ./dropbox.deb -y
  if [ $? -eq 0 ]; then
    echo "Installation of dropbox for Linux was successful."
  else
    echo "Installation of dropbox for Linux failed."
    exit 1
  fi
  sudo rm ./dropbox.deb
}

remove_dropbox(){
  echo "Removing dropbox..."
  sudo apt remove dropbox -y
  sudo apt autoremove -y
  echo "Dropbox has been removed"
}


install_firefox(){
  echo "Installing firefox..."
  sudo apt install firefox -y
  if [ $? -eq 0 ]; then
   echo "Installation of firefox for Linux was successful."
  else
   echo "Installation of firefox for Linux failed."
   exit 1
  fi
}

remove_firefox(){
  echo "Removing firefox..."
  sudo apt purge firefox -y
  sudo apt remove firefox
  sudo apt autoremove -y
  echo "Firefox has been removed"
}


install_qbittorrent(){
  echo "Installing qbittorrent..."
  sudo apt install qbittorrent -y
  if [ $? -eq 0 ]; then
   echo "Installation of qbittorrent for Linux was successful."
  else
   echo "Installation of qbittorrent for Linux failed."
   exit 1
  fi
}

remove_qbittorrent(){
  echo "Removing qbittorrent..."
  sudo apt purge qbittorrent -y
  sudo apt remove qbittorrent
  sudo apt autoremove -y
  echo "qbittorrent has been removed"
}

install_geany(){
  echo "Installing geany..."
  sudo apt install geany -y
  if [ $? -eq 0 ]; then
   echo "Installation of geany for Linux was successful."
  else
   echo "Installation of geany for Linux failed."
   exit 1
  fi
}

remove_geany(){
  echo "Removing geany..."
  sudo apt purge geany -y
  sudo apt remove geany
  sudo apt autoremove -y
  echo "geany has been removed"
}

install_gimp(){
  echo "Installing gimp..."
  sudo apt install gimp -y
  if [ $? -eq 0 ]; then
   echo "Installation of gimp for Linux was successful."
  else
   echo "Installation of gimp for Linux failed."
   exit 1
  fi
}

remove_gimp(){
  echo "Removing gimp..."
  sudo apt purge gimp -y
  sudo apt remove gimp
  sudo apt autoremove -y
  echo "gimp has been removed"
}


display_help() {
  echo "Usage: ./test-spade-script.sh [Number of Logs] [Software] [Exec path]"
  echo "This script collects logs using SPADE. Make sure to setup SPADE first."
  echo
  echo "OPTIONS:"
  echo "  -h, --help          Display this help message and exit."
  echo "  -l                  List the available softwares."
  echo
  echo "Arguments:"
  echo "  Number of logs      Specify the number of logs you want to collect."
  echo "  Software            Specify the software for which you want to collect the log."
  echo "  Exec path           Specify the executable path of the software."
  echo
  echo "Examples:"
  echo "  ./test-spade-script.sh 10 onedrive /usr/bin/onedrive"
}

is_number() {
  #val=$(($1))
  if [[ $1 =~ ^[0-9]+$ ]]; then
    echo true
  else
    echo "Argument '$1' is not a number."
    echo false
  fi
}


parse_commands(){
  total_arguments=$#
  if [[ $total_arguments == 1 && $1 == "-h" || $1 == "--help" ]]; then
    display_help
  elif [[ $total_arguments == 3 && $(is_number "$1") == "true" && $2 = @(firefox|Firefox|Gimp|gimp|geany|Geany|skype|Skype|teamviewer|Teamviewer|filezilla|Filezilla|dropbox|Dropbox|"7zip"|pwsafe|Pwsafe|qbittorrent|Qbittorrent) ]]; then
    main_function "$1" "$2" "$3"
  elif [[ $total_arguments == 1 && $1 == "-l" ]]; then
    echo -e "Available Softwares:Skype\nTeamviewer\nFilezilla\nDropbox\n7zip\nGeany\nPwsafe\nQbittorrent\nFirefox\nGimp"
  else
    # Unrecognized option or argument
    echo "Error: Incorrect arguments passed"
    echo "Use './test-spade-script.sh --help' to display the help message."
    exit 1
  fi
}




main_function(){
  local itr=$1
  local name=$2
  local exec_path=$3

  dir_path="/home/vagrant/sigl_logs/"

  # Check if the directory exists
  if [ ! -d "$dir_path" ]; then
    # Directory does not exist, create it
    mkdir -p "$dir_path"
    echo "Directory created: $dir_path"
  else
    echo "Directory already exists: $dir_path"
  fi

  auditctl -b 1000000

  for ((i=1; i<=$itr; i++))
  do
    cd /home/vagrant/SPADE
    echo "Clearing SPADE config"
    clear_spade_cfg
    sleep 2
    echo "Clearing SPADE manage-postgres"
    clear_postgresql_storage
    sleep 2
    start_spade
    echo "Running SPADE Control"
    send_spade_command "add reporter Audit localEndpoints=true namespaces=true IPC=true networkAddressTranslation=true outputLog=/tmp/$name-$i.log"
    sleep 10
    send_spade_command "exit"
    cd /home/vagrant/
    sleep 5
    if [[ $name = @(geany|Geany) ]]; then
      install_geany
    elif [[ $name = @(Gimp|gimp) ]]; then
      install_gimp
    elif [[ $name = @(teamviewer|Teamviewer) ]]; then
      install_teamviewer
    elif [[ $name = @(skype|Skype) ]]; then
      install_skype
    elif [[ $name = @(filezilla|Filezilla) ]]; then
      install_filezilla
    elif [[ $name = @(dropbox|Dropbox) ]]; then
      install_dropbox
    elif [[ $name = @(7zip) ]]; then
      install_7zip
    elif [[ $name = @(qbittorrent|Qbittorrent) ]]; then
      install_qbittorrent
    elif [[ $name = @(pwsafe|Pwsafe) ]]; then
      install_pwsafe
    elif [[ $name = @(firefox|Firefox) ]]; then
      install_firefox
    fi

    sleep 2
    cd /home/vagrant/SPADE
    send_spade_command "remove reporter Audit"
    sleep 20
    echo "Stopping SPADE"
    stop_spade
    sleep 20
    # Remove software installation
    if [[ $name = @(geany|Geany) ]]; then
      remove_geany
    elif [[ $name = @(Gimp|gimp) ]]; then
      remove_gimp
    elif [[ $name = @(teamviewer|Teamviewer) ]]; then
      remove_teamviewer
    elif [[ $name = @(skype|Skype) ]]; then
      remove_skype
    elif [[ $name = @(filezilla|Filezilla) ]]; then
      remove_filezilla
    elif [[ $name = @(dropbox|Dropbox) ]]; then
      remove_dropbox
    elif [[ $name = @(7zip) ]]; then
      remove_7zip
    elif [[ $name = @(qbittorrent|Qbittorrent) ]]; then
      remove_qbittorrent
    elif [[ $name = @(pwsafe|Pwsafe) ]]; then
      remove_pwsafe
    elif [[ $name = @(firefox|Firefox) ]]; then
      remove_firefox
    fi

    cp /tmp/$name-$i.log  /home/vagrant/sigl_logs/
  done
  source ~/SIGgenerator/spade-query-script.sh $itr $name $exec_path

}

#main_function
parse_commands $@
