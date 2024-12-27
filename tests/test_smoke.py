from dfa_samplers import gen_reach, gen_reach_avoid, gen_rad


def test_non_empty():
    for _ in range(100):
        assert next(gen_reach()).find_word() is not None
        assert next(gen_reach_avoid()).find_word() is not None
        assert next(gen_rad()).find_word() is not None
