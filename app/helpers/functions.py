import os
import json
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score
from sklearn.metrics import confusion_matrix as c_matrix
from app.train_predictions.hyperparameters.hyperparameters import save_hyperparameters
from configs.settings import COMMON_FEATURES


def natural_occurrences(possible_outcomes, train_frame, test_frame, target, print_output=True):
    # Combine train and test frames
    combined_frame = pd.concat([train_frame, test_frame], ignore_index=True)

    # Calculate the percentages & return occurrences
    occurrences = {}
    percentage_counts = combined_frame[target].value_counts()
    total_matches = len(combined_frame)

    for outcome in possible_outcomes:
        count = percentage_counts.get(outcome, -1)
        percentage = (count / total_matches) * 100

        # Set values close to zero to zero
        percentage = round(0 if percentage < 0.01 else percentage, 2)

        occurrences[outcome] = percentage
        if print_output:
            print(f"Natural Percentage of {outcome}: {percentage}%")

    return occurrences


def natural_occurrences_grid(possible_outcomes, train_frame, target, without_target_frame):
    # Calculate the percentages & return occurrences
    occurrences = {}

    _train_frame = train_frame

    train_frame = []
    for x in (without_target_frame):
        # for y in enumerate(_train_frame):
        print(x)
        # if x['id'] == y['id']:
        #     train_frame.append(y)

    percentage_counts = train_frame[target].value_counts()
    total_matches = len(train_frame)

    for outcome in possible_outcomes:
        count = percentage_counts.get(outcome, 0)
        percentage = round((count / total_matches) * 100, 2)
        occurrences[outcome] = percentage
        print(f"Natural Percentage of {outcome}: {percentage}%")

    return occurrences


def save_model(model, train_frame, test_frame, FEATURES, target, compe_data):
    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']

    matches = train_frame
    model.fit(matches[FEATURES], matches[target])

    # Create the directory if it doesn't exist
    directory = os.path.abspath(
        f"trained_models/{PREDICTION_TYPE}/{COMPETITION_ID}/")
    os.makedirs(directory, exist_ok=True)

    name = target[0]+'_multiple' if type(target) == list else target
    # Save the model
    filename = os.path.abspath(f"{directory}/{name}_model.joblib")

    joblib.dump(model, filename)

    print('Model saved.')


def get_model(target, compe_data):
    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']
    # Save the model
    filename = os.path.abspath(
        f"trained_models/{PREDICTION_TYPE}/{COMPETITION_ID}/{target}_model.joblib")
    return joblib.load(filename)


def preds_score(user_token, target, test_frame, preds, compe_data):
    # Calculate accuracy and precision for the target variable
    accuracy = accuracy_score(test_frame[target], preds)
    precision = precision_score(
        test_frame[target], preds, average='weighted', zero_division=0)
    f1 = f1_score(test_frame[target], preds,
                  average='weighted', zero_division=0)
    # Calculate the percentages
    average_score = int((1/3 * accuracy + 1/3 * precision + 1/3 * f1) * 100)
    accuracy = int((accuracy / 1) * 100)
    precision = int((precision / 1) * 100)
    f1 = int((f1 / 1) * 100)

    print(f"Accuracy: {accuracy}%")
    print(f"Precision: {precision}%")
    print(f"F1 score: {f1}%")
    print(f"AVG score: {average_score}%")
    print(f"")

    scores = accuracy, precision, f1, average_score

    if compe_data and 'is_training' in compe_data and compe_data['is_training']:
        compe_data['scores'] = scores
        save_hyperparameters(compe_data, target, user_token)


def confusion_matrix(test_frame, target, preds):
    # Calculate the confusion matrix
    confusion = c_matrix(test_frame[target], preds)
    # Print the confusion matrix
    print("Confusion Matrix:")
    print(confusion)
    print("\n")


