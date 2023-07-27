# SIGL
This repository contains code for the reimplementation of a variation of the [SIGL paper](https://arxiv.org/abs/2008.11533)

## Execution

To detect a graph for anomalies, locate the desired graph within the "testingGraphs" folder and proceed by executing the following command.

```bash
python exec.py graphName
```


## Training and Validation

The embedding models and the autoencoder model have already been trained.

If the training data is modified, you will need to retrain the model using the following:

```bash
python training.py
```

The threshold used to determine anomalous processes is computed in validation phase. In order to adjust the threshold modify `validation.py`. If the model is retrained or the threshold is adjusted, you will need to recompute it using the following:

```bash
python validation.py
```

## Data

SIGL takes in input SIGs in the form of SPADE JSON files

In order to generate your own SIG, read the instructions in the SIGgenerator directory
