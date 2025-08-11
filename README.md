## Hand controlled gravity sim

A project I've created to learn about computer vision and python. I've used real-world equations to model not only gravity, but also other things like the radius of black (here white) holes created. 

To control the simulation: 

1. open your thumb to move left, 
2. pinky finger to go right, 
3. index finger to go up, 
4. middle finger to zoom out, 
5. have an open palm to zoom in,
6. both index and middle finger to move down.

---

Areas for improvement:

1. Add Barnes-Hut algo!!!
2. Add more areas for improvemnt

---

In the simulation there is a constant dt that determines the amount of small fragments that time will be cut into. To get better (more acurate) results, you can lower the number. It, however, increases the number of calculations made by the computer, prolonging the time of completion.

For the code to work, some dependencies are necessary. To install them, run  `pip install numpy pygame opencv-python mediapipe` . After doing this and downloading the python file, you are ready to go.
