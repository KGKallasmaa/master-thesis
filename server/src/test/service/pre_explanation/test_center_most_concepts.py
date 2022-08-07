from main.service.pre_explanation.center_most_concepts import CENTER_MOST_CONCEPTS


def test_center_most_concepts_finding_works():
    # when
    label_concepts = {}
    for image_label, concepts in CENTER_MOST_CONCEPTS.items():
        clean_concepts = [c["conceptName"] for c in concepts]
        label_concepts[image_label] = clean_concepts
        print("label: {} concepts: {}".format(image_label, clean_concepts))
    # then
    assert label_concepts.get("attic") == ['floor;flooring', 'windowpane;window', 'wall', 'cabinet', 'ceiling', 'lamp']


if __name__ == '__main__':
    test_center_most_concepts_finding_works()
