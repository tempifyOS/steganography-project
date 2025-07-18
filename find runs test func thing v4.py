#Note: AI was used to help debug these functions
#I'm like 90% sure this works but if there's an issue lemme know - lawrence
def find_all_runs(s: str, M: int):
    """
    Finds all non-overlapping runs of at least length M in the binary string s.

    Parameters:
    - s (str): A string of '0's and '1's.
    - M (int): The minimum length of a run.

    Returns:
    - list of tuples: Each tuple is (start_index, end_index, character) for a valid run.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    runs = []
    i = 0
    n = len(s)

    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        if run_length >= M:
            runs.append((start, i - 1, run_char))

    return runs


def find_runs_and_convert_to_output_string(s: str, M: int) -> str:
    """
    Finds all non-overlapping runs of at least length M in the binary string s.
    For each run:
      - Appends '1' to the output if the run length is odd
      - Appends '0' if the run length is even

    Parameters:
    - s (str): A string of '0's and '1's.
    - M (int): The minimum run length.

    Returns:
    - str: A string of '0's and '1's representing parity of each qualifying run.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i = 0
    n = len(s)
    output = ""

    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        if run_length >= M:
            output += '1' if run_length % 2 == 1 else '0'

    return output


def count_runs(s, M):
    """Count the number of runs of length >= M in the string."""
    count = 0
    i = 0
    n = len(s)
    
    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        if i - start >= M:
            count += 1
    
    return count

def hide_message_and_obfuscate(s: str, message: str, M: int, strict=True) -> str:
    """
    Hides a binary message in runs of a binary string and prevents decoding beyond the message length.
    If strict=True, raises an error if there are not enough runs to encode the message.
    """
    if M <= 0:
        raise ValueError("M must be greater than 0.")
    
    if not message:
        # If no message to encode, just break all runs
        return break_all_runs(s, M)

    # Check if cover string is long enough to hold the message
    min_length_needed = calculate_minimum_length(message, M)
    if len(s) < min_length_needed:
        raise ValueError(f"Cover string length {len(s)} is too short to encode message '{message}'. "
                        f"Minimum length needed: {min_length_needed}")

    s = list(s)
    n = len(s)

    # Count available runs if in strict mode
    if strict:
        available_runs = count_runs(s, M)
        if available_runs < len(message):
            raise ValueError(f"Not enough runs of length ≥ {M} to encode message of length {len(message)}")

    # Encode each message bit
    for msg_bit_idx in range(len(message)):
        s = encode_message_bit(s, message[msg_bit_idx], msg_bit_idx, M)
    
    # Break any remaining runs after the message
    s = break_remaining_runs(s, len(message), M)
    
    return ''.join(s)


def calculate_minimum_length(message, M):
    """
    Calculate the minimum length needed to encode a message.
    
    For each bit in the message:
    - '0' needs an even run of length >= M (minimum M characters if M is even, M+1 if M is odd)
    - '1' needs an odd run of length >= M (minimum M characters)
    
    Returns the minimum total length needed.
    """
    total_length = 0
    for bit in message:
        if bit == '1':
            # Need odd run of length >= M
            total_length += M
        else:
            # Need even run of length >= M
            if M % 2 == 0:
                total_length += M  # M is already even
            else:
                total_length += M + 1  # Need M+1 to make it even
    
    return total_length


def encode_message_bit(s, message_bit, target_run_index, M):
    """Encode a single message bit into the target_run_index-th run."""
    desired_parity = int(message_bit)
    
    # Find the target run
    runs_found = 0
    i = 0
    n = len(s)
    
    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        
        if run_length >= M:
            if runs_found == target_run_index:
                # This is our target run
                actual_parity = run_length % 2
                
                if actual_parity != desired_parity:
                    # Need to change parity by adjusting length
                    if run_length > M:
                        # Safe to shorten - flip the last character to break the run
                        s[i - 1] = '1' if s[i - 1] == '0' else '0'
                    else:
                        # run_length == M, need to extend by 1
                        if i < n:
                            # Extend forward by converting next char
                            s[i] = run_char
                        elif start > 0:
                            # Extend backward by converting previous char
                            s[start - 1] = run_char
                        else:
                            # No choice but to shorten (this will break the run)
                            s[i - 1] = '1' if s[i - 1] == '0' else '0'
                
                break
            
            runs_found += 1
    
    return s


def break_remaining_runs(s, encoded_message_length, M):
    """Break all runs that come after the encoded message."""
    runs_found = 0
    i = 0
    n = len(s)
    
    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        
        if run_length >= M:
            if runs_found >= encoded_message_length:
                # This run is beyond our message, break it
                mid = start + run_length // 2
                s[mid] = '1' if s[mid] == '0' else '0'
                # Restart from the beginning of the modified area
                i = start
                continue
            runs_found += 1
    
    return s


def break_all_runs(s, M):
    """Break all runs of length >= M by flipping their middle character."""
    s = list(s)
    i = 0
    n = len(s)
    
    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        
        if run_length >= M:
            mid = start + run_length // 2
            s[mid] = '1' if s[mid] == '0' else '0'
            i = start  # Restart from the beginning of the modified area
        
    return ''.join(s)


def test_stego(s, message, M, expected_output):
    try:
        encoded = hide_message_and_obfuscate(s, message, M)
        decoded = find_runs_and_convert_to_output_string(encoded, M)
        print(f"Original: {s}")
        print(f"Message : {message}")
        print(f"Encoded : {encoded}")
        print(f"Decoded : {decoded}")
        print(f"✅ Pass\n" if decoded == expected_output else f"❌ Fail (expected {expected_output})\n")
    except ValueError as e:
        print(f"Original: {s}")
        print(f"Message : {message}")
        print(f"❌ Error: {e}\n")


# Test cases
test_stego("00110011", "", 3, "")
test_stego("00110011", "1", 3, "1")
test_stego("00110011", "10", 3, "10")
test_stego("000111000111", "10", 3, "10")
test_stego("000000111111", "01", 3, "01")
test_stego("000011100000111", "101", 3, "101")
test_stego("0000000", "1", 3, "1")
test_stego("00110011", "", 3, "")
test_stego("000111000111000111000", "10101", 3, "10101")
test_stego("000111000111", "11", 3, "11")
test_stego("000111", "10", 3, "10")  # This was the failing test
test_stego("000011110000", "11", 3, "11")
test_stego("0101010101", "", 3, "")
test_stego("0001110001110001110001000000111000100000011100011100011111000111000111001000000111000111000110111000000100000011100011100011111000110000001110001110001111000111000", "10101", 4, "10101")
