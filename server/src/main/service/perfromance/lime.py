from typing import List
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import numpy as np
from skimage.segmentation import mark_boundaries
from lime import lime_image
from main.service.pre_explanation.data_access import get_labels, get_images

labels = get_labels()
images = get_images()
image_indexes =[i for i in range(0, len(images))]

def classifier_fn(images_indexes):
    return [labels[image_index] for image_index in images_indexes ]

def average_lime_fidelity(image_indexes:List[int]):
    explainer = lime_image.LimeImageExplainer()
    # Explain the image
    explanation = explainer.explain_instance(image_indexes, classifier_fn, top_labels=5, hide_color=0, num_samples=1000)

    # Fidelity calculation
    fidelity_scores = []
    for label in explanation.top_labels:
        temp, mask = explanation.get_image_and_mask(label, positive_only=False, num_features=10, hide_rest=False)
        model_outputs = classifier_fn([mark_boundaries(temp / 255.0, mask)])
        weights = explanation.local_exp[label]
        weights = sorted(weights, key=lambda x: x[0])
        weights = np.array([w[1] for w in weights])
        regression_model = LinearRegression().fit(mask.reshape(-1, 1), model_outputs[0])
        fidelity_score = r2_score(model_outputs[0], regression_model.predict(mask.reshape(-1, 1)))
        fidelity_scores.append(fidelity_score)
    return  np.mean(fidelity_scores)


