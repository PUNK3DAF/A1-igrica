import cv2
import os

IMG_PATH = "screen.png"
SAVE_DIR = "."

img = cv2.imread(IMG_PATH)
if img is None:
    raise SystemExit("Nije pronađen 'screen.png' u trenutnom folderu.")

clone = img.copy()
cv2.namedWindow("image")

ix = iy = -1
rx = ry = -1
drawing = False
roi_ready = False
roi = None

def mouse_callback(event, x, y, flags, param):
    global ix, iy, rx, ry, drawing, roi_ready, roi, clone
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        drawing = True
        clone = img.copy()
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        clone = img.copy()
        cv2.rectangle(clone, (ix, iy), (x, y), (0,255,0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        rx, ry = x, y
        drawing = False
        roi_ready = True
        x1, y1 = min(ix, rx), min(iy, ry)
        x2, y2 = max(ix, rx), max(iy, ry)
        roi = img[y1:y2, x1:x2].copy()
        cv2.rectangle(clone, (x1, y1), (x2, y2), (0,255,0), 2)

cv2.setMouseCallback("image", mouse_callback)

print("Instrukcije: povuci levi klik da odabereš region. Pritisni 's' da sačuvaš selekciju, 'c' da obrišeš selekciju, 'q' za izlaz.")
count = 1
while True:
    cv2.imshow("image", clone)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        clone = img.copy()
        roi_ready = False
        roi = None
    if key == ord('s') and roi_ready and roi is not None:
        fname = input("Unesi ime fajla za snimanje (npr. good_top.png): ").strip()
        if fname == "":
            fname = f"template_{count}.png"
        path = os.path.join(SAVE_DIR, fname)
        cv2.imwrite(path, roi)
        print("Sačuvano:", path)
        count += 1
        roi_ready = False
        roi = None
        clone = img.copy()

cv2.destroyAllWindows()