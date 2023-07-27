import pickle
from typing import List

import PIL
import numpy as np
import pandas as pd
from skimage.feature import hog

base_path = ""
# TODO: use this bath when testing code locally
# base_path = "/Users/karl-gustav.kallasmaa/Documents/Projects/master-thesis/server/src/"
masks_path = f"{base_path}main/data/masks.pkl"
img_path = f"{base_path}main/data/resized_imgs.pkl"
labels_path = f"{base_path}main/data/classes.pkl"
ade_path = f"{base_path}main/data/objectInfo150.csv"

with open(masks_path, 'rb') as f:
    masks = pickle.load(f)
with open(img_path, 'rb') as f:
    imgs = pickle.load(f)
with open(labels_path, 'rb') as f:
    labels = np.array(pickle.load(f))



ade_classes = pd.read_csv(ade_path)


def get_ade_classes():
    return ade_classes


def get_masks():
    return masks


# TODO: add type pil
def get_images() -> List[PIL.Image.Image]:
    return imgs


def get_labels() -> np.array:
    return labels


def get_segments(img, mask, threshold=0.05):
    segs = np.unique(mask)
    segments = []
    total = mask.shape[0] * mask.shape[1]
    segments_classes = []

    for seg in segs:
        idxs = mask == seg
        sz = np.sum(idxs)
        if sz < threshold * total:
            continue
        coords = np.argwhere(idxs)
        x_min, y_min = coords.min(axis=0)
        x_max, y_max = coords.max(axis=0)

        segment_img = img[x_min:x_max+1, y_min:y_max+1, :]

        segments.append(segment_img)
        segments_classes.append(ade_classes['Name'].loc[ade_classes['Idx'] == seg].iloc[0])

    return segments, segments_classes


def get_hog(image: np.array):
    _, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                       cells_per_block=(1, 1), visualize=True, channel_axis=-1)
    return hog_image

hogs = [get_hog(img) for img in imgs]

def get_hogs() -> np.array:
    return hogs