def feature_importance(model, compe_data, target, FEATURES, show=True, threshold=0.005):
    feature_importance = model.feature_importances_

    if show:
        print(feature_importance)

    best_features = []
    for i, val in enumerate(feature_importance):
        if val > threshold:
            best_features.append(FEATURES[i])
    if show:
        print(len(FEATURES), len(best_features), best_features)

    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']

    # Create the directory if it doesn't exist
    directory = os.path.abspath(
        f"configs/important_features/{PREDICTION_TYPE}/{COMPETITION_ID}/")
    os.makedirs(directory, exist_ok=True)

    # Save the features
    filename = os.path.abspath(f"{directory}/{target}_features.json")
    # Save the sorted data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(best_features, file, indent=4)

    return best_features


def get_features(compe_data, target, is_grid_search=False):
    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']

    features = COMMON_FEATURES
    has_features = False

    if not is_grid_search:
        try:
            # Load hyperparameters data
            filename = os.path.abspath(
                f"configs/important_features/{PREDICTION_TYPE}/{COMPETITION_ID}/{target}_features.json")

            try:
                with open(filename, 'r') as file:
                    features_data = parse_json(json.load(file))
            except:
                FileNotFoundError

            # Get the hyperparameters for compe id
            if len(features_data) > 0:
                features = features_data
                has_features = True

        except:
            KeyError

    return features, has_features


def parse_json(json_data):
    if isinstance(json_data, dict):
        parsed_data = {}
        for key, value in json_data.items():
            parsed_key = int(key) if key.isdigit() else key
            parsed_value = parse_json(value)
            parsed_data[parsed_key] = parsed_value
        return parsed_data
    elif isinstance(json_data, list):
        return [parse_json(item) for item in json_data]
    else:
        return json_data


def store_score_weights(compe_data, target, score_weights):
    print(f'Best Score Weights:{score_weights}\n')

    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']

    # Create the directory if it doesn't exist
    directory = os.path.abspath(
        f"app/train_predictions/tuning/score_weights/{PREDICTION_TYPE}/")
    os.makedirs(directory, exist_ok=True)

    filename = f'{directory}/{target}_scores_weights.json'
    file_path = os.path.join(directory, filename)

    # Read existing data from the JSON file
    weights_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            weights_dict = parse_json(json.load(json_file))

    # Update or add the score weights for the target
    weights_dict[COMPETITION_ID] = score_weights

    # Sort the dictionary by keys
    weights_dict = dict(
        sorted(weights_dict.items(), key=lambda x: int(x[0])))

    # Write to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(weights_dict, json_file, indent=2)


def get_score_weights(compe_data, target):
    COMPETITION_ID = compe_data['id']
    PREDICTION_TYPE = compe_data['prediction_type']

    # Construct the file path
    directory = os.path.abspath(
        f"app/train_predictions/tuning/score_weights/{PREDICTION_TYPE}/")
    filename = f'{directory}/{target}_scores_weights.json'
    file_path = os.path.join(directory, filename)

    # Read existing data from the JSON file
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            weights_dict = json.load(json_file)

            # Retrieve score weights for the given competition ID
            score_weights = weights_dict.get(str(COMPETITION_ID))

            return score_weights

    return None  # Return None if no score weights are found


def combined_score(y_true, y_pred, score_weights, natural_score):
    natural_score = 0.25 * natural_score

    weighted_accuracy = 0
    if score_weights['accuracy'] > 0:
        weighted_accuracy = score_weights['accuracy'] * \
            (0.75 * accuracy_score(y_true, y_pred) + natural_score)

    weighted_precision = 0
    if score_weights['precision'] > 0:
        weighted_precision = score_weights['precision'] * (0.75 * precision_score(
            y_true, y_pred, average='weighted', zero_division=0) + natural_score)

    weighted_f1 = 0
    if score_weights['f1'] > 0:
        weighted_f1 = score_weights['f1'] * (0.75 * f1_score(
            y_true, y_pred, average='weighted', zero_division=0) + natural_score)

    weighted_recall = 0
    if score_weights['recall'] > 0:
        weighted_recall = score_weights['recall'] * (0.75 * recall_score(
            y_true, y_pred, average='weighted', zero_division=0) + natural_score)

    # Combine scores with provided weights
    combined_score = (weighted_accuracy + weighted_precision +
                      weighted_f1 + weighted_recall) / sum(score_weights.values())

    return combined_score
