# auxiliary functions


# Selection sort
def selection_sort(data, key):
    """
    first, the function calculates the minimum of the elements and places it in the first position, and then
    it moves to the next position calculating the minimum of the elements that are left and places it after
    the first minimum, and so on, until the sorting is done
    :param data:
    :param key:
    :return:
    """
    for i in range(len(data)):
        min_index = i
        for j in range(i+1, len(data)):
            if key(data[j]) < key(data[min_index]):
                min_index = j
        (data[i], data[min_index]) = (data[min_index], data[i])


# Filter function
def filter_elements(data, key):
    """
    from last element to the first so that we aren't affected by the length being shortened in the for loop
    :param data:
    :param key:
    :return:
    """
    index = 0
    while index < len(data):
        if not key(data[index]):
            data.remove(data[index])
        else:
            index += 1
    return data


