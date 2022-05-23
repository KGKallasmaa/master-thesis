import numpy as np
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from main.database.client import get_client
from main.database.explanation_requirement import ExplanationRequirementDb
from main.service.explain.explain import explain_using_concepts
from main.service.pre_explanation.common import serve_pil_image
from main.service.pre_explanation.data_access import get_labels, get_images
from main.service.pre_explanation.image_index import attach_image_to_explanation, find_closest_image_index
from main.service.pre_explanation.index_segments import image_segments
from main.service.pre_explanation.kmeans import concept_representatives, CENTER_MOST_CONCEPTS

api = Flask(__name__)
CORS(api)

client = get_client()


# TODO: this is used
@api.route("/health", methods=["GET"])
def health_view():
    return jsonify({"hello": "world"})


# TODO: this is used
@api.route("/upload-image", methods=["POST"])
def upload_images_view():
    image = request.files['file'].read()
    image_as_ar = np.fromstring(image, np.uint8)
    explanation_id = request.args.get('id')
    attach_image_to_explanation(image, explanation_id)
    index = find_closest_image_index(image_as_ar)
    return jsonify({"index": index})


# TODO: this is used
@api.route("/image-by-index", methods=["POST"])
def image_by_index_view():
    payload = request.get_json()
    index = payload["index"]
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
    index = payload["index"]
    if index is None:
        return jsonify({"results": []})
    label = get_labels()[index]
    center_concepts = CENTER_MOST_CONCEPTS.get(label, [])
    return jsonify({"results": center_concepts})


# TODO: this is used
@api.route("/concept-representatives", methods=["POST"])
def concept_representative_view():
    payload = request.get_json()
    concept_name = payload["name"]
    if concept_name is None or concept_name == "":
        return jsonify({"results": []})
    results = concept_representatives(concept_name)
    return jsonify({"results": results})


# TODO: this is used
@api.route("/concept-constraint", methods=["POST"])
def edit_concept_constraint_view():
    payload = request.get_json()
    viable_concepts = payload["concepts"]
    id = payload["id"]
    if viable_concepts is not None and id is not None:
        db = ExplanationRequirementDb(client)
        constraint = db.get_explanation_requirement(id)
        constraint.available_concepts = viable_concepts
        db.update_explanation_requirement(constraint)
        return '', 204
    return '', 400


# TODO: this is used
@api.route("/explain-using-concepts", methods=["POST"])
def explain_using_concepts_view():
    payload = request.get_json()
    img_id = payload["img"]
    id = payload["id"]
    if img_id is None:
        return 'Image number is missing', 400
    if id is None:
        return 'Explanation id is missing', 400
    explanation = explain_using_concepts(id, img_id)
    return jsonify(explanation)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
