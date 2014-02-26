from ktbs_bench.bench_manager import BenchManager

MGR = BenchManager()


@MGR.context  # TODO @MGR.context('Column name')
def test_env():
    try:
        print('begin try env')
        yield 'MY OBJ'
        print('end try env')
    finally:
        print('finally env')


@MGR.context
def new_env():
    yield 'a' * 10000


@MGR.bench
def test_func(obj):
    print('test_func obj: %s' % obj)


@MGR.bench
def new_func(obj):
    print('i am new func %s' % obj)


if __name__ == '__main__':
    MGR.run('/tmp/none')
