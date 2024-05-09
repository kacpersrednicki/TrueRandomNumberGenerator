import cv2
from frame_motion_module import process_frame_motion
from chaotic_map_module import generate_number_chaotic_map


def generate_random_numbers(video_path, sensitivity, motion_area_size, n_bits):
    """
    Funkcja generująca liczby losowe z wykorzystaniem modułów frame_motion_module i chaotic_map_module
    :param video_path: Ścieżka do pliku wideo
    :param sensitivity: Czułość generatora liczb z ruchu; im mniejsza wartość, tym generator jest czulszy
    :param n_bits: Liczba bitów, na której ma być możliwe zapisanie każdej z wygenerowanych liczb
    :param motion_area_size: Minimalny rozmiar obszaru ruchu, który ma być brany pod uwagę
    :return: Lista wygenerowanych liczb losowych
    """

    # Wczytanie pliku wideo
    cap = cv2.VideoCapture(video_path)

    # Inicjalizacja
    unused_numbers = []
    generated_numbers = []
    Q = 0.5
    g = 0.5

    # Wczytanie pierwszej klatki
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # wygenerowanie tablic r_values, s_values i t_values na podstawie ruchu
        lst1, lst2, lst3, prev_gray, unused_numbers = process_frame_motion(frame, prev_gray, unused_numbers,
                                                                           sensitivity, motion_area_size)
        # wygenerowanie liczby loswej na podstawie chaotic map
        random_number, Q, g = generate_number_chaotic_map(frame, lst1, lst2, lst3, Q, g, 4, n_bits)
        # dodanie wygenerowanej liczby losowej do końcowej listy
        generated_numbers.append(random_number)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    while None in generated_numbers:
        if None in generated_numbers:
            generated_numbers.remove(None)

    return generated_numbers


def generate_single_number(video_path, sensitivity, motion_area_size, n_bits):
    """
    Funkcja generująca jedną liczbę losową z wykorzystaniem modułów frame_motion_module i chaotic_map_module
    :param video_path: Ścieżka do pliku wideo
    :param sensitivity: Czułość generatora liczb z ruchu; im mniejsza wartość, tym generator jest czulszy
    :param motion_area_size: Minimalny rozmiar obszaru ruchu, który ma być brany pod uwagę
    :param n_bits: Liczba bitów, na której ma być możliwe zapisanie każdej z wygenerowanych liczb
    :return: Wygenerowana liczba losowa
    """

    # Wczytanie pliku wideo
    cap = cv2.VideoCapture(video_path)

    # Inicjalizacja
    unused_numbers = []
    Q = 0.5
    g = 0.5
    random_number = None

    # Pobranie pierwszej klatki
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while random_number is None:
        # Pobranie kolejnej klatki
        ret, frame = cap.read()
        if not ret:
            break

        # Generowanie liczby losowej na podstawie dwóch kolejnych klatek
        lst1, lst2, lst3, prev_gray, unused_numbers = process_frame_motion(frame, prev_gray, unused_numbers,
                                                                           sensitivity, motion_area_size)
        random_number, Q, g = generate_number_chaotic_map(frame, lst1, lst2, lst3, Q, g, 4, n_bits)

    cap.release()
    cv2.destroyAllWindows()

    return random_number
