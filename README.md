# DoomPy

>:: a python gui to keep track of scores _while_ playing [**Doomlings**](https://doomlings.com/)


## Introduction

### _Doomlings_
Ever since friends backed the original version on Kickstarter and the game finally arrived, we've been more than just addicted to [**Doomlings**](https://doomlings.com/) from the very first second. Unfortunately, we don't live too close to one another, so we only see each other every few weeks/months. But WHEN we do, it's set in stone that at least (!) one [**Doomlings**](https://doomlings.com/) session has to be played!

I guess anyone who knows the game knows how much you can annoy each other by stealing or swapping yet another trait from the trait pile. And sometimes you don't even want to, especially not to jeopardise the peace that has just been restored. But if it has to be done, we thought it would only be fair if the player in the lead becomes the target. 

So we always tried to get a quick overview of the others' points. But with all the scoring rules, it's quite difficult to work out who's in the lead. Especially as we extended it to 4 catastrophes at some point.

### _+ Python_

After many years of MATLAB and several unsuccessful attempts to switch to Python, I finally started using Python at the end of 2023 and turned my back on MATLAB for good. And what's the best way to learn a programming language? Exactly: With an interesting project! 

### _= DoomPy_

So it was only natural for my first python project to be a [**Doomlings**](https://doomlings.com/) live points counter. Consequently,

"**Doom**lings" + "**Py**thon" = "**DoomPy**" 

was born. With **DoomPy** you can easily allocate the traits to the respective players trait piles, select catastrophes & MOLs, and thus see what the score looks like at any time.

## Methods

If you take a look at my code, please keep in mind that I'm new to Python and forgive the, very likely little _Pythonic_, chaos.

In the past I've been coding mostly in academia, especially with MATLAB. Therefore my coding style is very procedural. I have never coded in an object-orientated way. So I'm sure that there would be a much more efficient OOP alternative, especially in this case where players/traits/MOLs/ages are predestined to be defined as a `class`... but that might be a project for the future when I learn OOP.

### How to run it

As this is also the first time that I am sharing a Python project with the world, this also poses new challenges for me. 
I think (hope) it should be possible for anyone with the provided [requirements.txt](./requirements.txt) to set up a virtual environment in which DoomPy has to run.

#### 1. getting the reop

[Download the repository][zip] and unzip it. Or if you prefer to use the terminal, run


    wget https://github.com/azabicki/DoomPy/archive/refs/heads/main.zip  

or 

    curl -L -O https://github.com/azabicki/DoomPy/archive/refs/heads/main.zip

(see [comment](https://askubuntu.com/questions/939830/how-to-download-a-github-repo-as-zip-using-command-line/1236771#comment2125069_1236771) on curl)

#### 2. virtual environmant

Install the virtual environment with the tool of your choice. You find a `requirements.txt` in the repo base folder

#### 3. go play

Finally, run 

    `python /path/to/DoomPy/main.py`

and have fun playing Doomlings!!

### further requirements

_Display Resolution_: This is a very important aspect, since the GUI takes a lot of space. Especially if you play with 4 catastrophes and many rounds. And depending on which traits are played, it may happen that the height of the trait pile is larger than the screen, making it impossible to select MOLs. With 4 players and 4 catastrophes and on a `1800 x 1200` display, we ocasionally run into problems.

Hence, if possible:

 - use a higher **vertical** resolution as 1200 px if played with more than 3 catastrophes 
 - use a wider **horizontal** resolution as 1800 px if you play with more then 4 players. 


## Results

Depending on your OS Dark-Mode, DoomPy looks like this:

![GUI](misc/gui.jpg)

The GUI consist of mainly two parts:

- the **control** box on the left, where you
  - set some options for the next game
  - deal traits from the deck to the players trait piles
  - select catastrophes world's end events
  - turn some options for the current on and off  
- and **trait pile**s on the right, where you 
  - see the players current point
  - organize each player's trait pile (i.e. playing, attaching, swapping and discarding traits)
  - select MOL(s)

### How to

I hope that the handling is self-explanatory. Especially if you've already played a round or two of Doomlings. But just in case, you can find more detailed explanations here.

![GUI_with_Controls](misc/how_to.jpg)

- **Game options:**
  - Set the amount of players, size of gene pool, amount of catastrophes & MOLs
  - Name the players, but keep the correct order at the table, because some effects affects the players to your left or right
  - The radiobutton to the right of the names defines the _first player_ (name is green), it can be changed at any time during the game, and changes automatically after each catastrophe
  - Click on `start game` to clear the table and restart the game
- **Deck:**
  - Search for the name of a trait, as soon as there is only one possibility left, the cursor jumps automatically into the list
    - Click on `clr` to clear the search field
  - You may also just use the [down-arrow] key or the mouse to select a trait
  - Click on the name of a `player` to deal the selected trait into his/her trait pile
- **Catastrophes & World's End:**
  - Every time a catastrophe is turned, select it from the dropdown box
  - _First player_ is automatically changed
  - Since `Prepper` is able to choose the world's end effect, you may need to change it manually
  - As soon as every _trait's world's end effects_ are resolved, click on th `GO!` button to activate the actual _world's end effect_
- **Settings:**
  - As a joke, we thought it could be funny to make own sound-snippets and record all the "quotes" on top of every trait. But until now, we only added some generic mp3's. Turn it only and be surprised :)
  - You can change what icons will be shown in the trait pile:
    - ![icons_default](./doompy/images/icons_on.png | width=20) `Default`: basic infos about the trait + effects
    - `none`: only effects
    - `full`: all icons



### Scoreboard

### Trait Pile

### How to
 

### Options


### Keyboard shortcuts


## Discussion

- bugs found? 
- ideas for improvement?
  - issues are the way to go


[zip]: https://github.com/azabicki/DoomPy/archive/refs/heads/main.zip