import cv2
import os
import math

def extract_frames_for_yolo(video_path, output_dir, target_frames):
    """
    ฟังก์ชันสำหรับสุ่มภาพจากวิดีโอเพื่อทำ Dataset YOLO
    """
    # สร้างโฟลเดอร์สำหรับเซฟรูปถ้ายังไม่มี
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # เปิดไฟล์วิดีโอ
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"ไม่สามารถเปิดไฟล์ได้")
        return

    # ดึงข้อมูลพื้นฐานของวิดีโอ
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # คำนวณว่าจะต้องข้ามทีละกี่เฟรม
    step = max(1, math.floor(total_frames / target_frames))

    saved_count = 0
    current_frame = 0

    while True:
        ret, frame = cap.read()
        
        # ถ้าอ่านวิดีโอจบหรือมีภาพครบเฟรมแล้ว ให้ออกจากลูป
        if not ret or saved_count >= target_frames:
            break

        # ตรวจสอบว่าเฟรมปัจจุบันถึงรอบที่จะบันทึกหรือยัง
        if current_frame % step == 0:
            # ตั้งชื่อไฟล์เป็นตัวเลขที่เรียงกัน เช่น 0001.jpg, 0002.jpg (YOOLO ชอบตัวเลขเรียง)
            filename = f"frame_{saved_count:05d}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            # บันทึกภาพ
            cv2.imwrite(filepath, frame)
            saved_count += 1
            
            # แสดง Progress (แสดงทุกๆ 100 ภาพ)
            if saved_count % 100 == 0:
                print(f"บันทึกแล้ว {saved_count}/{target_frames} ภาพ...")

        current_frame += 1

    # ปิดไฟล์วิดีโอ
    cap.release()
    print(f"บันทึกไฟล์ไปที่ {output_dir} ทั้งหมด {saved_count} ภาพ")

if __name__ == "__main__":
    # พาธของไฟล์วิดีโอ
    VIDEO_FILE = "Videos\\psu-reservoir-2026Aug06_121427.mp4"
    
    # โฟลเดอร์ที่จะเก็บรูปภาพ
    OUTPUT_FOLDER = "SamplingDataset" 
    
    # จำนวนเฟรมที่ต้องการ
    NUM_FRAMES = 1001      

    extract_frames_for_yolo(VIDEO_FILE, OUTPUT_FOLDER, NUM_FRAMES)