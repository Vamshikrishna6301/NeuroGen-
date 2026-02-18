from intent_router import route_intent

tests = [
    "click",
    "scroll down",
    "move left",
    "move fast right",
    "hello world",
    "exit"
]

for t in tests:
    print("\nTEXT:", t)
    print("INTENT:", route_intent(t))
