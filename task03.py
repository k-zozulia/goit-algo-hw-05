import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1

def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def measure_search_time(search_func, text, pattern):
    setup_code = f"from __main__ import {search_func.__name__}, text, pattern"
    test_code = f"{search_func.__name__}(text, pattern)"
    times = timeit.repeat(setup=setup_code, stmt=test_code, repeat=5, number=100)
    return min(times)

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

text1 = load_text('article01.txt')
text2 = load_text('article02.txt')

patterns = {
    "existing": "Алгоритм",  
    "non_existing": "Сонце світило яскраво"
}

results = []

for text in [text1, text2]:
    for description, pattern in patterns.items():
        for search_func in [kmp_search, boyer_moore_search, rabin_karp_search]:
            time_taken = measure_search_time(search_func, text, pattern)
            results.append((search_func.__name__, description, time_taken))


with open("results.md", "w", encoding='utf-8') as f:
    f.write("# Результати порівняння алгоритмів пошуку підрядка\n\n")
    f.write("У цьому звіті представлено результати порівняння алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа.\n\n")
    
    f.write("## Результати вимірювання часу\n")
    f.write("| Алгоритм                  | Тип підрядка     | Час (секунди)   |\n")
    f.write("|---------------------------|------------------|------------------|\n")
    
    for algo_name, pattern_desc, time in results:
        f.write(f"| {algo_name:<25} | {pattern_desc:<16} | {time:.6f}        |\n")

    f.write("\n## Висновки\n")
    f.write("На основі вимірювання часу виконання для кожного алгоритму, можна зробити наступні висновки:\n")
    f.write("- Алгоритм, який продемонстрував найкращу швидкість для кожного тексту, варіюється залежно від специфіки тексту та підрядка.\n")
    f.write("- В цілому, ефективність алгоритмів може відрізнятися, але, як правило, алгоритм Боєра-Мура показує хороші результати на великих текстах.\n")
    f.write("- Алгоритми Кнута-Морріса-Пратта та Рабіна-Карпа також демонструють хорошу продуктивність, особливо для коротших підрядків.\n")