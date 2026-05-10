import numpy as np


def get_distribution(simulator):
    """Return the unique values and their counts from the simulation results"""
    totals = simulator.get_totals()
    values, counts = np.unique(totals, return_counts=True)
    return values, counts


def most_and_least_frequent(simulator):
    """Return the most and least frequent values"""
    values, counts = get_distribution(simulator)
    most = values[counts.argmax()]
    least = values[counts.argmin()]
    return most, least


def empirical_probabilities(simulator):
    """Return each result value and its empirical probability"""
    totals = simulator.get_totals()
    n_throws = simulator.get_n_throws()
    values, counts = np.unique(totals, return_counts=True)
    probabilities = counts / n_throws
    return values, probabilities


def average_min_max(simulator):
    """Return the average, minimum and maximum of the results"""
    totals = simulator.get_totals()
    return np.mean(totals), np.amin(totals), np.amax(totals)


def single_dice_distribution(simulator):
    """Return the distribution of individual dice faces. For 1 die counting them directly and for two dice reshaping the result"""
    results = simulator.get_results()
    if simulator.get_n_dice() == 1:
        flat = results
    else:
        flat = results.reshape(-1)
    values, counts = np.unique(flat, return_counts=True)
    return values, counts


def percentage_of_doubles(simulator):
    """Return the percentage of throws where both dice show the same value. Returns None for 1 die"""
    if simulator.get_n_dice() == 1:
        return None
    results = simulator.get_results()
    n_throws = simulator.get_n_throws()
    doubles = np.where(results[:, 0] == results[:, 1])
    return len(doubles[0]) / n_throws * 100


def percentage_of_pairs(simulator):
    totals = simulator.get_totals()
    n_throws = simulator.get_n_throws()
    pairs = np.where(totals % 2 == 0)
    return len(pairs[0]) / n_throws * 100


def percentage_of_odds(simulator):
    totals = simulator.get_totals()
    n_throws = simulator.get_n_throws()
    odds = np.where(totals % 2 == 1)
    return len(odds[0]) / n_throws * 100