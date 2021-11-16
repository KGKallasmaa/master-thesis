from sanic import Sanic
from sanic.response import json

from main.service.data_access import get_labels
from main.service.index_segments import image_segments
from main.service.lable_image import label_example_image, label_all_images
from sanic_cors import CORS


app = Sanic("Master thesis service")
CORS(app)


@app.route("/all-labels", methods=["POST"])
async def all_labels_view(request):
    labels = list(set(get_labels().tolist()))
    return json({"labels": labels})


@app.route("/label-image", methods=["POST"])
async def label_image_view(request):
    label = request.json["label"]
    if len(label) == 0:
        return json({"index": -1, "url": "", "label": label})
    index, url = label_example_image(label)
    return json({"index": index, "url": url, "label": label})


@app.route("/image-segments", methods=["POST"])
async def image_segment_view(request):
    index = request.json["index"]
    if index == -1:
        return json({"results": []})
    results = image_segments(index)
    return json({"results": results})


@app.route("/label-all-images", methods=["POST"])
async def label_all_image_view(request):
    label = request.json["label"]
    results = label_all_images(label) if len(label) > 0 else []
    return json({"results": results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
