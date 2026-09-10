import os
import glob
import cv2
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ultralytics import YOLO

# 1. ตั้งค่า Path และ Model
IMAGE_DIR = "./frames"          # โฟลเดอร์ที่เก็บไฟล์ภาพ 1,000 เฟรม
OUTPUT_XML = "annotations.xml"  # ชื่อไฟล์ผลลัพธ์ที่จะนำเข้า CVAT
MODEL_PATH = "yolov8m-seg.pt"   # หรือ custom model ของคุณที่เทรนเลนถนนไว้

# แมป class id ของโมเดล ให้ตรงกับชื่อ Label ใน CVAT
LABEL_MAPPING = {
    0: "lane",
    1: "sideway"
}

model = YOLO(MODEL_PATH)

# ดึงรายชื่อภาพ เรียงลำดับตามชื่อไฟล์ให้ตรงกับ CVAT
image_paths = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.jpg")) + 
                     glob.glob(os.path.join(IMAGE_DIR, "*.png")))

# 2. สร้างโครงสร้าง Root XML สำหรับ CVAT for images 1.1
root = ET.Element("annotations")
version = ET.SubElement(root, "version")
version.text = "1.1"

# 3. วนลูปประมวลผลทีละภาพ
for frame_id, img_path in enumerate(image_paths):
    img_name = os.path.basename(img_path)
    img = cv2.imread(img_path)
    h, w, _ = img.shape

    # สร้างแท็ก <image> สำหรับแต่ละภาพ
    image_elem = ET.SubElement(root, "image", {
        "id": str(frame_id),
        "name": img_name,
        "width": str(w),
        "height": str(h)
    })

    # สั่ง Predict
    results = model.predict(source=img_path, conf=0.25, verbose=False)[0]

    # ตรวจสอบว่าโมเดลตรวจจับ mask ได้หรือไม่
    if results.masks is not None:
        polygons = results.masks.xy      # พิกัด pixel polygon (list ของ numpy array)
        classes = results.boxes.cls.cpu().numpy().astype(int)

        for poly, cls_id in zip(polygons, classes):
            if cls_id in LABEL_MAPPING:
                label_name = LABEL_MAPPING[cls_id]

                # กรอง polygon ที่จุดน้อยเกินไป
                if len(poly) < 3:
                    continue

                # จัดรูปแบบพิกัด: "x1,y1;x2,y2;x3,y3;..." ตามมาตรฐาน CVAT
                points_str = ";".join([f"{pt[0]:.2f},{pt[1]:.2f}" for pt in poly])

                # สร้างแท็ก <polygon> ภายใต้ <image>
                ET.SubElement(image_elem, "polygon", {
                    "label": label_name,
                    "points": points_str,
                    "occluded": "0"
                })

    print(f"Processed [{frame_id + 1}/{len(image_paths)}]: {img_name}")

# 4. บันทึกและจัดหน้า XML ให้อ่านง่าย
xml_str = minidom.parseString(ET.tostring(root, encoding="utf-8")).toprettyxml(indent="  ")
with open(OUTPUT_XML, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"\nบันทึกไฟล์สำเร็จ: {OUTPUT_XML}")