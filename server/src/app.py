import base64

import numpy as np
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from main.database.constraint_db import ConstraintDb
from main.database.explanation_requirement import ExplanationRequirementDb
from main.database.performance_db import PerformanceDb
from main.models.enums import ExplanationType
from main.service.explain.blackbox import BlackBoxModelService
from main.service.explain.counterfactual_explanation import CounterFactualExplanationService
from main.service.explain.decision_tree_explanation import DecisionTreeExplanationService
from main.service.pre_explanation.closest_image import find_closest_image_index
from main.service.pre_explanation.common import serve_pil_image, base64_to_pil
from main.service.pre_explanation.data_access import get_labels, get_images
from main.service.pre_explanation.static_concepts_map import MOST_POPULAR_CONCEPTS
from main.service.suggestions.concept_handler import UserSelectedConceptsHandler
from main.service.suggestions.concept_suggestion_service import ConceptSuggestionService

api = Flask(__name__)
CORS(api)

explanation_requirement_db = ExplanationRequirementDb()
constraint_db = ConstraintDb()
performance_db = PerformanceDb()

counterfactual_explanation_service = CounterFactualExplanationService()
decision_tree_explanation_service = DecisionTreeExplanationService()
concept_suggestion_service = ConceptSuggestionService()
user_selected_concepts_handler = UserSelectedConceptsHandler()
black_box_service = BlackBoxModelService()


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
    image = explanation_requirement_db.get_explanation_requirement(explanation_id).original_image
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
    explanation_type = ExplanationType.from_str(
        payload["explanation_type"]) if constraint_type != "initially_proposed_concepts" else None

    if constraint_type is None or explanation_id is None or viable_concepts is None:
        return '', 400

    explanation_requirement = explanation_requirement_db.get_explanation_requirement(explanation_id)
    explanation_requirement.original_image_id = image_id
    explanation_requirement_db.update_explanation_requirement(explanation_requirement)

    user_selected_concepts_handler.new_constraints_selected(explanation_id, constraint_type, explanation_type,
                                                            viable_concepts)

    match constraint_type:
        case "initially_proposed_concepts":
            black_box_service.execute(explanation_id,viable_concepts)
        case _:
            user_selected_concepts_handler.consept_suggestions(explanation_id, explanation_type, viable_concepts)

    return '', 204


@api.route("/explanation-concepts", methods=["POST"])
def explanation_concepts():
    payload = request.get_json()
    explanation_id = payload["id"]
    explanation_type = ExplanationType.from_str(payload["explanation_type"])
    return concept_suggestion_service.consept_suggestions(explanation_id, explanation_type).to_db_value()


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
    explanation = decision_tree_explanation_service.explain(explanation_id=explanation_id,
                                                            to_be_explained_image_index=img_id)
    return jsonify(explanation)


# TODO: this is used
@api.route("/counter-factual-explanation", methods=["POST"])
def counterfactual_explanation_view():
    payload = request.get_json()
    explanation_id = payload["id"]
    img_id = payload["img"]
    counter_factual_class = payload["counterFactualClass"]
    counter_factual = counterfactual_explanation_service.explain(explanation_id=explanation_id,
                                                                 counter_factual_class=counter_factual_class,
                                                                 to_be_explained_image_index=img_id)
    return jsonify(counter_factual)


# TODO: this is used
@api.route("/all-labels", methods=["GET"])
def all_labels_view():
    labels = sorted(set(list(get_labels())))
    return jsonify({"labels": labels})


# TODO: this is used
@api.route("/performance-metrics/<explanation_id>", methods=["GET"])
def performance_metrics_view(explanation_id):
    performance = performance_db.get_by_explanation_requirement_id(explanation_id)
    return performance.to_db_value()


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000, debug=True)
