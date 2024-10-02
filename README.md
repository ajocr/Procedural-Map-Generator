# Procedural-Map-Generator

Demo: [youtube link](https://youtu.be/UQstCKXHM-4) (see PS at the bottom)

The map generation algorithm (written in python) begins with a blank map and is them populated
with various entities like water, trees, gold mines, and player units. The generated maps are then
evaluated based on certain criteria, and hill climbing algorithm is used to improve the quality.
The development of this algorithm involved a series of experiments. Initially, everything was
randomly generated- grass, trees and water. This caused the game to end before it started so I had
to try to create a path of grass to enable movement of the movable objects. To address this, a path
of grass was established, and the rest of the cells were filled with either a tree or water. This
worked; though over time players were stuck, townhall could not be built and the water cells were
scattered randomly across the map, leading to isolated puddles (as seen in the demo) rather than
‘lakes’. To fix that, the instances of water was reduced drastically and dealt with as clusters to look
more realistic. Moreover, surrounding areas to the goldmine are just grass enabling building and
movement.


PS demo was done before I figured out a way to make the maps better- scattered water and grass
area surrounding the mine for improved movement. To see a better representation of my new
map, you may review with the currrent map.xml in the repo. Thank you!!
