# MyDiploma
Graduate qualification work 2021

The objective of the work is to create a computer vision system based on the designed optoelectronic system, which can be used as a payload of a small-sized aircraft.
----
To achieve this objective, the following tasks must be accomplished:
* Capturing video stream from a camera connected to Raspberry Pi Zero W;
* Determining and displaying the coordinates of the marker pointing to the laser spot;
* Combined operation of the OES guidance actuators and computer vision system;
* Recognizing objects in the video stream.
----
All program codes were run in the integrated development environment Thonny, preinstalled in Raspbian.
----
* The folder "obj_tracking" contains the program code for the implementation of tracking in the video stream of a laser spot or other colored object, HSV-parameters of which were previously defined.
* The folder "tracking_system" contains the software implementation of the object tracking system using the drives of the horizontal and vertical guidance channels of the OES based on stepper motors. Two control options are presented: by angle and by speed. The algorithm used the usual conditions to eliminate the resulting tracking error. 
* The "shape_classification" folder contains an algorithm for classifying the simplest geometric shapes by shape and color, with the outline of these shapes highlighted (https://lesson.iarduino.ru/page/machine-vision-raspberry-2/).
* The "tracking_system" folder contains the face recognition project in the video stream of the modular camera. A database of faces to be recognized by the algorithm is created in advance. Then the machine learning of the model is performed. (https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition)
