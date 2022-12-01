from unittest import mock

from main.models.closest_label import ClosestLabel
from main.models.consept_intuitevness import ConceptIntuitiveness
from main.models.constraints import Constraints
from main.models.enums import ExplanationType
from main.models.explanation_requirement import ExplanationRequirement
from main.service.suggestions.concept_suggestion_service import ConceptSuggestionService

constraint_db = mock.MagicMock()
intuitiveness_db = mock.MagicMock()
explanation_requirement_db = mock.MagicMock()
closest_label_db = mock.MagicMock()


def test_decision_tree_suggestions():
    # given
    service = ConceptSuggestionService(constraint_db=constraint_db,
                                       intuitiveness_db=intuitiveness_db,
                                       explanation_requirement_db=explanation_requirement_db,
                                       closest_labels_db=closest_label_db)
    # when
    constraint_db.get_constraint_by_explanation_requirement_id = mock.MagicMock(return_value=Constraints({
        "explanation_requirement_id": "123",
        "initially_proposed_concepts": [
            "concept1",
            "concept2",
            "concept3",
            "concept4",
            "concept5",
        ],
        "most_predictive_concepts": {
            "decision_tree": [
                "concept3",
                "concept4"
            ],
        },
        "user_selected_concepts": {
            "decision_tree": [
                "concept1",
                "concept2",
            ],
        },
    }))
    explanation_requirement_db.get_explanation_requirement = mock.MagicMock(return_value=ExplanationRequirement({
        "_id": "123",
        'original_image_id': 1,
        "original_image": "image1",
    }))

    intuitiveness_db.top_intuitive_concepts = mock.MagicMock(return_value=[
        ConceptIntuitiveness({
            '_id': 'i1',
            'label': 'street',
            'concept': 'concept5',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i2',
            'label': 'street',
            'concept': 'concept6',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i3',
            'label': 'street',
            'concept': 'concept7',
            'count': 1,
        }),
    ])

    results = service.consept_suggestions("123", ExplanationType.DECISION_TREE)
    # then
    expected_response = {
        "usedConcepts": ["concept1", "concept2"],
        "availableToBeChosenConcepts": ["concept3", "concept5", "concept4", "concept6", "concept7"],
    }
    assert results.to_db_value() == expected_response


def test_counterfactual_suggestions():
    # given
    service = ConceptSuggestionService(constraint_db=constraint_db,
                                       intuitiveness_db=intuitiveness_db,
                                       explanation_requirement_db=explanation_requirement_db,
                                       closest_labels_db=closest_label_db)
    # when
    constraint_db.get_constraint_by_explanation_requirement_id = mock.MagicMock(return_value=Constraints({
        "explanation_requirement_id": "123",
        "initially_proposed_concepts": [
            "concept1",
            "concept2",
            "concept3",
            "concept4",
            "concept5",
        ],
        "most_predictive_concepts": {
            "counterfactual": [
                "concept3",
                "concept4"
            ],
        },
        "user_selected_concepts": {
            "counterfactual": [
                "concept1",
                "concept2",
            ],
        },
    }))
    explanation_requirement_db.get_explanation_requirement = mock.MagicMock(return_value=ExplanationRequirement({
        "_id": "123",
        'original_image_id': 1,
        "original_image": "image1",
    }))

    intuitiveness_db.top_intuitive_concepts = mock.MagicMock(return_value=[
        ConceptIntuitiveness({
            '_id': 'i2',
            'label': 'street',
            'concept': 'concept10',
            'count': 2,
        }),
        ConceptIntuitiveness({
            '_id': 'i1',
            'label': 'street',
            'concept': 'concept5',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i3',
            'label': 'street',
            'concept': 'concept7',
            'count': 1,
        }),

        ConceptIntuitiveness({
            '_id': 'i4',
            'label': 'road',
            'concept': 'concept8',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i5',
            'label': 'road',
            'concept': 'concept9',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i6',
            'label': 'road',
            'concept': 'concept10',
            'count': 1,
        }),

        ConceptIntuitiveness({
            '_id': 'i7',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i8',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i9',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),

        ConceptIntuitiveness({
            '_id': 'i10',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i11',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i12',
            'label': 'ally',
            'concept': 'concept11',
            'count': 1,
        }),

        ConceptIntuitiveness({
            '_id': 'i12',
            'label': 'lane',
            'concept': 'concept11',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i13',
            'label': 'ally',
            'concept': 'concept12',
            'count': 1,
        }),
        ConceptIntuitiveness({
            '_id': 'i14',
            'label': 'ally',
            'concept': 'concept13',
            'count': 1,
        }),
    ])
    closest_label_db.get_by_image_id = mock.MagicMock(return_value=ClosestLabel({
        '_id': 'c1',
        'image_index': 1,
        'label': 'street',
        'closest': [
            "road",
            "ally",
            "lane",
        ]
    }))

    results = service.consept_suggestions("123", ExplanationType.COUNTERFACTUAL)
    # then
    expected_response = {
        "usedConcepts": ["concept1", "concept2"],
        "availableToBeChosenConcepts": [
            "concept3",
            "concept10",
            "concept4",
            "concept5",
            "concept7",
            "concept8",
            "concept9",
            "concept1",
            "concept2"
        ],
    }
    assert results.to_db_value() == expected_response
