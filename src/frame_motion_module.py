import cv2
import numpy as np


def process_frame_motion(frame, prev_gray, unused_numbers, sensitivity, motion_area_size):
    """
    Funkcja generująca z ruchu listy r, s, t liczb do wykorzystania w chaotic_map_module
    :return: Trzy wygenerowane i odpowiednio sformatowane listy liczb do wykorzystania w chaotic_map_module oraz Lista
    wygenerowanych liczb, które nie zostały wykorzystane
    """

    # Konwersja klatki na obraz w skali szarości
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Obliczenie różnicy między klatkami
    diff = cv2.absdiff(prev_gray, gray)

    # Progowanie obrazu różnicy
    _, thresh = cv2.threshold(diff, sensitivity, 255, cv2.THRESH_BINARY)

    # Znalezienie konturów na obrazie progowanym
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_areas = []

    # Iteracja po konturach
    for contour in contours:
        # Jeśli obszar konturu jest wystarczająco duży, dodaj go do obszarów ruchu
        if cv2.contourArea(contour) > motion_area_size:
            motion_areas.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            # Rysowanie prostokąta wokół obszaru ruchu
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Generowanie liczb losowych na podstawie obszarów ruchu
    random_numbers = generate_list_of_numbers_from_motion_areas(motion_areas)

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

    # Podział wygenerowanych liczb na trzy listy składające się z czterech liczb
    lst1 = random_numbers[:4]
    lst2 = random_numbers[4:8]
    lst3 = random_numbers[8:12]

    formatted_lst1 = integer_to_float_list(lst1, 3)
    formatted_lst2 = integer_to_float_list(lst2, 0)
    formatted_lst3 = integer_to_float_list(lst3, 0)

    # Wyświetlenie klatek z rysowaniem obszarów ruchu
    cv2.imshow('Motion Detection', frame)

    prev_gray = gray

    return formatted_lst1, formatted_lst2, formatted_lst3, prev_gray, unused_numbers


def generate_list_of_numbers_from_motion_areas(motion_areas):
    """
    Funkcja generująca listę liczb losowych z obszarów ruchu
    """
    random_numbers = []
    for area in motion_areas:
        # Generowanie liczby losowej na podstawie wielkości obszaru ruchu
        random_numbers.append(np.sum(area) // 100)  # Skalowanie wartości obszaru ruchu
    return random_numbers


def fill_missing_numbers(prev_unused_numbers, required_count, generated_numbers):
    """
    Funkcja uzupełniająca listę wygenerowanych z obszarów ruchu liczb nadmiarowymi i niewykorzystanymi wcześniej
    wartośćiami w sytuacji, gdy wygenerowano mniej niż liczb niż jest wymagane
    """
    if required_count <= len(prev_unused_numbers):
        selected_numbers = prev_unused_numbers[:required_count]
        generated_numbers.extend(selected_numbers)
        prev_unused_numbers = prev_unused_numbers[required_count:]
    else:
        print('Brakuje liczb wygenerowanych z ruchu')
    return generated_numbers, prev_unused_numbers


def maintain_max_list_size(lst, max_size):
    """
    Funkcja ograniczająca rozmiar listy z niewykorzystanymi wcześniej wartościami, w celu kontroli wydajności
    """
    lst_length = len(lst)
    index_to_cut = lst_length - max_size
    lst = lst[index_to_cut:]
    return lst


def integer_to_float_list(integer_list, units_digit):
    """
    Funkcja konwertująca wygenerowance z ruchu wartości do wymaganej w algorytmie Chaotic map postaci
    """
    float_list = []
    for num in integer_list:
        num_str = str(num)
        fraction = str(units_digit) + '.' + num_str[::-1]  # Odwróć string i dodaj cyfrę jedności
        float_list.append(float(fraction))
    return float_list
