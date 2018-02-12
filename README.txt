Hi!

This is my own "Quickbot" mobile robot used for simulation assignments in the awesome online course "Control of Mobile Robots (Georgia University)" available on Coursera.org.

The robot is built entirely on Python3. The packages you need are: numpy.

The GUI is very basic as of now, just a simple window displaying the obstacles, the robot car and the goal.


TO RUN THE PROJECT:
Just run "main.py" like a regular program file in your idle.


Project Structure:

The main.py contains the main rendering loop, which fetches object data from the files in 'World' and sends it to the 'Screen'.

The 'World' folder has all of the files you will most want to edit - they contain all the robot states, sensors, behaviors codes, as well as the obstacle, collision detection etc.

If you want to improve the GUI, please feel free to edit the file found in the Screen folder.

Unfortunately I haven't added any graphs showing relevant data, but will do it soon using matplotlib (so you may install that package as well, if you haven't already).



This is my first upload to GitHub, and will hopefully improve on this a little more, including this README.txt.
