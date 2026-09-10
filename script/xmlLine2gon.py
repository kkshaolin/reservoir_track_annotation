import os
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

def parse_points(points_str):
    coords = []
    for pair in points_str.strip().split(";"):
        if pair:
            x, y = map(float, pair.split(","))
            coords.append((x, y))
    return coords

def format_points(coords):
    return ";".join([f"{x:.2f},{y:.2f}" for x, y in coords])

def polyline_to_polygon(coords, buffer_dist=5.0, tolerance=1.5):
    line = LineString(coords)
    
    # 1. ขยายเส้นให้เป็น Polygon
    poly = line.buffer(distance=buffer_dist, cap_style="flat", join_style="round")
    
    # 2. ลดจำนวนจุด (Simplify) ตัดจุดที่ใกล้กันหรืออยู่บนเส้นตรงเดียวกันทิ้ง
    poly = poly.simplify(tolerance, preserve_topology=True)
    
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda a: a.area)
        
    return list(poly.exterior.coords)

def convert_cvat_tracks_to_polygon(xml_in, xml_out, line_thickness_px=20.0):
    tree = ET.parse(xml_in)
    root = tree.getroot()
    buffer_dist = line_thickness_px / 2.0
    modified_count = 0

    # 1. จัดการข้อมูลแบบ Shape (แยกเฟรม)
    for image_tag in root.findall("image"):
        for line_tag in image_tag.findall("polyline"):
            coords = parse_points(line_tag.get("points"))
            if len(coords) < 2: continue
            
            poly_coords = polyline_to_polygon(coords, buffer_dist)
            attribs = line_tag.attrib.copy()
            attribs["points"] = format_points(poly_coords)
            
            new_poly_tag = ET.Element("polygon", attribs)
            image_tag.remove(line_tag)
            image_tag.append(new_poly_tag)
            modified_count += 1

    # 2. จัดการข้อมูลแบบ Track (เชื่อมโยง ID ข้ามเฟรม)
    for track_tag in root.findall("track"):
        for line_tag in track_tag.findall("polyline"):
            coords = parse_points(line_tag.get("points"))
            if len(coords) < 2: continue
            
            poly_coords = polyline_to_polygon(coords, buffer_dist)
            attribs = line_tag.attrib.copy()
            attribs["points"] = format_points(poly_coords)
            
            new_poly_tag = ET.Element("polygon", attribs)
            track_tag.remove(line_tag)
            track_tag.append(new_poly_tag)
            modified_count += 1

    os.makedirs(os.path.dirname(xml_out) or ".", exist_ok=True)
    tree.write(xml_out, encoding="utf-8", xml_declaration=True)
    
    print(f"เสร็จสิ้น! แปลง Polyline เป็น Polygon ไปทั้งหมด {modified_count} เส้น/เฟรม")

if __name__ == "__main__":
    INPUT_XML = r"c:\Users\kitti\Desktop\cvatforimages11\annotations.xml"
    OUTPUT_XML = r"c:\Users\kitti\Desktop\cvatforimages11\new_track_annotations.xml"
    THICKNESS = 20.0 

    convert_cvat_tracks_to_polygon(INPUT_XML, OUTPUT_XML, THICKNESS)