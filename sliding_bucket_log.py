import time
from collections import deque

class SlidingWindowLog:
    def __init__(self, limit: int, window_size: int):
        """
        :param limit: Max number of requests allowed in the time window
        :param window_size: Window size in seconds
        """
        self.limit = limit
        self.window_size = window_size
        self.requests = deque()  # store timestamps of requests

    def allow_request(self) -> bool:
        now = time.time()

        # Remove requests that are outside the current window
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()

        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        else:
            return False

if __name__ == "__main__":
    limiter = SlidingWindowLog(limit=3, window_size=10)

    # First 3 requests should pass
    print(limiter.allow_request())  # ✅ True
    print(limiter.allow_request())  # ✅ True
    print(limiter.allow_request())  # ✅ True

    # 4th request immediately -> should fail
    print(limiter.allow_request())  # ❌ False

    # Wait 11 seconds -> old requests expire
    time.sleep(11)
    print(limiter.allow_request())  # ✅ True again

