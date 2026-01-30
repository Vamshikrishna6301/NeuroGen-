import sounddevice as sd

print("Available audio devices:\n")
print(sd.query_devices())
