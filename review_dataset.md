# Overview
### **Cityscapes Dataset**
เป็น dataset ขนาดใหญ่ ที่มุ่งเน้นการทำความเข้าใจฉากเมือง ในระดับ semantic segmentation
มี 5,000 ภาพที่มีคุณภาพสูง ถูกทำ Annotation อย่าง แม่นยำระดับพิกเซล และ 20,000 ภาพแบบ coarse
จากวิดีโอ stereo จาก 50 เมืองที่ต่างกัน มีทั้งหมด 30 คลาส

```text
    Cityscapes/
    ├── gtFine/                     # โฟลเดอร์เก็บ Ground Truth (Label คุณภาพสูง)
    │   ├── train/
    │   │   ├── aachen/             # โฟลเดอร์ย่อยแบ่งตามชื่อเมือง
    │   │   ├── bochum/
    │   │   └── ...
    │   ├── val/
    │   │   ├── frankfurt/
    │   │   └── ...
    │   └── test/
    │       ├── berlin/
    │       └── ...
    └── leftImg8bit/                # โฟลเดอร์เก็บภาพสี RGB ต้นฉบับจากกล้องหน้ารถ
        ├── train/
        │   ├── aachen/
        │   └── ...
        ├── val/
        └── test/
```

### **CULane Dataset**
เป็น dataset ขนาดใหญ่สำหรับงาน traffic lane detection มีจำนวนภาพ: 133,235 frames แบ่งเป็น train 88,880 ภาพ , val 9,675 ภาพ และ test: 34,680 ภาพ จากวิดีโอกว่า 55 ชั่วโมง ที่มาจากกล้องบนรถ 6 คันในกรุงปักกิ่ง ประเทศจีน
ที่ lanes ถูก annotate ด้วย cubic splines ตรวจจับ lane markings 4 เส้นหลัก

```text
    CULane/
    ├── driver_23_30frame/                  # โฟลเดอร์เก็บภาพและพิกัดเลน ภายในจะมีโฟลเดอร์ย่อยแบ่งตามคลิปวิดีโอ
    ├── driver_37_30frame/          
    ├── driver_100_30frame/         
    ├── driver_161_90frame/         
    ├── driver_182_30frame/         
    ├── driver_193_90frame/         
    ├── laneseg_label_w16/                  # Segmentation masks สำหรับ Train/Val 
    ├── laneseg_label_w16_test/             # Segmentation masks สำหรับ Test
    │   ├── train.txt                       # รายชื่อไฟล์ภาพสำหรับ Train
    │   ├── train_gt.txt                    # รายชื่อไฟล์ภาพ พร้อม Path ของ Label พ่วงท้าย
    │   ├── val.txt                         # รายชื่อไฟล์ภาพสำหรับ Validation
    │   ├── val_gt.txt
    │   ├── test.txt                        # รายชื่อไฟล์ภาพสำหรับ Test ทั้งหมด
    │   └── test_split/                     # โฟลเดอร์เฉพาะใน CULane ที่แบ่งการ Test ตามสภาพแวดล้อม
    └── annotations_new/
```
### **TuSimple Dataset**
เป็น benchmark สำหรับ lane detection บนทางหลวงในสหรัฐอเมริกา 
มีจำนวนภาพ 6,408 ภาพ แบ่งเป็น train: 3,626 ภาพ , val 358 ภาพและ test 2,782 ภาพ มีความละเอียด 1280×720 พิกเซล มีสภาพอากาศที่หลากหลาย ใน test set

