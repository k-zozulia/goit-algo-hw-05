def binary_search_with_bounds(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return (iterations, upper_bound)


sorted_array = [0.5, 1.2, 3.4, 5.6, 7.8, 9.9, 12.5]
target_value = 6.0

result = binary_search_with_bounds(sorted_array, target_value)
print(result)