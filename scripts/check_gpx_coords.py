import xml.etree.ElementTree as ET

gpx_path = r'c:\Users\carlo\Downloads\recorrido-10-km-avila-monumental.gpx'
tree = ET.parse(gpx_path)
root = tree.getroot()
tag_prefix = root.tag.split('}')[0] + '}' if '}' in root.tag else ''

points = []
for trkpt in root.iter(f'{tag_prefix}trkpt'):
    lat = float(trkpt.get('lat'))
    lon = float(trkpt.get('lon'))
    ele = float(trkpt.find(f'{tag_prefix}ele').text) if trkpt.find(f'{tag_prefix}ele') is not None else 0.0
    name = trkpt.find(f'{tag_prefix}name')
    name_str = name.text if name is not None else ''
    points.append((lat, lon, ele, name_str))

print("Total points:", len(points))
print("Start pt:", points[0])
print("Finish pt:", points[-1])

# Sample points every ~20 points
for idx in range(0, len(points), 20):
    print(f"Pt {idx:03d}: lat={points[idx][0]:.6f}, lon={points[idx][1]:.6f}, ele={points[idx][2]:.1f}")
