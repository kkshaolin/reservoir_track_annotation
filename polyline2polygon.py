import os
import xml.etree.ElementTree as ET
from shapely.geometry import LineString, Polygon


def parse_points(points_str):
    """แปลง string รูปแบบ 'x1,y1;x2,y2;...' เป็น list ของ (x, y)"""
    coords = []
    for pair in points_str.strip().split(";"):
        if pair:
            x, y = map(float, pair.split(","))
            coords.append((x, y))
    return coords


def polyline_to_polygon(coords, buffer_dist=5.0):
    """ขยายความหนาของเส้น Polyline ให้กลายเป็น Polygon ด้วย shapely"""
    line = LineString(coords)
    # cap_style: 'flat' (ตัดตรงหัวท้าย) หรือ 'round' (โค้งมน)
    # join_style: 'round' หรือ 'mitre'
    poly = line.buffer(distance=buffer_dist, cap_style="flat", join_style="round")

    # กรณีได้ MultiPolygon (อาจเกิดจากเส้นทับซ้อนกันซับซ้อน) ให้เลือกชิ้นที่ใหญ่ที่สุด
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda a: a.area)

    return list(poly.exterior.coords)


def convert_cvat_to_yolo_seg(
    xml_file, output_dir, class_mapping, line_thickness_px=6.0
):
    """
    - xml_file: path ของไฟล์ annotations.xml จาก CVAT
    - output_dir: โฟลเดอร์ปลายทางที่จะเก็บไฟล์ .txt ของ YOLO
    - class_mapping: dict จับคู่ชื่อ label -> class_id (เช่น {'lane': 0, 'car': 1})
    - line_thickness_px: ความหนาของเส้นรวม (พิกเซล) ที่ต้องการให้กลายเป็น polygon
    """
    os.makedirs(output_dir, exist_ok=True)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    buffer_dist = line_thickness_px / 2.0  # ขยายออกซ้าย-ขวา ข้างละครึ่ง

    for image_tag in root.findall("image"):
        img_name = image_tag.get("name")
        img_w = float(image_tag.get("width"))
        img_h = float(image_tag.get("height"))

        txt_filename = os.path.splitext(img_name)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)

        yolo_lines = []

        # 1. จัดการ Polygon ปกติที่มีอยู่แล้ว
        for poly_tag in image_tag.findall("polygon"):
            label = poly_tag.get("label")
            if label not in class_mapping:
                continue

            class_id = class_mapping[label]
            coords = parse_points(poly_tag.get("points"))

            # Normalize พิกัดให้อยู่ในสเกล 0-1
            norm_coords = []
            for x, y in coords:
                norm_x = max(0.0, min(1.0, x / img_w))
                norm_y = max(0.0, min(1.0, y / img_h))
                norm_coords.extend([f"{norm_x:.6f}", f"{norm_y:.6f}"])

            line_str = f"{class_id} " + " ".join(norm_coords)
            yolo_lines.append(line_str)

        # 2. จัดการ Polyline (แปลงเป็น Polygon แล้วบันทึก)
        for line_tag in image_tag.findall("polyline"):
            label = line_tag.get("label")
            if label not in class_mapping:
                continue

            class_id = class_mapping[label]
            coords = parse_points(line_tag.get("points"))

            if len(coords) < 2:
                continue

            # แปลงเส้นเป็น Polygon
            poly_coords = polyline_to_polygon(coords, buffer_dist=buffer_dist)

            # Normalize พิกัด
            norm_coords = []
            for x, y in poly_coords:
                norm_x = max(0.0, min(1.0, x / img_w))
                norm_y = max(0.0, min(1.0, y / img_h))
                norm_coords.extend([f"{norm_x:.6f}", f"{norm_y:.6f}"])

            line_str = f"{class_id} " + " ".join(norm_coords)
            yolo_lines.append(line_str)

        # เขียนลงไฟล์ .txt
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))

    print(f"แปลงข้อมูลเสร็จสิ้น! ไฟล์บันทึกอยู่ที่: {output_dir}")


# --- ตัวอย่างการเรียกใช้งาน ---
if __name__ == "__main__":
    # กำหนด mapping คลาสตามที่คุณตั้งชื่อไว้ใน CVAT
    CLASS_MAPPING = {
        "lane": 0,
        "track_line_l": 1,
        "track_line_c": 2,
        "track_line_r": 3,
        "sideway": 4
    }

    convert_cvat_to_yolo_seg(
        xml_file="c:\\Users\\kitti\\Desktop\\cvatforimages11\\annotations.xml",  # ใส่ path ไฟล์ XML ของคุณ
        output_dir="labels_yolo",  # โฟลเดอร์เซฟไฟล์ .txt
        class_mapping=CLASS_MAPPING,
        line_thickness_px=20.0,  # กำหนดความหนาเส้น polyline เป็น 6 พิกเซล
    )