from requests import api

from main.service.common import serve_pil_image
from main.service.data_access import get_labels, get_images
from main.service.index_segments import image_segments
from main.service.kmeans import CENTER_MOST_CONCEPTS, CONCEPT_K_REPRESENTATIVES
from main.service.lable_image import label_example_image, label_all_images
import numpy as np
from flask_cors import CORS
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

CORS(app)


@app.route("/health", methods=["GET"])
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


# TODO: this is used
@api.route("/center-most-concepts", methods=["POST"])
def label_concepts_view():
    return jsonify({"results": CENTER_MOST_CONCEPTS})


# TODO: this is used
@api.route("/concept-representatives", methods=["POST"])
def concept_representative_view():
    payload = request.get_json()
    concept_name = payload["name"]
    if concept_name is None or concept_name == "":
        return jsonify({"results": []})
    results = CONCEPT_K_REPRESENTATIVES.get(concept_name, [])
    return jsonify({"results": results})


@api.route("/image-segments", methods=["POST"])
def image_segment_view():
    payload = request.get_json()
    index = payload["index"]
    if index == -1:
        return jsonify({"results": []})
    results = image_segments(index)
    return jsonify({"results": results})


@api.route("/all-labels", methods=["POST"])
def all_labels_view():
    labels = list(set(get_labels().tolist()))
    return jsonify({"labels": labels})


@app.route("/label-image", methods=["POST"])
def label_image_view():
    payload = request.get_json()
    label = payload["label"]
    if len(label) == 0:
        return jsonify({"index": -1, "url": "", "label": label})
    index, url = label_example_image(label)
    return jsonify({"index": index, "url": url, "label": label})


@app.route("/image-segments", methods=["POST"])
def image_segment_view():
    payload = request.get_json()
    index = payload["index"]
    if index == -1:
        return jsonify({"results": []})
    results = image_segments(index)
    return jsonify({"results": results})


@app.route("/label-all-images", methods=["POST"])
def label_all_image_view():
    payload = request.get_json()
    label = payload["label"]
    results = label_all_images(label) if len(label) > 0 else []
    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
