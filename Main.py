import time
import numpy as np
import mss
import cv2
import mouseinfo
import pyautogui
from ultralytics import YOLO


model = YOLO('best.pt')  


capture_width = 300
capture_height = 500


clicked = False


while True:
    
    x, y = mouseinfo.position()

   
    left = max(0, x - capture_width // 2)
    top = max(0, y - capture_height // 2)

    with mss.mss() as sct:
        scr = sct.grab({
            "left": left,
            "top": top,
            "width": capture_width,
            "height": capture_height,
        })

       
        frame = np.array(scr)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        
        results = model.predict(source=frame, conf=0.5, verbose=False)

     
        for result in results:
            for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
                x1, y1, x2, y2 = map(int, box.tolist())
                class_id = int(cls)
                label = f"{result.names[class_id]} {conf:.2f}"

                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                
                if conf > 0.55 and not clicked and result.names[class_id] == 'ripple':  
                    pyautogui.click()
                    time.sleep(3)
                    pyautogui.click()
                    clicked = True

        
        if clicked and len(results[0].boxes) == 0:
            clicked = False

        
        cv2.imshow("Trojan", frame)
        cv2.setWindowProperty("Trojan", cv2.WND_PROP_TOPMOST, 1)

        
        if cv2.getWindowProperty("Trojan", cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


    time.sleep(0.01)






