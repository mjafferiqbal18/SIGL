# Generating the Dataset

In order to add more SIGs to the dataset, fulfill the following requirements:

  1) Have the SIG available in the SPADE JSON format in the "graphs" folder

  2) Have the path of the executable file of the installed software

Run the generateTraining.py file along with the json file and executablePame

```bash
python generateTraining.py "fileName.json" "executablePath" 
```

Onedrive example:

```bash
  python generateTrainingData.py onedrive.json /usr/bin/onedrive
```

