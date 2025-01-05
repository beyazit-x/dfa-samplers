from dfa_samplers import RADSampler, ReachSampler, ReachAvoidSampler

if __name__ == "__main__":
    rad_sampler = RADSampler()
    reach_sampler = ReachSampler()
    reach_avoid_sampler = ReachAvoidSampler()
    for _ in range(100):
        assert rad_sampler.sample().find_word() is not None
        assert reach_sampler.sample().find_word() is not None
        assert reach_avoid_sampler.sample().find_word() is not None
