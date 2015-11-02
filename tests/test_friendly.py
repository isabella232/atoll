import unittest
from functools import partial
from atoll import Pipeline
from atoll.friendly import get_example, _get_name

def add(x, y):
    return x + y

class Adder():
    def __call__(self, x, y):
        return add(x, y)


class FriendlyTests(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual(_get_name(add), 'add')
        self.assertEqual(_get_name(partial(add, 4)), 'add')
        self.assertEqual(_get_name(Adder), 'Adder')

        f = lambda x,y: x+y
        self.assertEqual(_get_name(f), 'f = lambda x,y: x+y')

    def test_pipeline_signature(self):
        p = Pipeline().to(add).to(Adder())
        self.assertEqual(p.sig, '1f3c5e11d0facd1e488cf225227f5d26')

    def test_pipeline_repr(self):
        p = Pipeline().to(add).to(Adder())
        self.assertEqual(str(p), 'to:add -> to:Adder')

    def test_pipeline_branching_repr(self):
        p = Pipeline().to(add).fork(add, add)
        self.assertEqual(str(p), 'to:add -> fork:add|add')

    def test_examples(self):
        input = [1,2,3,4]
        self.assertEqual(get_example(input), '[1,...]')

        input = [[1,2], [3,4]]
        self.assertEqual(get_example(input), '[[1,...],...]')

        input = 'foo'
        self.assertEqual(get_example(input), 'foo')

        input = 1
        self.assertEqual(get_example(input), '1')

        input = (1,2,3)
        self.assertEqual(get_example(input), '(1,2,3)')

        input = [(1,2,3),(4,5,6)]
        self.assertEqual(get_example(input), '[(1,2,3),...]')

        input = [([1,2,3],2,3),(4,5,6)]
        self.assertEqual(get_example(input), '[([1,...],2,3),...]')

        input = {'foo':'bar', 'hi': 1}
        self.assertTrue(get_example(input) in ['{foo:bar,hi:1}', '{hi:1,foo:bar}'])

