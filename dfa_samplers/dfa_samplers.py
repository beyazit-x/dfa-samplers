import math
import numpy as np
from dfa import dict2dfa, DFA
from dfa_mutate import change_transition

__all__ = ["DFASampler", "ReachSampler", "ReachAvoidSampler", "RADSampler"]

class DFASampler:
    def __init__(self, n_tokens: int = 10, max_size: int = 10):
        assert n_tokens > 1 and max_size >= 2
        self.n_tokens = n_tokens
        self.max_size = max_size

    def sample(self) -> DFA:
        dfa = self._sample()
        while dfa.find_word() is None:
            dfa = self._sample()
        return dfa

    def _sample(self) -> DFA:
        raise NotImplementedError

    def get_size_bound(self) -> int:
        Q = self.max_size
        F = 1 # Assumption
        E = self.n_tokens
        m = Q * E # Assuming worst case
        if F > Q / 2: F = Q - F
        b_Q = math.ceil(math.log(Q, 2))
        b_E = math.ceil(math.log(E, 2))
        bin_size = math.ceil(3 + 2 * b_Q + 2 * b_E + (F + 1) * b_Q + m * (b_E + 2 * b_Q))
        return len(str(2**bin_size - 1))

class ReachSampler(DFASampler):
    def __init__(self, prob_stutter: float = 0.9, **kwargs):
        super().__init__(**kwargs)
        assert 0 <= prob_stutter <= 1
        self.prob_stutter = prob_stutter

    def _sample(self) -> DFA:
        tokens = list(range(self.n_tokens))
        n = np.random.randint(2, self.max_size) + 1
        success = n - 1
        transitions = {
            success: (True, {t: success for t in range(self.n_tokens)})
        }
        for state in range(n - 1):
            noop, good = set(), set()
            np.random.shuffle(tokens)
            good.add(tokens[0])
            for token in tokens[1:]:
                if np.random.random() <= self.prob_stutter:
                    noop.add(token)
                else:
                    good.add(token)
            _transitions = {token: state + 1 for token in good}
            _transitions.update({token: state for token in noop})
            transitions[state] = (False, _transitions)
        return dict2dfa(transitions, start=0).minimize()

class ReachAvoidSampler(DFASampler):
    def __init__(self, prob_stutter: float = 0.9, p: float | None = None, **kwargs):
        super().__init__(**kwargs)
        assert 0 <= prob_stutter <= 1
        self.prob_stutter = prob_stutter
        self.p = p
        self.n_values = np.array(list(range(1, self.max_size - 2 + 1)))
        if self.p is not None:
            self.n_p = np.array([(self.p)**v for v in self.n_values])
            self.n_p = self.n_p / np.sum(self.n_p)

    def _sample_n(self) -> int:
        if self.p is not None:
            return 2 + np.random.choice(self.n_values, p=self.n_p)
        return 2 + np.random.choice(self.n_values)

    def _sample(self) -> DFA:
        tokens = list(range(self.n_tokens))
        n = self._sample_n()
        success, fail = n - 2, n - 1
        transitions = {
            success: (True, {t: success for t in range(self.n_tokens)}),
            fail: (False, {t: fail for t in range(self.n_tokens)}),
        }
        for state in range(n - 2):
            noop, good, bad = set(), set(), set()
            np.random.shuffle(tokens)
            good.add(tokens[0])
            bad.add(tokens[1])
            for token in tokens[2:]:
                if np.random.random() <= self.prob_stutter:
                    noop.add(token)
                else:
                    np.random.choice([good, bad]).add(token)
            _transitions = {token: state + 1 for token in good}
            _transitions.update({token: fail for token in bad})
            _transitions.update({token: state for token in noop})
            transitions[state] = (False, _transitions)
        return dict2dfa(transitions, start=0).minimize()

class RADSampler(DFASampler):
    def __init__(self, max_mutations: int = 5, prob_stutter: float = 0.9, p: float | None = 0.5, **kwargs):
        super().__init__(**kwargs)
        assert max_mutations >= 0
        self.max_mutations = max_mutations
        self.reach_avoid_sampler = ReachAvoidSampler(prob_stutter=prob_stutter, p=p, **kwargs)

    def _accepting_is_sink(self, d: DFA) -> DFA:
        def transition(s: int, c: int) -> int:
            if d._label(s):
                return s
            return d._transition(s, c)
        return DFA(start=d.start, inputs=d.inputs, label=d._label, transition=transition)

    def _sample(self) -> DFA:
        candidate = self.reach_avoid_sampler.sample()
        for _ in range(np.random.choice(self.max_mutations + 1)):
            tmp = self._accepting_is_sink(change_transition(candidate))
            if tmp is None: continue
            tmp = tmp.minimize()
            if len(tmp.states()) == 1:
                continue
            candidate = tmp
        return candidate
