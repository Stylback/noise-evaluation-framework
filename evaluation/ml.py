# External modules
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# --------------------

"""
This module attempts to evaluate performance of a machine learning model when making predictions using new data.

To use it, call the mlMain function with the required parameters.
"""

# --------------------

def loadModel(model_directory: str, filename: str) -> tf.keras.Model:
    """Loads a machine-learning model from a file, given the directory and filename of the model.

    Args:
        model_directory: Path to the directory holding the machine learning model, can be either absolute or relative to the project root directory.
        filename: name of the file, including file extension, containing the machine learning model.

    Returns:
        A TensorFlow model object.
    
    Examples:
        >>> from ml import *
        >>> model_dir = "./test/models/"
        >>> model_name = "CNN.hdf5"
        >>> CNN_model = loadModel(model_dir, model_name)
        CNN.hdf5 loaded.
    """

    loaded_model = tf.keras.models.load_model(model_directory + filename)
    print("\n" + filename + " loaded.\n")

    return loaded_model

# --------------------

def shapeData(data: list, length: int) -> list[list]:
    """Re-shapes data into a 3D array with shape (None, length, 1) as required by many models.
    If the data is equal or longer than "length", it is split into increments of the expected length (some elements are discarded) and the user is warned.
    If the data is shorter than "length", it is padded with numpy.pad and the user is warned.
    
    Args:
        data: 1D array to be re-shaped.
        length: Array length as required by the machine learning model.

    Examples:
        >>> length = 2500
        >>> original_shaped_data = shapeData(original_data, length)
        >>> noisy_shaped_data = shapeData(noisy_data, length)
    """

    if len(data) >= length:
        no_of_slices = int(len(data) / length)
        discard = len(data) % length
        shaped_data = []

        for i in range(no_of_slices):
            slice = data[length*i:length*(i+1)]
            shaped_slice = np.expand_dims(slice, axis=-1)
            shaped_data.append(shaped_slice)

        print("\n" + str(discard) + " elements were discarded.")
        
        return shaped_data

    else:
        difference = length - len(data)
        pad_width = (0,(difference))
        padded_data = np.pad(data, pad_width, mode="edge")
        shaped_data = np.expand_dims(padded_data, axis=-1)
        print("\nData was padded with " + str(difference) + " elements to meet required length.")
        
        return [shaped_data]

# --------------------

def predict(model: tf.keras.Model, data: list[float]) -> list[float]:
    """Feeds data into a machine learning model for prediction.

    Args:
        model: A machine learning model, TensorFlow model object.
        data: Data to use as basis for prediction. Shape must match the expected one of the model.

    Returns:
        A list of predictions, usually a single float.

    Examples:
        >>> prediction = predict(CNN_model, prediction_data_array)
        >>> print(prediction[0])
        0.443
    """

    prediction = model.predict(np.array([data]))
    
    return prediction

# --------------------

def confidencePlot(predictions_unaltered_data: list[float], predictions_noisy_data: list[float]) -> None:
    """Attempts to visualize any difference in model confidence as a result of signal alteration (added noise etc.).

    As one usually does not have access to ground truth when using new data to make predictions, one instead
    have to look at how confident the model is at classifying a sample. Assuming binary classification, 
    a model with high confidence in a sample will make a prediction close to the classification values 
    (very close to 0 or 1). On the other hand, if a model instead outputs a prediction with a value between
    the two classes (i.e. 0.5) it is an indication of low confidence.

    Args:
        predictions_unaltered_data: A list of prediction outputs, originating from unaltered/original data.
        predictions_noisy_data: A list of prediction outputs, originating from altered/manipulated data.

    Examples:
        >>> predictions_raw = []
        >>> predictions_noisy = []
        >>> 
        >>> for data_set in original_shaped_data:
        >>>     prediction = predict(loaded_model, data_set)
        >>>     predictions_raw.append(prediction[0][0])
        >>> 
        >>> for data_set in noisy_shaped_data:
        >>>     prediction = predict(loaded_model, data_set)
        >>>     predictions_noisy.append(prediction[0][0])
        >>> 
        >>> confidencePlot(predictions_raw, predictions_noisy)
    """
    
    one_class = np.full(len(predictions_unaltered_data), 1)
    low_conf = np.full(len(predictions_unaltered_data), 0.5)
    zero_class = np.full(len(predictions_unaltered_data), 0)

    figure(figsize=(12, 6), dpi=100)
    plt.plot(one_class, color="green", ls="--", label="High confidence of class 1")
    plt.plot(low_conf, color="salmon", ls="--", label="Line of low confidence")
    plt.plot(zero_class, color="green", ls="--", label="High confidence of class 0")
    plt.plot(predictions_unaltered_data, color="lightblue", label="Unaltered")
    plt.plot(predictions_noisy_data, color="orange", label="Altered")
    plt.legend()
    plt.xlabel("Sample")
    plt.ylabel("Prediction")
    plt.title("Evaluation: ML Performance")
    plt.show()
    
    return

def mlMain(model_directory: str, model_filename: str, unaltered_data: list, altered_data: list, array_length: int) -> None:
    """Calls the functions necessary to load a machine learning model, re-shape data and perform performance evaluation.
    
    """
    
    unaltered_shaped_data = shapeData(unaltered_data, array_length)
    altered_shaped_data = shapeData(altered_data, array_length)

    loaded_model = loadModel(model_directory, model_filename)

    predictions_unaltered = []
    predictions_altered = []

    for sample in unaltered_shaped_data:
        prediction = predict(loaded_model, sample)
        predictions_unaltered.append(prediction[0][0])

    for sample in altered_shaped_data:
        prediction = predict(loaded_model, sample)
        predictions_altered.append(prediction[0][0])
    
    deviation_unaltered = np.average([abs(element-0.5) for element in predictions_unaltered])
    deviation_altered = np.average([abs(element-0.5) for element in predictions_altered])

    print("The average distance from the 0.5-line was %1.2f for the unaltered signal and %1.2f for the altered signal." % (deviation_unaltered, deviation_altered))

    # confidencePlot(predictions_unaltered, predictions_altered)

    return [deviation_unaltered, deviation_altered]