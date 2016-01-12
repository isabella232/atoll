from .common import beta_binomial_model
from ..models import Comment
from .readability import Readability


def make(data):
    """convert json (dict) data to a Comment object"""
    return Comment(**data)


def diversity_score(comment, alpha=2, beta=2):
    """
    description: Probability that a new reply would be from a new user.
    type: float
    valid:
        type: range
        min: 0
        max: 1
        min_inclusive: True
        max_inclusive: True
    """
    seen_users = set()

    unique_participants = []
    for r in comment.children:
        if r.user not in seen_users:
            unique_participants.append(1)
            seen_users.add(r.user)
        else:
            unique_participants.append(0)

    y = sum(unique_participants)
    n = len(comment.children)

    # again, to be conservative, we take the lower-bound
    # of the 90% credible interval (the 0.05 quantile)
    return beta_binomial_model(y, n, alpha, beta, 0.05)


def readability_scores(comment):
    """
    description: A variety of readability scores (limited language support).
    type: dict
    valid:
        type: range
        min: 0
        max: null
        min_inclusive: True
        max_inclusive: False
    """
    r = Readability(comment.content)
    return {
        'ari': r.ARI(),
        'flesch_reading_ease': r.FleschReadingEase(),
        'flesch_kincaid_grade_level': r.FleschKincaidGradeLevel(),
        'gunning_fog_index': r.GunningFogIndex(),
        'smog_index': r.SMOGIndex(),
        'coleman_liau_index': r.ColemanLiauIndex(),
        'lix': r.LIX(),
        'rix': r.RIX()
    }



