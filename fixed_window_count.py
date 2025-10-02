import time

class FixedWindowCounter:
    def __init__(self, limit: int, window_size: int):
        """
        :param limit: Max requests allowed per window
        :param window_size: Duration of each window in seconds
        """
        self.limit = limit
        self.window_size = window_size
        self.window_start = int(time.time())
        self.counter = 0

    def allow_request(self) -> bool:
        now = int(time.time())

        # Determine the current window
        current_window = now // self.window_size

        # If we've moved to a new window, reset counter
        if current_window != self.window_start:
            self.window_start = current_window
            self.counter = 0

        if self.counter < self.limit:
            self.counter += 1
            return True
        else:
            return False

if __name__ == "__main__":
    limiter = FixedWindowCounter(limit=3, window_size=10)

    # First 3 requests → allowed
    print(limiter.allow_request())  # ✅ True
    print(limiter.allow_request())  # ✅ True
    print(limiter.allow_request())  # ✅ True

    # 4th request in same 10s window → blocked
    print(limiter.allow_request())  # ❌ False

    # Wait until next window
    time.sleep(10)
    print(limiter.allow_request())  # ✅ True (new window started)




