from main.service.data_access import get_labels
from main.service.index_segments import image_segments
from main.service.lable_image import label_example_image, label_all_images
from flask_cors import CORS
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

CORS(app)


@app.route("/all-labels", methods=["POST"])
async def all_labels_view():
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
