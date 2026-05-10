from DICE_SIMULATOR.simulator import DiceSimulator
from DICE_SIMULATOR.exceptions import InvalidNumberOfThrowsError, InvalidNumberOfDiceError
from DICE_SIMULATOR import statistics as stats
from DICE_SIMULATOR import plots
from DICE_SIMULATOR import report


def ask_user_inputs():
    """Ask the user for the number of throws and dice, and return both values"""
    n_throws = int(input("How many times do you want to throw the dice? (10 - 100000): "))
    n_dice = int(input("How many dice do you want to use? (1 or 2): "))
    return n_throws, n_dice


def print_results(simulator):
    """Print all statistical results from the simulation to the console"""
    print("\n--- RESULTS ---\n")

    most, least = stats.most_and_least_frequent(simulator)
    print(f"Most frequent result: {most}")
    print(f"Least frequent result: {least}")

    values, probabilities = stats.empirical_probabilities(simulator)
    print("\nEmpirical probabilities:")
    for v, p in zip(values, probabilities):
        print(f"  Result {v}: {p * 100:.2f}%")

    avg, minimum, maximum = stats.average_min_max(simulator)
    print(f"\nAverage: {avg:.2f}")
    print(f"Min: {minimum}")
    print(f"Max: {maximum}")

    print(f"\nPercentage of pairs (even results): {stats.percentage_of_pairs(simulator):.2f}%")
    print(f"Percentage of odds: {stats.percentage_of_odds(simulator):.2f}%")

    if simulator.get_n_dice() == 2:
        print(f"Percentage of doubles: {stats.percentage_of_doubles(simulator):.2f}%")


def show_all_plots(simulator):
    """Display all four plots for the simulation results"""
    plots.plot_distribution(simulator)
    plots.plot_single_dice(simulator)
    plots.plot_pairs_vs_odds(simulator)
    plots.plot_doubles(simulator)


def main():
    """Runs the simulation, prints the results, show plots and saves a PDF report (if the user wants to)"""
    try:
        n_throws, n_dice = ask_user_inputs()
        simulator = DiceSimulator(n_throws, n_dice)
        simulator.run()
        print_results(simulator)
        show_all_plots(simulator)

        save_pdf = input("\nDo you want to save a PDF report? (y/n): ")
        if save_pdf.lower() == "y":
            pdf_path = report.generate_report(simulator, "DICE_SIMULATOR/output")
            print(f"Report saved to: {pdf_path}")
    except InvalidNumberOfThrowsError as e:
        print(f"Error: {e}")
    except InvalidNumberOfDiceError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: please enter a valid integer.")


if __name__ == "__main__":
    main()