from dfa_sampler import gen_mutated_sequential_reach_avoid


def test_smoke():
    next(gen_mutated_sequential_reach_avoid())
