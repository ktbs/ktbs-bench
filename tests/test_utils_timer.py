from ktbs_bench.utils.timer import Timer


class TestTimer(object):
    def test_init_no_tick(self):
        t = Timer(tick_now=False)
        assert not t.start_time
        assert not t.delta
        assert not t.stop_time

    def test_init(self):
        t = Timer()
        assert t.start_time
        assert not t.delta
        assert not t.stop_time

    def test_start(self):
        t = Timer()
        t_start = t.start_time
        t.start()
        assert t_start == t.start_time

    def test_stop(self):
        t = Timer()
        t.stop()
        assert t.stop_time

    def test_delta(self):
        t = Timer()
        assert not t.delta
        t.stop()
        for time_type in t.stop_time:
            assert t.stop_time[time_type] - t.start_time[time_type] == t.delta[time_type]

    def test_get_times(self):
        t = Timer()
        t.stop()
        times = t.get_times()
        for time_type, time_value in times.items():
            assert time_value == t.delta[time_type]

    def test_get_times_not_stop(self):
        t = Timer()
        times = t.get_times()
        assert not times
