from functools import wraps
from inspect import getcallargs

from timer import Timer


def bench(f):
    """Decorator to time a function.

    :param function f: The function to benchmark.
    :returns: call_signature and real time taken to execute the function, in second.
    :rtype: tuple

    Examples
    >>> @bench
    ... def square_list(numbers):
    ...     for ind_num in range(len(numbers)):
    ...         numbers[ind_num] *= numbers[ind_num]
    ...     return numbers
    >>> call_sig, time = square_list(range(10))
    >>> call_sig
    'numbers=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
    >>> 0 < time < 1  # benched function is not computationally intensive so time should be less than 1 s
    True
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        """Actual benchmark takes place here."""
        call_sig = call_signature(f, *args, **kwargs)

        timer = Timer(tick_now=False)
        timer.start()
        f(*args, **kwargs)
        timer.stop()

        res = [call_sig, timer.get_times()['real']]
        return res

    return wrapped


def call_signature(f, *args, **kwargs):
    """Return a string representation of a function call.

    :param function f: The function to get the call signature from.
    :param list args: List of arguments.
    :param dict kwargs: Dictionary of argument names and values.
    :return: representation of a function call.
    :rtype: str

    Examples:
    >>> def square(num):
    ...     return num*num
    >>> call_signature(square, 4)
    'num=4'
    """
    call_args = getcallargs(f, *args, **kwargs)
    return ';'.join(["%s=%s" % (k, v) for k, v in call_args.items()])
