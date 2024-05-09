from generator import generate_random_numbers

video_path = '../res/bacteria1.mp4'
generated_numbers = generate_random_numbers(video_path, 10, 100, 8)
print('Wygenerowane liczby:', generated_numbers)
print('Ile liczb:', len(generated_numbers))
