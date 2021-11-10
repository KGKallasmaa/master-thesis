from sanic import Sanic
from sanic.response import json

from service.index_segments import image_segments
from service.lable_image import label_example_image, label_all_images

app = Sanic("Master thesis service")


@app.route("/label-image", methods=["POST"])
async def label_image_view(request):
    label = request.json["label"]
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
    results = label_all_images(label)
    return json({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
