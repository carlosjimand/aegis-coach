import xml.etree.ElementTree as ET
import math

gpx_path = r'c:\Users\carlo\Downloads\recorrido-10-km-avila-monumental.gpx'
tree = ET.parse(gpx_path)
root = tree.getroot()

tag_prefix = root.tag.split('}')[0] + '}' if '}' in root.tag else ''

points = []
for trkpt in root.iter(f'{tag_prefix}trkpt'):
    lat = float(trkpt.get('lat'))
    lon = float(trkpt.get('lon'))
    ele_elem = trkpt.find(f'{tag_prefix}ele')
    ele = float(ele_elem.text) if ele_elem is not None else 0.0
    points.append((lat, lon, ele))

def haversine(p1, p2):
    R = 6371000
    lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
    lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Calculate distances along track
dists = [0.0]
for i in range(1, len(points)):
    d = haversine(points[i-1], points[i])
    dists.append(dists[-1] + d)

total_dist = dists[-1]

# Kilometer-by-kilometer breakdown
print(f"Total distance: {total_dist:.1f} m")
print("=" * 65)
print("KM BY KM BREAKDOWN (10K ÁVILA MONUMENTAL)")
print("=" * 65)

km_targets = list(range(1000, int(total_dist) + 1000, 1000))
prev_dist = 0.0
prev_ele = points[0][2]

for km_idx, target in enumerate(km_targets, 1):
    # Find points in this km window
    # interpolate at target
    if target > total_dist:
        target = total_dist
    
    # points between prev_dist and target
    seg_points = []
    seg_gain = 0.0
    seg_loss = 0.0
    
    # Find elevation at target
    for i in range(len(dists)-1):
        if dists[i] <= target <= dists[i+1]:
            ratio = (target - dists[i]) / (dists[i+1] - dists[i]) if dists[i+1] > dists[i] else 0
            target_ele = points[i][2] + ratio * (points[i+1][2] - points[i][2])
            break
    else:
        target_ele = points[-1][2]
        
    # calculate gain/loss inside segment
    # sample points
    last_d = prev_dist
    last_e = prev_ele
    for i in range(len(points)):
        if prev_dist < dists[i] <= target:
            de = points[i][2] - last_e
            if de > 0: seg_gain += de
            else: seg_loss += abs(de)
            last_e = points[i][2]
    # add final piece to target
    de = target_ele - last_e
    if de > 0: seg_gain += de
    else: seg_loss += abs(de)
    
    net_diff = target_ele - prev_ele
    seg_len = target - prev_dist
    slope = (net_diff / seg_len) * 100 if seg_len > 0 else 0
    
    print(f"KM {km_idx:02d} ({prev_dist/1000:.1f}k -> {target/1000:.1f}k): Start: {prev_ele:.1f}m -> End: {target_ele:.1f}m | Net: {net_diff:+5.1f}m | Gain: +{seg_gain:4.1f}m | Loss: -{seg_loss:4.1f}m | Avg Slope: {slope:+.2f}%")
    
    prev_dist = target
    prev_ele = target_ele
    if target >= total_dist:
        break
