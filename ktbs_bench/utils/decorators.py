from functools import wraps
from inspect import getcallargs

from timer import Timer


def bench(f):
    """Times a function given specific arguments."""

    timer = Timer(tick_now=False)

    @wraps(f)
    def wrapped(*args, **kwargs):
        call_signature = getcallargs(f, *args, **kwargs)

        timer.start()
        f(*args, **kwargs)
        timer.stop()

        res = [';'.join(["%s=%s" % (k, v) for k, v in call_signature.items()]),
               timer.get_times()['real']]  # TODO penser a quel temps garder
        return res

    return wrapped


@bench
def lala(a, b, c="default c", d="default d"):
    print("lala est appelee")


if __name__ == '__main__':
    print(lala("cest a", "cest b", d="change d"))