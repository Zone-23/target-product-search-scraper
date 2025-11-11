thonimport time

class RetryLogic:
    def __init__(self, max_retries):
        self.max_retries = max_retries

    def apply(self, func, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retries += 1
                time.sleep(2 ** retries)
                if retries == self.max_retries:
                    raise e