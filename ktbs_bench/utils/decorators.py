from functools import wraps
from inspect import getcallargs

from timer import Timer


def bench(f):
    """Decorator to time a function.

    Parameters
    ----------
    f : function
        The function to time.

    Returns
    -------
    call_signature : str
        The signature of the function call, with parameter names and values.
    time : float
        The real time taken to execute the function, in second.

    Examples
    --------
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

    Parameters
    ----------
    f : function
        The function to get the call signature from.
    args : list
        List of arguments.
    kwargs : dict
        Dictionary of argument names and values.

    Returns
    -------
    out : str
        String representation of the function call

    Examples
    --------
    >>> def square(num):
    ...     return num*num
    >>> call_signature(square, 4)
    'num=4'
    """
    call_args = getcallargs(f, *args, **kwargs)
    return ';'.join(["%s=%s" % (k, v) for k, v in call_args.items()])
