# nasa-volcanic-eruptions
![Satellite image of Planet Earth](INPUT/epic_1b_20190611003634.png)

The objective of this project was to practice the complete process of a data pipeline; We started with a dataset which had to be cleaned, and then enriched with data from an external source.
The program generated should be run from bash command line by runing `python3 main.py` and by giving it at least two arguments. The program should generate a brief `stdout` report about the data requested in the bash command.

In this case, we are using a Volcanic Eruptions Dataset found on Kaggle. The dataset was posted by [ritmandotpy](https://github.com/ritmandotpy/volcanic_eruptions), and it is normally mantained by the [Smithsonian Institution's Global Volcanism Program](https://volcano.si.edu/).

On the other hand, we are using NASA's Earth Polychromatic Imaging Camera (EPIC) satellite's archive API to look at our planet earth from 1 million miles away on a specified date.


![Deep Space Climate Observatory](INPUT/DSCOVR.jpg)

When filtering dates,

Active volcanoes go through eruptive phases that can last from a day to years. During these phases, there are moments where the volcano does not show any activity.

The DSCOVR satellite was launched on 2015 by SpaceX's Falcon 9 rocket, and it's constantly taking photos of our blue marble.

The idea of this project was to use NASA's EPIC API and volcano eruption data to find the available images from the satellite for those specific dates.

The resulting images will still be hosted at the NASA archive.

##  Getting started:
∫
requires you to install python 3 or higher

0. Use the dev branch as it was most stable last I tried : `git checkout presenter-dev`
1. running `python3 main.py` or `python main.py` depending on your configuration will give you the welcome screen and instructions.
2. provide a year and a month to query (`python3 main.py YYYY MM`)
3. open the PDF report on `/OUTPUT` folder


To read more about the API: 
https://epic.gsfc.nasa.gov/about/api
