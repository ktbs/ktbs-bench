from ktbs_bench.utils.decorators import call_signature


class TestCallSignature(object):
    def test_simple_func(self):
        # Simple function for test purpose
        def my_func(my_param):
            return my_param

        # Test output
        for p in [1, 'val', True]:
            assert call_signature(my_func, p) == ('my_param=%s' % p)

    def test_multiple_args(self):
        def simple_sum(a, b):
            return a + b

        # Check a=1 and b=2 with permutation (as arguments are taken from dict keys, which are not sorted)
        assert call_signature(simple_sum, 1, 2) == 'a=1;b=2' or \
               call_signature(simple_sum, 1, 2) == 'b=2;a=1'

    def test_kw_args(self):
        def my_str(cat_name, dog_name):
            return 'cat name is: %s, dog name is: %s' % (cat_name, dog_name)

        call_sig = call_signature(my_str, cat_name='Lala', dog_name='Lili')
        assert call_sig == 'cat_name=Lala;dog_name=Lili' or \
               call_sig == 'dog_name=Lili;cat_name=Lala'

    @staticmethod
    def my_func(a, b=None):
        return a, b

    def test_all_args(self):
        call_sig = call_signature(TestCallSignature.my_func, 1, b=2)
        assert call_sig == 'a=1;b=2' or call_sig == 'b=2;a=1'

    def test_partial_args(self):
        call_sig = call_signature(TestCallSignature.my_func, 1)
        assert call_sig == 'a=1;b=None' or call_sig == 'b=None;a=1'
