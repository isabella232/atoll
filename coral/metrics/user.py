import numpy as np
from .common import gamma_poission_model, beta_binomial_model
from ..models import User


def make(data):
    """convert json (dict) data to a user object"""
    return User(**data)


def community_score(user, k=1, theta=2):
    """estimated number of likes a comment by this user will get"""
    X = np.array([c.likes for c in user.comments])
    n = len(X)

    # we want to be conservative in our estimate of the poisson's lambda parameter
    # so we take the lower-bound of the 90% confidence interval (i.e. the 0.05 quantile)
    # rather than the expected value
    return gamma_poission_model(X, n, k, theta, 0.05)


def organization_score(user, alpha=2, beta=2):
    """probability that a comment by this user will be an editor's pick"""
    # assume whether or not a comment is starred
    # is drawn from a binomial distribution parameterized by n, p
    # n is known, we want to estimate p
    y = sum(1 for c in user.comments if c.starred)
    n = len(user.comments)

    # again, to be conservative, we take the lower-bound
    # of the 90% credible interval (the 0.05 quantile)
    return beta_binomial_model(y, n, alpha, beta, 0.05)


def moderation_prob(user, alpha=2, beta=2):
    """probability that a user's comment will be moderated"""
    y = sum(1 for c in user.comments if c.moderated)
    n = len(user.comments)
    return beta_binomial_model(y, n, alpha, beta, 0.05)


def discussion_score(user, k=1, theta=2):
    """estimated number of replies a comment by this user will get"""
    X = np.array([len(c.children) for c in user.comments])
    n = len(X)
    return gamma_poission_model(X, n, k, theta, 0.05)
