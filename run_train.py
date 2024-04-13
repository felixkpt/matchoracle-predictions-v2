from configs.logger import Logger
from app.matches.load_matches import load_for_training
from app.train_predictions.train_predictions import train_predictions
from configs.active_competitions.competitions_data import trained_competitions


def run_train(user_token, compe_data, target, be_params, ignore_saved, is_grid_search):

    per_page = 800
    print(f'Train/test max limit: {per_page}')

    is_random_search = False
    update_model = True
    train_ratio = .75

    if target is None or target == 'hda' or target == 'ft-hda':
        trgt = 'ft_hda_target'
        outcomes = [0, 1, 2]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print('No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'ht-hda':
        trgt = 'ht_hda_target'
        outcomes = [0, 1, 2]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'bts':
        trgt = 'bts_target'
        outcomes = [0, 1, 2]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'over15':
        trgt = 'over15_target'
        outcomes = [0, 1]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'over25':
        trgt = 'over25_target'
        outcomes = [0, 1]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'over35':
        trgt = 'over35_target'
        outcomes = [0, 1]
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    if target is None or target == 'cs':
        trgt = 'cs_target'
        outcomes = range(0, 121)
        train_matches, test_matches, total_matches = get_matches(
            user_token, compe_data, trgt, be_params, per_page, train_ratio, ignore_saved)
        if total_matches == 0:
            print(f'No matches to make predictions for {trgt}.\n')
        else:
            train_predictions(user_token, train_matches, test_matches, compe_data, trgt, outcomes,
                          is_grid_search, is_random_search=is_random_search, update_model=update_model)

    # Update trained competitions
    compe_data['trained_to'] = be_params['to_date'].strftime(
        '%Y-%m-%d %H:%M:%S')
    trained_competitions(user_token, compe_data, len(train_matches))


def get_matches(
        user_token, compe_data, target, be_params, per_page, train_ratio, ignore_saved):
    # Load train and test data for all targets
    train_matches, test_matches = load_for_training(
        user_token, compe_data, target, be_params, per_page, train_ratio, ignore_saved)

    total_matches = len(train_matches) + len(test_matches)

    # Calculate the percentages
    train_percentage = (
        int(round((len(train_matches) / total_matches) * 100)) if total_matches > 0 else 0)
    test_percentage = (
        int(round((len(test_matches) / total_matches) * 100)) if total_matches > 0 else 0)

    Logger.info(
        f"Number of train matches: {len(train_matches)}, ({train_percentage})%")
    Logger.info(
        f"Number of test matches: {len(test_matches)}, ({test_percentage})%")

    return train_matches, test_matches, total_matches
