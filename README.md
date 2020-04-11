# nasa-volcanic-explosions
The idea of this project was to practice the complete process of a data pipeline.

We started with a dataset, clean it, and then enrich it with data from an external source.
The program generated could be run from bash command line, and generate brief reports about the data.

In this case, we are using a Volcanic Eruptions Dataset found on Kaggle.
The dataset was posted by [ritmandotpy](https://github.com/ritmandotpy/volcanic_eruptions) but it is normally mantained by the [Smithsonian Institution's Global Volcanism Program](https://volcano.si.edu/).

On the other hand, we are using NASA's Earth Polychromatic Imaging Camera (EPIC) satellite to look at our planet earth from a distand perspective during these eruption events.

![Deep Space Climate Observatory](INPUT/DSCOVR.jpg)

Active volcanoes go through eruptive phases that can last from a day to years. During these phases, there are moments where the volcano does not show any activity.

The DSCOVR satellite was launched on 2015 by SpaceX's Falcon 9 rocket, and it's constantly taking photos of our blue marble.

The idea of this project was to use NASA's EPIC API and volcano eruption data to find the available images from the satellite for those specific dates.

The resulting images will still be hosted at the NASA archive.

To read more about the API: 
https://epic.gsfc.nasa.gov/about/api
