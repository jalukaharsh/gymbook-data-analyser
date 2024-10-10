# gymbook-data-analyser

This program generates the trend graphs for any given exercise given .csv data from the GymBook app (https://www.gymbookapp.com/). 

The app has functionality to generate these graphs, but some bug resets the graphs everytime the recorded weight is switched between kg and lbs, for a given exercise. The app also doesn't generate weight per rep graphs over time, which this program does. 

For now, all you have to do is specify the path of the .csv file in workout.py, the exercise name and type of graph you would like to generate. Generated graphs will be stored in same directory as workout.py. 

Hoping to add some functionality for time based exercises, and maybe a basic command line interface to generate the graphs. 
