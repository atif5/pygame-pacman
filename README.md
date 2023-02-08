# pygame-pacman
 A pacman clone made with pygame! (incomplete)
  
### How to install and play  
 This project is still being developed, but you are free to play it at your own risk :)
 
 I have provided a batch script for windows users to install and play the game for windows. It assumes that you have git installed.
 Only thing you need to is the run the batch file by double clicking on it, complete setting up python3 and then running `play.bat` after it's generated.
 
 If the batch script somehow fails or you are not a windows user, here is the manual installation process.
 
### Installation
You need a python 3 interpreter to play this pacman clone.

To install a python 3 interpreter follow these guidelines for: [Windows](https://docs.python-guide.org/starting/install3/win), [Linux](https://docs.python-guide.org/starting/install3/linux), [MacOs](https://docs.python-guide.org/starting/install3/osx)

  
This project uses two external libraries, [pygame](https://www.pygame.org) and [numpy](https://numpy.org/).

After installing python, you should install these libraries via [pip](https://pypi.org/project/pip/):

For windows:

```$ py -m pip install pygame numpy```

For linux or MacOs:

```$ python3 -m pip install pygame numpy```

After those libraries are installed:

```$ cd pacman```

And then;

For windows:

```$ py -m pacman```

For linux or MacOs:

```$ python3 -m pacman```

Enjoy!

## Notes

- There are numerous resources that I used (and using) to understand the game logic like: ["The Pac-Man Dossier"](https://pacman.holenet.info/) 
- I tried to stay loyal to the original version, the ghost behaviour is almost the same, the sprites are from the original arcade.
- The project is under development and you may experience bugs while playing, and there are some functionalities I haven't implemented yet like: post, pre-turning.

 

 
  
