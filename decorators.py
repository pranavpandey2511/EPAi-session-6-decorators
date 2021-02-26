from functools import wraps
import time
from math import trunc


def only_odd(func: callable):
    """This decorator lets the function execute only when the current time isin seconds is odd.

    Args:
        func (callable): Function that is being decorated.

    Returns:
        result: Returns the result of function with decorater functionality added.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        now = trunc(time.time())

        # Check if time in seconds is odd
        if now % 2 == 1:
            res = func(*args, **kwargs)
            return (f"Time in seconds is odd - ({now} seconds), {func.__name__}() executed successfully. \n Result = {res}")
        else:
            return (f"Time in seconds is NOT odd - ({now} seconds), {func.__name__}() NOT executed !!.")

    return wrapper

################## Part 2 #############################


def logger(func: callable):
    """This is a decorator function which adds logging capability to any function decorated with it.

    Args:
        funct (callable): Function to be decorated with logger.

    Returns:
        result: Returns a results of function with logging capability added.
    """

    from datetime import datetime, timezone

    @wraps(func)
    def wrapper(*args, **kwargs):
        run_dt = datetime.now(timezone.utc)
        result = func(*args, **kwargs)
        print('{0}: was called at time {1}'.format(fn.__name__, run_dt))
        return result

    return wrapper

###################### Part 3 ######################


def authenticatedOrNot(auth: bool):
    """Function which returns a decorator to add capibility for authentication for access to call a fucntion.

    Args:
        auth (bool): Authorized or not (True/False).

    Returns:
        callable: Returns a decorator with authentification capabilities.
    """
    def deco(func: callable):
        """Decorator which executes the passed in function and extra added functionality as well.

        Args:
            func (callable): Function which is decorated with authentication capability.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if auth:
                authenticity = "Your are AUTHENTICATED !!"
            else:
                authenticity = "You are NOT AUTHENTICATED !!"
            
            return result, authenticity

        # if (auth):
        #     print("Your are AUTHENTICATED !!")
        #     return wrapper
        # else:
        #     print("You are NOT AUTHENTICATED !!")
        #     return None

    return deco


########################## Part 4 ##############################

def timed_n(n: int):
    """This function gives back a decorator which executes the funciton 'n' times and keep track of the time taken.

    Args:
        n (int): number of times to execute the function.
    """
    def timed(func: callable) -> callable:
        """Decorator which keeps track of time of execution of function.

        Args:
            func (callable): funciton that is decorated.

        Raises:
            ValueError: Raise ValueError if n <= 1 

        Returns:
            result: Decorated function result.
        """
        from time import perf_counter

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Measure the execution time for function"

            Raises:
                ValueError: ValueError if n <= 1.

            Returns:
                str: string with time of execution results.
            """
            if n < 1:
                raise ValueError('n must be > =1')

            start = perf_counter()
            for i in range(n+1):
                func(*args, **kwargs)
            end = perf_counter()
            time_taken = end - start
            return f'{time_taken}:{func.__name__}():{n}: times ms'

        return wrapper
    return timed


################ Part 5 ###########################

def auth_factory(privelege_level: str):
    """Privelege levels maybe low/mid/high/no, based on which access is provied.

    Args:
        privelege_level (str): What privelege level does the current user have.
    """

    def singledispatch(func: callable):
        """ This si where we define what accesss does each privilige level has.

        Args:
            func (callable): function that is being decorated

        Returns:
            result: output of the decorated function.
        """
        registry = dict()
        registry['high'] = ['createfolder',
                            'createfile', 'editfile', 'readfile']
        registry['med'] = ['createfile', 'editfile', 'readfile']
        registry['low'] = ['editfile', 'readfile']
        registry['no'] = ['readfile']

        @wraps(func)
        def inner(*args, **kwargs):
            allowed_parameters = registry.get(privelege_level)
            print(
                f'parameters accessible with privilege="{privelege_level}" are {allowed_parameters}')
            if func.__name__ in allowed_parameters:
                return func(*args, **kwargs)
            else:
                return f'insuffient previlege for function {func.__name__} with privilege= {privelege_level}'

        return inner

    return singledispatch
