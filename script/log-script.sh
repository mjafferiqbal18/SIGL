#!/bin/bash

install_skype() {
  # Download and install Skype for Linux
  echo "Installing teamviewer for Linux..."
  #wget https://go.skype.com/skypeforlinux-64.deb
  #sudo apt install ./skypeforlinux-64.deb -y
  #sudo add-apt-repository ppa:yann1ck/onedrive
  #sudo apt install onedrive -y
  #sudo apt-get install filezilla -y

  #wget https://downloads.slack-edge.com/linux_releases/slack-desktop-4.0.2-amd64.deb
  #sudo apt install ./slack-desktop-4.0.2-amd64.deb -y

  wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb
  sudo apt install ./teamviewer_amd64.deb -y


  # Check if the installation was successful
  if [ $? -eq 0 ]; then
    echo "Installation of teamviewer for Linux was successful."
  else
    echo "Installation of teamviewer for Linux failed."
    exit 1
  fi

  # Remove the installation package
  #echo "Removing teamviewer for Linux installation package..."
  sudo rm teamviewer_amd64.deb
}


remove_skype() {
  # Remove Skype for Linux
  echo "Removing dropbox for Linux..."
  #sudo apt-get remove skypeforlinux -y
  #sudo apt remove onedrive -y
  #sudo add-apt-repository –remove ppa:yann1ck/onedrive
  #sudo apt remove filezilla -y
  sudo apt-get remove teamviewer -y
  sudo apt-get autoremove teamviewer -y
  echo "dropbox for Linux has been removed."
}

# Call the install function
#install_skype

# Call the remove function
#remove_skype

# Define the number of times to run the loop
num_loops=3

# Loop the specified number of times
for ((i=1; i<=$num_loops; i++))
do
    echo "Loop iteration $i"
    # Add your loop code here
done

exit 0
