import sys
from fitparse import FitFile

def parse_fit(file_path):
    print("=" * 60)
    print(f"PARSING FIT FILE: {file_path}")
    print("=" * 60)
    fitfile = FitFile(file_path)
    
    # Check messages
    sets = []
    for record in fitfile.get_messages('set'):
        data = {}
        for field in record:
            data[field.name] = field.value
        sets.append(data)
    
    print(f"Total 'set' messages: {len(sets)}")
    for i, s in enumerate(sets):
        st = s.get('set_type')
        reps = s.get('repetitions')
        weight = s.get('weight')
        dur = s.get('duration')
        cat = s.get('category')
        name = s.get('exercise_name')
        print(f"Set {i+1:02d}: Type={st} | Reps={reps} | Weight={weight} kg | Dur={dur}s | Cat={cat} | Name={name}")

    if not sets:
        print("No 'set' messages found. Checking available message types:")
        types = set()
        for msg in fitfile.messages:
            types.add(msg.name)
        print("Message types:", sorted(list(types)))

if __name__ == '__main__':
    for path in sys.argv[1:]:
        parse_fit(path)
