def simpleCipher(encrypted, k):
    result = ''
    for char in encrypted:
        index = ord(char) - ord('A')
        new_index = (index - k) % 26
        result += chr(new_index + ord('A'))
    return result

# Test with example from assignment
print(simpleCipher('VTAOG', 2))  # Expected: TRYME