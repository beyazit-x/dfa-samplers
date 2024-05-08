from dfa_sampler import gen_mutated_sequential_reach_avoid


def test_non_empty():
    for _ in range(100):
        lang = next(gen_mutated_sequential_reach_avoid())
        assert lang.find_word() is not None
