# Tennis Age

A Python package that retrieves a player's career match data from Tennis Abstract and plots the player's age against the age difference between the player and each opponent. Wins and losses appear in different colors.

## Installation

After pushing this project to GitHub, install it with:

~~~bash
pip install git+https://github.com/USERNAME/REPOSITORY.git
~~~

Replace `USERNAME/REPOSITORY` with your GitHub username and repository name.

## Usage

~~~python
from tennisage import get_career_data, plot_career

serena = get_career_data("Serena Williams")
serena_plot = plot_career(serena)

rafael = get_career_data("Rafael Nadal")
nadal_plot = plot_career(rafael)
~~~

Names can be written with spaces (`"serena williams"`) or as one PascalCase name (`"SerenaWilliams"`). An unrecognized name raises a descriptive error.

`get_career_data()` returns a pandas DataFrame with the match date, tournament, surface, result, opponent, player age, opponent age, and age difference. The age difference is the player's age minus the opponent's age. `plot_career()` returns a Matplotlib axes object.

## Tests

The tests use local examples of the female and male JS formats. They do not contact the live website.

~~~bash
python -m unittest discover -s tests -v
~~~

## Personal Reflections

This assignment helped me understand how to organize code into a reusable Python package with clear public functions. I also learned that the source files represent opponent age differently for female and male players, so the cleaning step needs to handle both birth dates and decimal ages. Using local mock data for tests showed me how to check data processing without relying on a live website.
