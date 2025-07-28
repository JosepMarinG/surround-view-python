import cv2

cap = cv2.VideoCapture(6)
ret, frame = cap.read()
cv2.imwrite("images/back.png", frame)
cap.release()

cap = cv2.VideoCapture(2)
ret, frame = cap.read()
cv2.imwrite("images/front.png", frame)
cap.release()

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite("images/right.png", frame)
cap.release()

cap = cv2.VideoCapture(4)
ret, frame = cap.read()
cv2.imwrite("images/left.png", frame)
cap.release()