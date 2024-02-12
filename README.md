# Killer Sudoku Solver

Killer sudoku is a variant of the sudoku game. In addition to the traditional rules of sudoku, killer sudoku imposes an additional restraint that each region, denoted by dotted lines, has to sum up to a particular value. 

This repository then contains the code needed to (partially) automatically solve the game. The goal of this program would be to extract visual data from the killer sudoku board, process it, and automatically input the solution into the game. The version of the game used for testing can be found [here](https://sudoku.com/killer). 

<p align='center'><img src=https://github.com/lohzhishen/killer-sudoku/assets/82319546/20fcad8b-3fb7-41a6-8e77-bcf2c1a76eae)></p>

<p align='center'>An example of the killer sudoku game</p>

## How it works

The problem can be broken down into 3 stages: 
1. Processing the visual image of the game
2. Finding a solution
3. Inputting the solution into the game

### Processing the visual image of the game 

The program will first prompt the user to select the region of the game board (This refers to the 9x9 box only) using their mouse. The program will then take a screenshot of the region and apply classical computer vision techniques, such as thresholding and masking, to process the image. It is assumed that the boxes are equally spaced so images of individual boxes are cropped from the screenshot with that in mind (try to keep the excess to a minimum). Contour detection is used to find regions that are likely numbers for further processing by deep learning models. A high-accuracy model was obtained by utilizing transfer learning from the MNIST dataset with fine-tuning using a manually labelled dataset of images from killer sudoku boards. Another model is used to detect the presence of dotted lines around the borders. This model was trained completely on images obtained by the preprocessing pipeline. 

The result of the computer vision pipeline is shown to the user using a pygame interface. The interface enables the user to manually verify and correct the mistakes made by the model. 

<p align='center'><img src=https://github.com/lohzhishen/killer-sudoku/assets/82319546/832ba13a-1b90-47c9-a92c-3a6f1eb18027></p>
<p align='center'>Editor interface</p>

### Finding a solution

Similar to traditional sudoku solvers, the killer sudoku solver utilizes backtracking to find a solution. However, the input is verified by the program to ensure it is consistent with the game rules. For example, it ensures that the top row always has a border at the top. Graph traversal algorithm, specifically depth-first search, was utilized to pre-process the data into more suitable forms.

### Inputting the solution into the game

Lastly, the program takes control over the mouse to enter the solution. Be sure not to move the mouse in this stage otherwise, it will disturb the program and could result in a wrong or incomplete solution. 

## Structure of the repository 

Editor directory - contains the classes used to draw the pygame interface to edit the result of the computer vision pipeline.

Models directory - contains the models and notebooks used to train and evaluate the various models

dataset_labeller.ipynb - contains a Python notebook widget to label the images for the wall recognition model

detection.py - contains the functions to pre-process the images for inference and pipeline to transform the image into arrays representing the state of the game

prediction.py - contains the functions to call the models to make inferences

editor_demo.py - the program to demonstrate the editor program

interaction.py - contains functions to interact with the killer sudoku game

main.py - the overall program to solve killer sudoku games

make_dataset.py - the program to automatically create unlabelled data from killer sudoku games

solver.py - contains functions to solve the killer sudoku game

## Libraries used

* Tensorflow and Keras - for model training and inference

* Pygame - for editor interface

* Pyautogui and pynput - for interacting with the killer sudoku game

## Areas of improvement

1. An object detection model, such as YOLOv8, would be a better solution to localize and classify digits in the image. However, due to the lack of a GPU for training and inference, small models and classical techniques were used instead.

2. The dataset for fine-tuning of the digit recognizer and training the wall recognizer is rather small. The experience of manually labelling data has made me realise why labelled data is so rare in the industry. It is often not worthwhile to have individuals label data. As such, the models do make mistakes which means there is a need for human verification.

