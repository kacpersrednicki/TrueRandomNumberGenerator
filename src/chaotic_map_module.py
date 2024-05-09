import numpy as np


def generate_number_chaotic_map(frame, r_values, s_values, t_values, Q_prev, g_prev, dec_length, n_bits, P_prev=0.5):
    """
    Funkcja generująca liczbę losową dla danej klatki filmu za pomocą algorytmu Chaotic map i list liczb wygenerowanych
    na podstawie ruchu w frame_motion_module
    :return: Wygenerowana liczba losowa
    """

    # Sytuacja, w której nie wypełniono list values
    if len(r_values) < 4 or len(s_values) < 4 or len(t_values) < 4:
        print('Niepełne tabllice z frame_motion()')
        return None, 0.5, 0.5

    # Przetwarzanie klatki i wybór wartości z list z frame_motion_module
    r, s, t = process_frame_select_parameters(frame, r_values, s_values, t_values)

    # Wykonanie równań duffing map i logistic map
    P_prev, Q_prev = duffing_map(P_prev, Q_prev, s, t)
    g_prev = logistic_map(g_prev, r)

    flag = 0
    formatted_Q_prev = format_generated_number(Q_prev, dec_length, flag)
    formatted_g_prev = format_generated_number(g_prev, dec_length, flag)
    if flag == 2:
        print('Niewystarczająca liczba cyfr')
        return None, 0.5, 0.5

    bin_Q_prev = integer_to_binary_fixed_length(formatted_Q_prev, n_bits)
    bin_g_prev = integer_to_binary_fixed_length(formatted_g_prev, n_bits)

    # Wygenerowanie liczby losowej poprzez połączenie map Duffinga i Logistycznej oraz wykonanie operacji XOR
    random_number = xor_of_binary_strings(bin_Q_prev, bin_g_prev)
    print(random_number)

    Q_prev = float("{:.3f}".format(abs(Q_prev)))
    g_prev = float("{:.3f}".format(abs(g_prev)))

    return random_number, Q_prev, g_prev


def xor_of_binary_strings(bin_str1, bin_str2):
    """
    Funkcja wykonująca operację xor dwóch stringów reprezentujących liczby binarne
    """
    res = int(bin_str1, 2) ^ int(bin_str2, 2)
    return res


def get_last_bit(num):
    """
    Funkcja pobierająca najmłodszy bit zapisu binarnego liczby
    """
    binary_num = bin(num)
    last = binary_num[-1]
    return int(last)


def get_second_last_bit(num):
    """
    Funkcja pobierająca drugi najmłodszy bit zapisu binarnego liczby
    """
    binary_num = bin(num)
    second_last = binary_num[-2]
    return int(second_last)


def integer_to_binary_fixed_length(number, n):
    """
    Funkcja konwertująca liczbę z postaci decymalnej do postaci binarnej o podanej długości bitowej
    """
    binary_string = bin(number)[2:]
    if len(binary_string) > n:
        binary_string = binary_string[-n:]
    padded_binary_string = binary_string.zfill(n)
    return padded_binary_string


def format_generated_number(val, n, flag):
    """
    Funkcja formatująca liczbę całkowitą zgodnie z podaną liczbą cyfr
    """
    str_val = str(val)
    decimal_part = str_val.split('.')[1]
    if len(decimal_part) >= n + 1:
        return int(decimal_part[1:1 + n])
    else:
        flag += 1
        return int(decimal_part)


def duffing_map(P_prev, Q_prev, a, b):
    """
    Funkcja implementująca algorytm Duffing map
    """
    P = Q_prev
    Q = -b * P_prev + a * Q_prev - (Q_prev ** 3)
    return P, Q


def logistic_map(g_prev, r):
    """
    Funkcja implementująca algorytm Logistic map
    """
    g = r * g_prev * (1 - g_prev)
    return g


def process_frame_select_parameters(frame, r_values, s_values, t_values):
    """
    Funkcja przetwarzająca klatkę filmu i obliczająca indeksy do wybrania wartości z list z frame_motion_module
    :return: Wartości r, s, t pobrane z obliczonych indeksów list
    """

    # Przekształcenie klatki do wartości liczbowej, średnia wartość kanałów RGB
    processed_data = np.mean(frame)
    formatted_processed_data = int(processed_data * (10 ** 6))

    # Wybór odpowiednich parametrów r, s, t na podstawie dwóch najmłodszych bitów
    k = get_second_last_bit(formatted_processed_data)
    m = get_last_bit(formatted_processed_data)

    if k == 0 and m == 0:
        r, s, t = r_values[0], s_values[0], t_values[0]
    elif k == 0 and m == 1:
        r, s, t = r_values[1], s_values[1], t_values[1]
    elif k == 1 and m == 0:
        r, s, t = r_values[2], s_values[2], t_values[2]
    elif k == 1 and m == 1:
        r, s, t = r_values[3], s_values[3], t_values[3]

    return r, s, t
