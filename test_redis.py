import redis
r = redis.from_url("redis://localhost:6379", decode_responses=True)
r.set("testkey", "hello world")
print("Giá trị:", r.get("testkey"))
