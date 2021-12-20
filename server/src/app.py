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
from main.service.pre_explanation.image_index import find_image_index
from main.service.pre_explanation.index_segments import image_segments
from main.service.pre_explanation.kmeans import CENTER_MOST_CONCEPTS, concept_representatives
from main.service.pre_explanation.lable_image import label_example_image, label_all_images

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
    index = find_image_index(image_as_ar)
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


@api.route("/image-segments", methods=["POST"])
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
    label = get_labels()[index]
    return jsonify({"results": CENTER_MOST_CONCEPTS.get(label, [])})


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
        constraint.set_available_concepts(viable_concepts)
        db.update_explanation_requirement(constraint)

# TODO: this is used
@api.route("/explain-using-concepts", methods=["POST"])
def explain_using_concepts_view():
    payload = request.get_json()
    img_id = payload["img"]
    id = payload["id"]
    explanation = explain_using_concepts(id, img_id)
    return jsonify({"explanation": explanation})

@api.route("/all-labels", methods=["POST"])
def all_labels_view():
    labels = list(set(get_labels().tolist()))
    return jsonify({"labels": labels})


@api.route("/label-image", methods=["POST"])
def label_image_view():
    payload = request.get_json()
    label = payload["label"]
    if len(label) == 0:
        return jsonify({"index": -1, "url": "", "label": label})
    index, url = label_example_image(label)
    return jsonify({"index": index, "url": url, "label": label})


@api.route("/label-all-images", methods=["POST"])
def label_all_image_view():
    payload = request.get_json()
    label = payload["label"]
    results = label_all_images(label) if len(label) > 0 else []
    return jsonify({"results": results})


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)
