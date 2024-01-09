import pandas as pd
from configs.logger import Logger
from app.predictions_normalizers.over25_normalizer import normalizer
from app.helpers.functions import get_model, get_features
from app.helpers.print_results import print_preds_update_hyperparams


def over_predictions(matches, compe_data, target):
  
    Logger.info(f"Prediction Target: {target}")

    features, has_features = get_features(compe_data, target)
    FEATURES = features
    print(f"Has filtered features: {'Yes' if has_features else 'No'}")

    # Create train and test DataFrames
    predict_frame = pd.DataFrame(matches)

    # Get the model
    model = get_model(target, compe_data)

    # Make predictions on the test data
    preds = model.predict(predict_frame[FEATURES])
    predict_proba = model.predict_proba(predict_frame[FEATURES])

    predict_proba = normalizer(predict_proba)

    print_preds_update_hyperparams(None, target, compe_data, preds, predict_proba,
                                   train_frame=None, test_frame=predict_frame)

    return [preds, predict_proba]