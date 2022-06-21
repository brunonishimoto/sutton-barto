from blackjack import Blackjack
from monte_carlo import MonteCarloPrediction, MonteCarloES, MonteCarloWithoutES
from policies import PlayerPolicy1, PlayerPolicy2, PlayerPolicyWithoutES
from consts import *
from argparse import ArgumentParser

def play_monte_carlo_prediction(num_episodes, directory, experiment_name):
    game = Blackjack()
    monte_carlo = MonteCarloPrediction(PlayerPolicy1())

    for eps in range(num_episodes):
        print(eps)
        state = game.start_game()
        monte_carlo.start_episode()

        end_game = False
        action = monte_carlo.step(state, 0, end_game)

        while not end_game:
            if action is not None:
                state, reward, end_game = game.action(action)

                action = monte_carlo.step(state, reward, end_game)

        monte_carlo.update_states()


    monte_carlo.save(directory, experiment_name)

def play_monte_carlo_es(num_episodes, directory, experiment_name):
    game = Blackjack()
    monte_carlo = MonteCarloES(PlayerPolicy2())

    for eps in range(num_episodes):
        print(eps)
        state = game.start_game()
        monte_carlo.start_episode()

        end_game = False
        action = monte_carlo.step(state, 0, end_game)

        while not end_game:
            if action is not None:
                state, reward, end_game = game.action(action)

                action = monte_carlo.step(state, reward, end_game)

        # When episode ends update states and policy
        monte_carlo.update_states()

    monte_carlo.save(directory, experiment_name)

def play_monte_carlo_without_es(num_episodes, directory, experiment_name):
    game = Blackjack()
    monte_carlo = MonteCarloWithoutES(PlayerPolicyWithoutES())

    for eps in range(num_episodes):
        print(eps)
        state = game.start_game()
        monte_carlo.start_episode()

        end_game = False
        action = monte_carlo.step(state, 0, end_game)

        while not end_game:
            if action is not None:
                state, reward, end_game = game.action(action)

                action = monte_carlo.step(state, reward, end_game)

        # When episode ends update states and policy
        monte_carlo.update_states()

    monte_carlo.save(directory, experiment_name)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num_episodes", type=int, default=5e5, help="Number of episodes to run")
    parser.add_argument("--directory", type=str, default="./saves/monte_carlo_without_es", help="Directory to save the files")
    parser.add_argument("--experiment_name", type=str, default="500k_eff", help="Name of experiment")
    args = parser.parse_args()

    play_monte_carlo_without_es(int(args.num_episodes), args.directory, args.experiment_name)
    # play_monte_carlo_es(int(args.num_episodes), args.directory, args.experiment_name)
    # play_monte_carlo_prediction(int(args.num_episodes), args.directory, args.experiment_name)
