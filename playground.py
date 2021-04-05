import cv2
file_path = "../play/2.jpg"  # change to your own video path
img = cv2.imread(file_path)
height = img.shape[0]
width = img.shape[1]
print(height, width)