```text
    TUSimple/
    ├── test_set/
    │   ├── clips/
    │   │   ├── 0530/                        # ด้านในเป็นโฟลเดอร์ ของแต่ละคลิปวิดีโอ ที่รันเลขไปเรื่อยๆ
    │   │   ├── 0531/
    │   │   └── 0601/
    │   ├── readme.md
    │   └── test_tasks_0627.json             # ไฟล์ระบุว่าต้องทดสอบกับคลิป/เฟรมไหนบ้าง
    ├── train_set/
    │   ├── clips/
    │   │   ├── 0313-1/
    │   │   ├── 0313-2/
    │   │   ├── 0531/
    │   │   └── 0601/
    │   ├── seg_label/                      # โฟลเดอร์สำหรับ Segmentation Mask สร้างไว้เทรนโมเดลจำพวก Segmentation
    │   │   ├── 0313-1/
    │   │   ├── 0313-2/
    │   │   ├── 0530/
    │   │   ├── 0531/
    │   │   ├── 0601/
    │   │   └── list/
    │   │       ├── test.json               # รวม Path ของข้อมูลที่แบ่งไว้สำหรับ Test
    │   │       └── train_val.json          # รวม Path ของข้อมูลที่แบ่งไว้สำหรับ Train และ Validation
    │   ├── label_data_0313.json            # ไฟล์ JSON เก็บพิกัด (x, y) ของเส้นเลนสำหรับชุดนั้น
    │   ├── label_data_0531.json
    │   ├── label_data_0601.json
    │   └── readme.md
    ├── test_label.json                     # Ground Truth สำหรับใช้วัดผลความแม่นยำของ Test Set
    └── test_label_new.json                 # Ground Truth สำหรับ Test Set (เวอร์ชันอัปเดต)
```


# ข้อดี-ข้อเสีย
- Cityscapes 

    **ข้อดี** เป็น Dataset ที่มีความหลากหลายสูงมาก จาก 50 เมือง เหมาะกับงานพัฒนาแบบหลายโมดูลร่วมกัน และมี label id ที่ชัดเจน

    **ข้อเสีย** การใช้งานยากที่สุด มีโฟลเดอร์ซับซ้อน และมีไฟล์หลายประเภท และภาพมีความละเอียดสูงทำให้ใช้ VRAM สูงในการฝึก 
- CULane 

    **ข้อดี** เป็น Dataset ที่มีขนาดใหญ่จากสถานที่จริง และมีสภาพแวดล้อมที่หลากหลาย ทำให้โมเดลเรียนรู้ฟีเจอร์ได้ดี แล้วยังมีไฟล์เก็บพิกัดแยก ทำให้ยืนหยุ่นขึ้นในการสร้าง mask ใหม่ด้วยตนเอง 

    **ข้อเสีย** มีโฟลเดอร์ที่ซับซ้อน ทำให้ต้องจัดการพาร์ทให้ดี และการใช้เส้นแบบ Cubic Splines ทำให้บางจุดมี moise สูง
- TuSimple 

    **ข้อดี** ใช้งานง่าย มีโครงสร้างเป็น JSON ที่ตรงไปตรงมา

    **ข้อเสีย** มีปริมาณข้อมูลน้อย และไม่หลากหลาย ข้อมูลเป็นลายเส้นตรงที่ชัดเจน ทำให้เมื่อนำมาใช้จะมีโอกาศผิดพลาดสูงเมื่อใช้กับสภาพแวดล้อมที่ไม่เคยเห็น 


# การนำมาใช้งานกับ YOLO
### Cityscapes Dataset
เลือกคลาสที่เกี่ยวข้อง: Road, Lane markings จาก 30 คลาส
แปลง Polygon เป็น YOLO format:
อ่าน polygon จาก JSON files
แปลงเป็น normalized coordinates (0-1)
บันทึกเป็น .txt files
### CULane Dataset
ขั้นตอนการแปลง:
อ่าน annotation files (.txt):
แต่ละไฟล์มี x,y coordinates ของ lane key points
สร้าง segmentation masks:
ใช้ cubic splines สร้างเส้น lane
สร้าง polygon รอบเส้น lane
แปลงเป็น YOLO format:
Normalize coordinates
บันทึกเป็น .txt files
### TuSimple Dataset
ขั้นตอนการแปลง:
อ่าน JSON annotation files:
Parse lanes และ h_samples
สร้าง lane coordinates:
ผสม lanes กับ h_samples เพื่อได้ (x, y) points
แปลงเป็น YOLO format




