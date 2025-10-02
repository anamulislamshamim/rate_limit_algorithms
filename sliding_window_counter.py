import time

class SlidingWindowCounter:
    def __init__(self, window_size: int, sub_window_size: int, limit: int):
        """
        :param window_size: Total window size in seconds (e.g., 60)
        :param sub_window_size: Sub-window size in seconds (e.g., 10)
        :param limit: Max allowed requests in the window
        """
        self.window_size = window_size
        self.sub_window_size = sub_window_size
        self.limit = limit

        # Number of sub-windows
        self.num_sub_windows = window_size // sub_window_size

        # Circular buffer for counters
        self.counters = [0] * self.num_sub_windows
        self.timestamps = [0] * self.num_sub_windows  # track sub-window start times

    def _get_index(self, current_time):
        """Get the index of the sub-window for the given time"""
        return int(current_time // self.sub_window_size) % self.num_sub_windows

    def allow_request(self):
        current_time = int(time.time())
        idx = self._get_index(current_time)

        # If this sub-window is stale (older than window_size), reset it
        if current_time - self.timestamps[idx] >= self.window_size:
            self.counters[idx] = 0
            self.timestamps[idx] = current_time

        # Calculate total requests in the last window
        total = 0
        for i in range(self.num_sub_windows):
            if current_time - self.timestamps[i] < self.window_size:
                total += self.counters[i]

        if total < self.limit:
            self.counters[idx] += 1
            return True  # request allowed
        else:
            return False  # request denied

if __name__ == "__main__":
    limiter = SlidingWindowCounter(window_size=60, sub_window_size=10, limit=10)

    for i in range(15):
        allowed = limiter.allow_request()
        print(f"Request {i+1}: {'ALLOWED' if allowed else 'BLOCKED'}")
        time.sleep(3)  # simulate requests every 3s
