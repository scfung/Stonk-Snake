# Project Notes


![Thumbnail](/thumbnail.png?raw=true "Thumbnail")

## Team Members:
- Rounak Bhowmik
- Stanley Fung

## Inspiration: 

Our team wanted to attempt to do the GameDev hack that was given as one of the categories for the SBU Hackathon. 
## What it does: 
Our program is called Stock Snake and it’s a unique take on a gaming classic, Snake. The snake runs around and the objective of the snake is to obtain green apples and try to avoid the red apples, where the green apples give the snake more size, and hitting a red apple will end the snake’s life. (ends the game) The apples in our game contain the stock ticker of the companies with the top 25 net worth. In addition, the apples are green or red, depending if the market change of the stop is a positive or negative change, respectively. This market change is taken from the real-time data from Yahoo Finance. This game is played using the arrow keys or WASD keys, depending on the user's preference. 
## How we built it:
Our team used Python to create our program. We used imported Python libraries, like pygame and pricefetch, and built-in libraries system, random, and time. We created functions that would control the aspects of the actual snake and the apples that the snake would have to consume. Some examples are controlling the creation of the apples in the game, dealing with the stock companies, and the movement of the snake. We deployed our game on a local level, where it is runnable through a .exe file.
## Challenges we ran into:
Most of our team had little to no experience dealing with Python, so we had to learn about the Python libraries and certain syntax that was different from other high-level languages. We had problems with getting the market changes of the stock to update every time the game was played, where the color of the apples would stay the same, even if the stock moved towards an overall positive or negative change. We had to use Yahoo Finance’s delayed market data, as opposed to Google Finance’s real-time market data, since we could not seamlessly integrate the data properly into our program. Our team also had problems with starting the game, where it would take over 10 seconds for our game to get the market data to run. Our team could not implement our code to the web, where we had to deal with javascript to translate our code to something more user-friendly.
## Accomplishments our team is proud of:
- Our team is proud of how our game looks and how smoothly it runs, despite it being on the simpler end of projects.
- This is our team’s first hackathon and we created a complete program.

## What we learned:
- Most of our team learned or improved our Python skills, through learning about different libraries and their uses and Python's unique syntax.
- Deploying Python to the web and having a proper website is a very complicated task.

## What's next for Stonk Snake
In the future, our team can incorporate more companies into the game and implement power-ups within the game. We can also incorporate this program into a website or even a mobile application.
