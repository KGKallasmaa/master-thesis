from sanic import Sanic
from sanic.response import json

from service.lable_concepts import label_concepts
from service.lable_image import lable_example_image

app = Sanic("Master thesis service")


@app.route("/label-image", methods=["POST"])
async def label_image_view(request):
    label = request.json["label"]
    url = lable_example_image(label)
    return json({"url": url, "label": label})


@app.route("/label-concepts", methods=["POST"])
async def label_concepts_view(request):
    label = request.json["label"]
    results = label_concepts(label)
    return json({"results": results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
