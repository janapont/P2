import numpy as np
from DICE_SIMULATOR.exceptions import InvalidNumberOfThrowsError, InvalidNumberOfDiceError


class DiceSimulator:
    """Simulates dice throws and stores the result"""
    def __init__(self, n_throws, n_dice):
        """Initialize the simulator with the number of throws and dice. Rises errors if values are invalid"""
        if n_throws < 10 or n_throws > 100000:
            raise InvalidNumberOfThrowsError("n_throws must be between 10 and 100000")
        if n_dice != 1 and n_dice != 2:
            raise InvalidNumberOfDiceError("n_dice must be 1 or 2")

        self._n_throws = n_throws
        self._n_dice = n_dice
        self._results = None

    def run(self):
        """Generate random dice results"""
        if self._n_dice == 1:
            self._results = np.random.randint(1, 7, self._n_throws)
        else:
            self._results = np.random.randint(1, 7, (self._n_throws, 2))
    
    def get_results(self):
        """Return the results"""
        return self._results

    def get_n_throws(self):
        """Return the number of throws"""
        return self._n_throws

    def get_n_dice(self):
        """Return the number of dice"""
        return self._n_dice

    def get_totals(self):
        """Returns the total number per throw. For 1 die returns the result directly, for two dice returns the sum of each row"""
        if self._n_dice == 1:
            return self._results
        else:
            return self._results.sum(axis=1)