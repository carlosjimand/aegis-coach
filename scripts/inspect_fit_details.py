from fitparse import FitFile

def inspect_messages(path):
    print("=" * 60)
    print(f"INSPECTING: {path}")
    fit = FitFile(path)
    for msg in fit.get_messages(['session', 'lap']):
        print(f"MSG {msg.name}:")
        for f in msg:
            if f.value is not None:
                print(f"   {f.name}: {f.value}")

inspect_messages('scripts/i200171689.fit')
inspect_messages('scripts/i201394798.fit')
