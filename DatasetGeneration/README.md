#This contains all the dataset on which SIGL is trained. 
All the data is contained in dataset.json

In order to add more training graphs perform the following steps:

  1) Have the graphs available in the SPADE JSON format

  2) Know the path of the executable of the installed software

Run the generateTraining.py file along with the json file and executable name

Onedrive example:

  python generateTraining.py onedrive.json /usr/bin/python


