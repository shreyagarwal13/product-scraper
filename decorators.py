import time

def retry(max_attempts:int =3, wait_time:int =1):
    """
    This is a decorator to wrap any sync function and retry if N number of times with a given wait time.

    Args:
        max_attemps: the number of retries that the decorator will perform
        wait_time: the amount of time in seconds that the function will wait before retrying
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error in : {func.__name__}.\nFailed with error: {e} \nRetrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            raise Exception("Max retries reached.")
        return wrapper
    return decorator