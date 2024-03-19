from run_train import run_train
from datetime import datetime
from configs.active_competitions.competitions_data import get_competition_ids, get_trained_competitions
import argparse

# Calculate from_date and to_date
TRAIN_TO_DATE = datetime.strptime('2023-09-10', '%Y-%m-%d')


def train(user_token, target=None, prediction_type=None, hyperparameters={}):
    print("\n............... START TRAIN PREDICTIONS ..................\n")

    parser = argparse.ArgumentParser(
        description='Train predictions with different configurations.')
    parser.add_argument('--competition', type=int, help='Competition ID')
    parser.add_argument('--ignore-saved', action='store_true', help='Ignore saved data')
    parser.add_argument('--is-grid-search', action='store_true', help='Enable grid search')

    args, extra_args = parser.parse_known_args()
    ignore_saved = args.ignore_saved
    is_grid_search = args.is_grid_search

    # If competition_id is provided, use it; otherwise, fetch from the backend API
    competition_ids = [
        args.competition] if args.competition is not None else get_competition_ids(user_token)

    trained_competition_ids = get_trained_competitions()

    # Set default prediction type or use provided prediction_type
    # If prediction_type is provided, restrict history_limits to [8]
    HISTORY_LIMITS = [5, 10, 15]
    history_limits = HISTORY_LIMITS

    # Starting points for loops
    start_from = [10, 6, 6]
    end_at = [10, 6, 6]

    for history_limit_per_match in history_limits:
        # Skip if current history_limit_per_match is less than the specified starting point
        if history_limit_per_match < start_from[0] or history_limit_per_match > end_at[0]:
            continue
        else:
            for current_ground_limit_per_match in [4, 6, 8]:
                if current_ground_limit_per_match < start_from[1] or current_ground_limit_per_match > end_at[1]:
                    continue
                else:
                    for h2h_limit_per_match in [4, 6, 8]:
                        if h2h_limit_per_match < start_from[2] or h2h_limit_per_match > end_at[2]:
                            continue
                        else:
                            # Generate prediction type based on loop parameters
                            PREDICTION_TYPE = (
                                prediction_type
                                or f"regular_prediction_{history_limit_per_match}_{current_ground_limit_per_match}_{h2h_limit_per_match}"
                            )
                            # Loop over competition IDs
                            for COMPETITION_ID in competition_ids:
                                if not trained_competition_ids or COMPETITION_ID not in trained_competition_ids:
                                    compe_data = {'id': COMPETITION_ID,
                                                  'prediction_type': PREDICTION_TYPE}
                                    # Parameters for training
                                    be_params = {
                                        'history_limit_per_match': history_limit_per_match,
                                        'current_ground_limit_per_match': current_ground_limit_per_match,
                                        'h2h_limit_per_match': h2h_limit_per_match,
                                        'to_date': TRAIN_TO_DATE,
                                    }
                                    print(f'Competition: {COMPETITION_ID}')
                                    # Run training for the current configuration
                                    run_train(user_token, compe_data=compe_data, target=target, be_params=be_params,
                                              ignore_saved=ignore_saved, is_grid_search=is_grid_search)
                                    # return 0
    print(f"\n....... END TRAIN PREDICTIONS, Happy coding! ........")
