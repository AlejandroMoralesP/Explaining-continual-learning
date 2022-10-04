# Explaining-continual-learning
A master thesis on Explainable artificial intelligence (XAI) techniques to understand what Deep neural networs learn, forget and why a neural network produces a certain result when the input data consists of images. 
This work has been designed to be executed based on certain models of the repository https://github.com/GMvandeVen/brain-inspired-replay , specifically:
* Baseline. Trained and tested with the configuration ```python ./main_cl.py --replay=none --pre-convE --scenario=task --experiment=CIFAR100 ```
* BI-R. Trained and tested with the configuration ```python ./main_cl.py --replay=generative --brain-inspired --scenario=task --experiment=CIFAR100 ```
* EWC. Trained and tested with the configuration ```python ./main_cl.py --ewc --lambda=1000 --pre-convE --scenario=task --experiment=CIFAR100 ```

In this link you can download all the Cifar-100 images and models used during the work: https://zenodo.org/record/7144881#.Yzyyb3bMJPY

Alejandro Morales Pérez

Tutor: Natalia Díaz Rodríguez

## Installation & requirements
This code needs to be executed with Python 3.8+. Assuming that you already have one of the compatible Python versions and pip installed, the rest of the Python-packages to install would be found in the `requirements.txt` file, the command to install them is:
```
pip install -r requirements.txt
```

## Brief explanation and running
This code is in charge of extracting the Cifar100 classes that have a folder in `./cifar100_png/train` and once all the names of the classes have been obtained, it processes them to obtain an excel with data for each class and a heat map for each stored image in the folder. The extracted heat maps correspond to those of the sublayers of layer 3 and the sublayers of layer 5 of the aforementioned models. All this process is done by the `gradcam_extractor.py`.

The part in which the Lacunarity developed by Juneau in 2015 and exposed in the work called Quantification of Heat Map Data Displays for High-Throughput Analysis is used, from the heat maps previously extracted with `gradcam_extractor.py`, lacunarities of different sliding window sizes (2x2, 4x4 and 8x8) and the number of pixels of the different established groups (red, orange, yellow and other pixels) are calculated and collected in another generated excel. What is exposed in this paragraph is executed by `lacunarity.py`.

Although you can run only the first part of the process with: 
```python gradcam_extractor.py```

The entire process is executed with the command:
```python lacunarity.py```

## Results
All the results of the execution, both the excels and the generated heat maps, can be found in the `./results` folder.
