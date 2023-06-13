# Generating the Dataset

All the SIGs for a particular type of training data is combined and compressed into the dataset.json files

For eg. apt-graphs contains many SIGs from apt software installations. All the information required from those SIGs is stored in the apt-dataset.json file

The generateTrainingData.py file is used to add to the training data

In order to add more SIGs to the dataset, fulfill the following requirements:

  1) Have the SIG available in the SPADE JSON format

  2) Have the path of the executable file of the installed software

Run the generateTraining.py file along with the json file and executable name

python generateTraining.py "fileName.json" "executableLocation" 

Onedrive example:

  python generateTrainingData.py onedrive.json /usr/bin/onedrive


