from main.service.pre_explanation.center_most_concepts import CENTER_MOST_CONCEPTS


def test_center_most_concepts_finding_works():
    # when
    center_concepts = CENTER_MOST_CONCEPTS
    for image_label, concepts in center_concepts.items():
        clean_concepts = [c["conceptName"]for c in concepts]
        print("label: {} concepts: {}".format(image_label, clean_concepts))
    # then
    assert [] == center_concepts


if __name__ == '__main__':
    test_center_most_concepts_finding_works()
