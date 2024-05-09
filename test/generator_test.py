import matplotlib.pyplot as plt
import cv2
from generator import generate_random_numbers

video_path = '../res/bacteria1.mp4'
generated_numbers = generate_random_numbers(video_path, 10, 100, 8)
print('Wygenerowane liczby:', generated_numbers)
print('Ile liczb:', len(generated_numbers))

video_capture = cv2.VideoCapture(video_path)
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
print("Liczba klatek w filmie:", total_frames)
video_capture.release()

plt.hist(generated_numbers, bins=6, edgecolor='black')
plt.title('Histogram wygenerowanych liczb losowych')
plt.xlabel('Wygenerowane wartości')
plt.ylabel('Częstość występowania')
plt.grid(True)
plt.show()
