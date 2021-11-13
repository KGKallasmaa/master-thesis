from typing import List

import PIL
import numpy as np
import pickle
import pandas as pd

with open('src/data/masks.pkl', 'rb') as f:
    masks = pickle.load(f)
with open('src/data/resized_imgs.pkl', 'rb') as f:
    imgs = pickle.load(f)
with open('src/data/classes.pkl', 'rb') as f:
    labels = np.array(pickle.load(f))


def get_masks():
    return masks

# TODO: add type pil
def get_images():
    return imgs


def get_labels() -> np.array:
    return labels


def get_segments(img, mask, threshold=0.05):
    ade_classes = pd.read_csv('src/data/objectInfo150.csv')
    segs = np.unique(mask)
    segments = []
    total = mask.shape[0] * mask.shape[1]
    segments_classes = []
    for seg in segs:
        idxs = mask == seg
        sz = np.sum(idxs)
        if sz < threshold * total:
            continue
        segment = img * idxs[..., None]
        w, h, _ = np.nonzero(segment)
        segment = segment[np.min(w):np.max(w), np.min(h):np.max(h), :]
        segments.append(segment)
        segments_classes.append(ade_classes['Name'].loc[ade_classes['Idx'] == seg].iloc[0])
    return segments, segments_classes
