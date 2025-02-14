#!/usr/bin/env python3

def process_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()[1:]  # Skip the first line (header)
    
    result = []
    for i in range(0, len(lines) - 1, 2):  # Process every 2 rows
        combined = lines[i].strip().replace(",", "") + lines[i+1].strip().replace(",", "")
        result.append(combined)
    
    return result

def binary_to_ascii(binary_list):
    # Each item in binary_list should be a valid binary string (e.g., '01101000')
    ascii_chars = []
    for binary in binary_list:
        # Split into chunks of 8 bits (1 byte)
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                ascii_chars.append(chr(int(byte, 2)))
    return "".join(ascii_chars)  # Join characters into a string

# Example usage
file_path = "input.csv"
output = process_file(file_path)
print(output)  # Prints the list of binary strings

# Assuming the output list is valid binary data
ascii_output = binary_to_ascii(output)
print(ascii_output)  # Prints the final ASCII string














# with open('input.csv', 'r') as f:
#     logic = f.read().strip().split('\n')  # Read file and split into lines

# # Skip the first line
# logic = logic[1:]

# # Convert each row into a list of binary digits (ignore non-binary characters)
# binary_rows = []
# for line in logic:
#     cleaned_line = ''.join(filter(lambda x: x in '01', line))  # Keep only '0' and '1'
#     binary_rows.append(list(map(int, cleaned_line)))


# # Ensure all rows have the same length
# if not all(len(row) == len(binary_rows[0]) for row in binary_rows):
#     raise ValueError("Rows must be of equal length")

# print("Binary rows:", binary_rows)



# # Sum corresponding elements from each row and take mod 2
# summed_binary = [str(sum(bits) % 2) for bits in zip(*binary_rows)]

# print("Summed binary:", summed_binary)

# # Convert binary string to ASCII
# binary_string = ''.join(summed_binary)



# # Ensure binary_string length is a multiple of 8 for proper ASCII conversion
# if len(binary_string) % 8 != 0:
#     binary_string = binary_string.ljust((len(binary_string) // 8 + 1) * 8, '0')  # Pad with zeros

# ascii_text = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))

# print("Decoded ASCII:", ascii_text)
