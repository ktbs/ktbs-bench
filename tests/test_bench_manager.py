from ktbs_bench.bench_manager import BenchManager
import pytest


class TestBenchManager(object):
    def test_init(self):
        bm = BenchManager()
        assert not bm._contexts
        assert not bm._bench_funcs
        assert not bm._results

    def test_add_bench(self):
        bm = BenchManager()
        assert not bm._bench_funcs
        # Function to bench
        @bm.bench
        def bench_func():
            pass

        # Test
        assert len(bm._bench_funcs) == 1

    def test_rtype_bench(self):
        bm = BenchManager()
        # Function to bench
        @bm.bench
        def bench_func():
            return 'this is str'

        # Test
        res_bench_func = bm._bench_funcs[0]()
        assert isinstance(res_bench_func, tuple)  # should return (str call_sig, float bench_time)
        assert isinstance(res_bench_func[0], str)
        assert isinstance(res_bench_func[1], float)

    def test_add_context(self):
        bm = BenchManager()
        assert not bm._contexts
        # Function that defines a context
        @bm.context
        def context_func():
            pass

        # Test
        assert len(bm._contexts) == 1

    @pytest.fixture
    def simple_bm(self):
        # Define a basic scenario
        bm = BenchManager()

        @bm.context
        def first_context():
            print('before bench')
            try:
                yield 123
            finally:
                print('after bench')

        @bm.context
        def second_context():
            print('second context begin')
            try:
                yield 0
            finally:
                pass

        @bm.bench
        def first_bench(n):
            print('first bench %d' % n)

        @bm.bench
        def second_bench(n):
            print('second bench %d' % n)

        return bm

    def test_run_fd_output(self, simple_bm, tmpdir, capfd):
        tmp_file = '/tmp/none'  # str(tmpdir.join('res_bench_manager_run_fd_output'))
        simple_bm.run(tmp_file)

        # Test output
        out, _ = capfd.readouterr()
        expected_res = u'before bench\n'
        expected_res += u'first bench 123\n'
        expected_res += u'after bench\n'
        expected_res += u'second context begin\n'
        expected_res += u'first bench 0\n'
        expected_res += u'before bench\n'
        expected_res += u'second bench 123\n'
        expected_res += u'after bench\n'
        expected_res += u'second context begin\n'
        expected_res += u'second bench 0\n'

        assert out == expected_res

    def test_run_file_output(self, simple_bm, tmpdir):
        tmp_file = str(tmpdir.join('res_bench_manager_run_file_output'))
        simple_bm.run(tmp_file)

        # Test file output
        with open(tmp_file, 'r') as csv_out:
            lines = csv_out.readlines()

        # Check header
        header = lines[0].split(',')
        assert header[0] == 'func_name'
        assert {context.strip() for context in header[1:]} == {'first_context', 'second_context'}

        # Check bench function names
        function_names = set()
        for line in lines[1:]:
            first_el = line.split(',')[0].strip()  # get the first element of each line, except header
            function_names.add(first_el)
        assert function_names == {'first_bench', 'second_bench'}

        # Check result types
        for line in lines[1:]:
            elements = [el.strip() for el in line.split(',')[1:]]
            for el in elements:
                assert TestBenchManager.isfloat(el)

    @staticmethod
    def isfloat(string):
        """Return True if string represents a float, False otherwise."""
        try:
            float(string)
            return True
        except ValueError:
            return False
