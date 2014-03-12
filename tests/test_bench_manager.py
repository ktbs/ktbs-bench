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
        def my_context():
            print('before bench')
            try:
                yield 123
            finally:
                print('after bench')

        @bm.bench
        def first_bench(n):
            print('first bench %d' % n)

        @bm.bench
        def second_bench(n):
            print('second bench %d' % n)

        return bm

    def test_run_fd_output(self, simple_bm, tmpdir, capfd):
        tmp_file = str(tmpdir.join('res_bench_manager_run_fd_output'))
        simple_bm.run(tmp_file)

        # Test output
        out, _ = capfd.readouterr()
        expected_res = u'before bench\n'
        expected_res += u'first bench 123\n'
        expected_res += u'after bench\n'
        expected_res += u'before bench\n'
        expected_res += u'second bench 123\n'
        expected_res += u'after bench\n'
        assert out == expected_res

    def test_run_file_output(self, simple_bm, tmpdir):
        tmp_file = str(tmpdir.join('res_bench_manager_run_file_output'))
        simple_bm.run(tmp_file)

        # Test file output
        with open(tmp_file, 'r') as csv_out:
            lines = csv_out.readlines()

        pass
