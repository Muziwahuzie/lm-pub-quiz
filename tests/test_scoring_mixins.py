import pytest

from lm_pub_quiz.evaluators.scoring_mixins import MaskedLMScoringMixin

def test_sentence_l2r(distilbert):
    model, tokenizer = distilbert

    scorer = MaskedLMScoringMixin.from_model("distilbert-base-cased", pll_metric="sentence_l2r")

    batch = scorer.tokenizer(
        ["The traveler lost the souvenir."],
        return_tensors="pt",
        padding=True,
        return_special_tokens_mask=True,
        return_length=True,
    )

    scores = scorer.score_statements(batch)[0]

    # TODO: add test for correct masking here
    reference_scores = [
            -7.889340400695801,
            -11.87872314453125,
            -4.540374279022217,
            -8.895203590393066,
            -3.4925360679626465,
            -7.935790538787842,
            -2.4408531188964844,
            0, #-5.364403477869928e-06
            -1.5065549612045288
    ]

    for a, b in zip(scores, reference_scores):
        assert a == pytest.approx(b, abs=1e-5)

def test_within_word_l2r(distilbert):
    model, tokenizer = distilbert

    scorer = MaskedLMScoringMixin.from_model("distilbert-base-cased")

    batch = scorer.tokenizer(
        ["The traveler lost the souvenir."],
        return_tensors="pt",
        padding=True,
        return_special_tokens_mask=True,
        return_length=True,
    )

    scores = scorer.score_statements(batch)[0]

    reference_scores = [
        -3.260617733001709,
        -8.343321800231934,
        -3.81472110748291,
        -8.155835151672363,
        -2.182821273803711,
        -8.663058280944824,
        -3.539592742919922,
        0.0,
        -1.5065603256225586,
    ]

    for a, b in zip(scores, reference_scores):
        assert a == pytest.approx(b, abs=1e-5)


def test_original(distilbert):
    model, tokenizer = distilbert

    scorer = MaskedLMScoringMixin.from_model("distilbert-base-cased", pll_metric="original")

    batch = scorer.tokenizer(
        ["The traveler lost the souvenir."],
        return_tensors="pt",
        padding=True,
        return_special_tokens_mask=True,
        return_length=True,
    )

    scores = scorer.score_statements(batch)[0]

    reference_scores = [
        -3.260617733001709,
        -3.4614992141723633,
        -3.81472110748291,
        -8.155835151672363,
        -2.182821273803711,
        -0.026716232299804688,
        -5.7220458984375e-05,
        0.0,
        -1.5065603256225586,
    ]

    for a, b in zip(scores, reference_scores):
        assert a == pytest.approx(b, abs=1e-5)
