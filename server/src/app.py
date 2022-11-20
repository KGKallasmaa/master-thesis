import numpy as np
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import base64

from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.counterfactual_explanation import CounterFactualExplanationService
from main.service.explain.decision_tree_explanation import explain_using_concepts
from main.service.pre_explanation.static_concepts_map import LABEL_CENTER_MOST_CONCEPT, MOST_POPULAR_CONCEPTS
from main.service.pre_explanation.common import serve_pil_image, base64_to_pil
from main.service.pre_explanation.data_access import get_labels, get_images
from main.service.pre_explanation.closest_image import find_closest_image_index
from main.service.pre_explanation.image_segments import image_segments

api = Flask(__name__)
CORS(api)

explanation_requirement_db = ExplanationRequirementDb()

counterfactual_explanation_service = CounterFactualExplanationService()


# TODO: this is used
@api.route("/upload-image", methods=["POST"])
def upload_images_view():
    image = request.files['file'].read()
    explanation_id = request.args.get('id')
    base_64_image = base64.b64encode(image).decode("utf-8")
    explanation_requirement_db.add_original_image_to_explanation(base_64_image, explanation_id)

    image_as_ar = np.array(base64_to_pil(base_64_image))
    index = find_closest_image_index(image_as_ar)

    return jsonify({"index": index})


# TODO: this is used
@api.route("/image-by-index", methods=["POST"])
def image_by_index_view():
    payload = request.get_json()
    index = payload.get("index", None)
    if index is None:
        return jsonify({"url": "", "label": ""})
    img = get_images()[index]
    label = get_labels()[index]
    return jsonify({"url": serve_pil_image(img), "label": label})


# TODO: this is used
@api.route("/original-image", methods=["POST"])
def original_image():
    payload = request.get_json()
    explanation_id = payload["id"]
    if explanation_id is None:
        return jsonify({"url": ""})
    database = ExplanationRequirementDb()
    image = database.get_explanation_requirement(explanation_id).original_image
    return jsonify({"url": image})


# TODO: this is used
@api.route("/most-popular-concepts", methods=["POST"])
def most_popular_concepts():
    payload = request.get_json()
    img = payload["img"]
    if img is None:
        return jsonify({"concepts": []})
    label = get_labels()[img]
    return jsonify({"concepts": MOST_POPULAR_CONCEPTS[label]})


# TODO: this is used



@api.route("/concept-constraint", methods=["POST"])
def edit_concept_constraint_view():
    # TODO: we should do some validation before submitting data
    payload = request.get_json()

    constraint_type = payload["constraint_type"]
    viable_concepts = payload["concepts"]
    explanation_id = payload["id"]
    image_id = payload["img"]

    if constraint_type is None or explanation_id is None or viable_concepts is None:
        return '', 400

    viable_concepts.sort()

    explanation_requirement = explanation_requirement_db.get_explanation_requirement(explanation_id)
    explanation_requirement.constraints.change_concept_constraint(constraint_type, viable_concepts)
    explanation_requirement.original_image_id = image_id
    explanation_requirement_db.update_explanation_requirement(explanation_requirement)
    return '', 204

@api.route("/explanation-concepts", methods=["POST"])
def explanation_concepts():
    payload = request.get_json()
    img = payload["img"]
    explanation_id = payload["id"]
    explanation_type = payload["explanation_type"]
    if img is None:
        return jsonify({"concepts": []})
    explanation_requirement = explanation_requirement_db.get_explanation_requirement(explanation_id)
    used_concepts_labels = explanation_requirement.constraints.currently_used_concepts[explanation_type]
    available_to_be_chosen_concepts = explanation_requirement.constraints.available_concepts(explanation_type)

    return jsonify(
        {
            "usedConcepts": used_concepts_labels,
            "availableToBeChosenConcepts": available_to_be_chosen_concepts,
        }
    )

"""




@api.route("/user_uploaded_image-segments", methods=["POST"])
def image_segment_view():
    payload = request.get_json()
    index = payload["index"]
    if index == -1:
        return jsonify({"results": []})
    results = image_segments(index)
    return jsonify({"results": results})


# TODO: this is used
@api.route("/center-most-concepts", methods=["POST"])
def label_concepts_view():
    payload = request.get_json()

    label = payload.get("label", "")
    index = payload["index"]
    if label == "":
        if index is None or index == -1:
            return jsonify({"results": []})
        label = get_labels()[index]

    center_concepts = CENTER_MOST_CONCEPTS.get(label, [])
    if len(center_concepts) == 0:
        return '', 400
    return jsonify({"results": center_concepts})


# TODO: this is used



# TODO: this is used
@api.route("/decision-tree-explanation", methods=["POST"])
def decision_tree_explanation_view():
    payload = request.get_json()
    img_id = payload["img"]
    explanation_id = payload["id"]
    if img_id is None:
        return 'Image number is missing', 400
    if explanation_id is None:
        return 'Explanation id is missing', 400
    explanation = explain_using_concepts(explanation_id, img_id)
    return jsonify(explanation)


# TODO: this is used
@api.route("/counter-factual-explanation", methods=["POST"])
def counterfactual_explanation_view():
    payload = request.get_json()
    explanation_id = payload["id"]
    img_id = payload["img"]
    counter_factual_class = payload["counterFactualClass"]
    counter_factual = counterfactual_explanation_service.counterfactual_explanation(explanation_id, img_id,
                                                                                    counter_factual_class)
    return jsonify(counter_factual)


# TODO: this is used
@api.route("/all-labels", methods=["GET"])
def all_labels_view():
    labels = list(set(list(get_labels())))
    labels.sort()
    return jsonify({"labels": labels})

"""

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
