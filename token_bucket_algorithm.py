import time

class TokenBucket:
    def __init__(self, rate, capacity):
        """
        :param rate: tokens added per second
        :param capacity: max bucket size (burst size)
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()

    def allow_request(self):
        now = time.time()
        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.last_refill = now

        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

        if self.tokens >= 1:
            self.tokens -= 1
            return True  # request allowed
        else:
            return False  # request denied

if __name__ == "__main__":
    bucket = TokenBucket(rate=5, capacity=10)  # 5 req/sec, burst up to 10

    for i in range(20):
        allowed = bucket.allow_request()
        print(f"Request {i+1} : {'ALLOWED' if allowed else 'BLOCKED'}")
        time.sleep(0.1)  # simulate 5 requests/sec
        print(bucket.tokens)
