import cv2
import numpy as np


# Funkcja generująca liczby losowe na podstawie obszarów ruchu
def generate_random_numbers(areas_of_motion):
    generated_numbers = []
    for area in areas_of_motion:
        # Generowanie liczby losowej na podstawie wielkości obszaru ruchu
        generated_numbers.append(np.sum(area) // 100)  # Skalowanie wartości obszaru ruchu
    return generated_numbers


# Funkcja uzupełniająca brakujące wartości
def fill_missing_numbers(prev_unused_numbers, how_many_missing, generated_numbers):
    if how_many_missing <= len(prev_unused_numbers):
        selected_numbers = prev_unused_numbers[:how_many_missing]
        generated_numbers.extend(selected_numbers)
        prev_unused_numbers = prev_unused_numbers[how_many_missing:]
    else:
        print('Brakuje liczb wygenerowanych z ruchu')
    return generated_numbers, prev_unused_numbers


def maintain_max_list_size(lst, max_size):
    lst_length = len(lst)
    index_to_cut = lst_length - max_size
    lst = lst[index_to_cut:]
    return lst


def integer_to_float_array(integer_array, units_digit):
    float_array = []
    for num in integer_array:
        num_str = str(num)
        fraction = str(units_digit) + '.' + num_str[::-1]  # Odwróć string i dodaj "0."
        float_array.append(float(fraction))
    return float_array


# Wczytanie pliku wideo
cap = cv2.VideoCapture('../res/bacteria1.mp4')

# Inicjalizacja listy przechowującej wszystkie wygenerowane liczby losowe
unused_numbers = []
streaks_without_generation = []
no_generation_streak = 0

# Wczytanie pierwszej klatki
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while cap.isOpened():
    # Wczytanie kolejnej klatki
    ret, frame = cap.read()
    if not ret:
        break

    # Konwersja klatki na obraz w skali szarości
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Obliczenie różnicy między klatkami
    diff = cv2.absdiff(prev_gray, gray)

    # Progowanie obrazu różnicy
    _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

    # Znalezienie konturów na obrazie progowanym
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_areas = []

    # Iteracja po konturach
    for contour in contours:
        # Jeśli obszar konturu jest wystarczająco duży, dodaj go do obszarów ruchu
        if cv2.contourArea(contour) > 100:
            motion_areas.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            # Rysowanie prostokąta wokół obszaru ruchu (opcjonalne)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # print(motion_areas)
    # Generowanie liczb losowych na podstawie obszarów ruchu
    random_numbers = generate_random_numbers(motion_areas)
    # print('wygenerowane: ', random_numbers)
    print('kolejna klatka:')
    print('ile wygenerowano:', len(random_numbers))

    if len(random_numbers) < 4:
        no_generation_streak += 1
    else:
        streaks_without_generation.append(no_generation_streak)
        no_generation_streak = 0

    # Uzupełnienie tablic brakującymi liczbami
    required_count = 12 - len(random_numbers)
    if required_count > 0:
        random_numbers, unused_numbers = fill_missing_numbers(unused_numbers, required_count, random_numbers)
    else:
        surplus_numbers = random_numbers[12:]
        random_numbers = random_numbers[:12]
        unused_numbers.extend(surplus_numbers)

    max_unused_list_size = 500
    if len(unused_numbers) > max_unused_list_size:
        unused_numbers = maintain_max_list_size(unused_numbers, max_unused_list_size)

    # Podział wygenerowanych liczb na trzy tablice składające się z czterech liczb
    arr1 = random_numbers[:4]
    arr2 = random_numbers[4:8]
    arr3 = random_numbers[8:12]

    formatted_aar1 = integer_to_float_array(arr1, 3)
    formatted_aar2 = integer_to_float_array(arr2, 0)
    formatted_aar3 = integer_to_float_array(arr3, 0)

    # Wyświetlenie klatek z rysowaniem obszarów ruchu (opcjonalne)
    cv2.imshow('Motion Detection', frame)

    # Wyświetlenie wygenerowanych tablic
    print("Wygenerowane tablice:")
    print("Tab1:", formatted_aar1)
    print("Tab2:", formatted_aar2)
    print("Tab3:", formatted_aar3)

    # print('nieużyte: ', unused_numbers)
    print('ile zapasowych:', len(unused_numbers))

    prev_gray = gray

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# print('max streak:', max(streaks_without_generation))
