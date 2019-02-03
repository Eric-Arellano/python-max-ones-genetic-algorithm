# Max ones genetic algorithm

Simple genetic algorithm that finds the bit string with the most 1s in it possible through emulating evolution. Uses mutation, single-point crossover, and tournament selection as main operators, along with a custom analysis module to compare runs.

## Prereqs
* Python 3.7
* Pipenv

## To install
`pipenv install`

## To run
`pipenv run python app.py`

### Change config
Open up `resources/config.ini` and modify the values as desired.

## What I learned
* How to implement a genetic algorithm. I had learned the principles in ASU's CSE 598 Bio-Inspired Computing; this project made me learn how to actually code the algorithm.
* Matplotlib
* ConfigParser
