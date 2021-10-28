# FunFish

https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww


FunFish is based on Eddie Sharick work on YouTube. My intention was to learn more
about Pygame in particular. Since I knew about Chess programming, I was also curious
to see how he would proceed. After a few videos, I was lost. Drawing a board on the screen
with pieces that can be moved with a mouse is the easy part. But making a program to 
play according to the rules of Chess, is a task in itself. Without the proper knowledge,
it is very difficult. There are usually four elements in writing a Chess program:

1- board representation
2- move generator + make moves
3- position evaluation
4- search engine

When writing a GUI, only 1 and 2 are needed. Also, the speed at which the code is
executed is not important per se. I can say that Eddie did a good job with the GUI part.
At first, I liked the idea of using a row and column coordinates system for the board.
But, then, I realize that the one-dimensional array representation was easier to handle.
It is very easy to convert from index to row and column, and vise versa. Instead of
having two variables per square locations, one was enough. Anyway, I followed what Eddie
did but in a different way.

Instead of writing a Chess engine and merge it with the GUI program, I use an old version
of the program "sunfish" that I was able to import as a module. I made some modifications 
to the program to make it work as a process using a queue to communicate with the GUI.
Eddie's tutorial in that sense was very useful.


PS.:

Sunfish,
a simple open source chess engine under the GPL written by Thomas Dybdahl Ahle in Python
for didactic purposes, inspired by Harm Geert Muller's Micro-Max 

https://github.com/thomasahle/sunfish



