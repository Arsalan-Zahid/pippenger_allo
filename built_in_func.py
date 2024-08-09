# For Allo 
from typing import Iterable, Any, Callable, List, Generator, Union # Would this work or perhaps need to omit another module
                       # Maybe '...' could work but likely not 

# int 
# Copied from GPT
def int_allo(value: Union[str, float, int]) -> int:
    if isinstance(value, int):
        # If the value is already an integer, return it directly
        return value
    
    if isinstance(value, float):
        # For float, convert it to int by truncating the decimal part
        return int(value)  # This is used for conversion in the absence of int() itself

    if isinstance(value, str):
        # Handle string conversion by parsing the integer value
        # Initialize variables for parsing
        result = 0
        sign = 1
        index = 0
        
        # Check for optional sign
        if value[index] == '-':
            sign = -1
            index += 1
        elif value[index] == '+':
            index += 1
        
        # Process each character in the string
        while index < len(value):
            char = value[index]
            if '0' <= char <= '9':
                digit = ord(char) - ord('0')  # Convert char to integer digit
                result = result * 10 + digit
                index += 1
            else:
                raise ValueError(f"Invalid literal for integer with base 10: '{value}'")
        
        return sign * result
    
    # Handle unsupported types
    raise TypeError(f"Cannot convert type '{type(value).__name__}' to int")

# len
def len_allo(iterable: Iterable[Any]) -> int: 
    count: int = 0
    for i in iterable:
        count += 1
    return count

# list
def list_allo(iterable: Iterable = None) -> list[Any]:
    result: list[Any]= []
    
    if iterable is None:
        return result
    
    try:
        for i in iterable:
            result += [i]  
    except TypeError:
        # Raise an error if the input is not an iterable
        raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
    
    return result

# floor
def floor_allo(x: float) -> int:
    # Check if the input is an integer
    if x == int_allo(x):
        return int_allo(x)
    
    # For positive numbers, truncate the decimal part
    if x > 0:
        return int_allo(x)  
    
    # For negative numbers, convert to positive, truncate, and then negate
    else:

        floored = int_allo(-x)
        return -floored

# log2
# Copied from GPT
def log2_allo(x: int, tolerance: float =1e-10) -> int: 
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    
    # Handle the case where x is exactly 1
    if x == 1:
        return 0

    # Initialize bounds
    low: int = 0
    high: int = 1
    while (2 ** high) < x:
        high *= 2
    
    # Binary search to approximate the log2 value
    while high - low > tolerance:
        mid = (low + high) / 2
        if 2 ** mid < x:
            low = mid
        else:
            high = mid

    return (low + high) / 2

# map 
def map_allo(func: Callable, iterable: Iterable):  
     # To store results
    result: list[Any] = []

    # Iterate over the iterable
    for i in iterable:
        # Apply the function to each item and add the result to the result list
        result += [func(i)]
    
    return result

# combinations 
# Copied from GPT
def combinations_allo(iterable: Iterable, r: int) -> Generator[List, None, None]:
    # Convert the iterable to a list to work with indexing
    iterable = list(iterable)
    
    def combine(start: int, path: List) -> Generator[List, None, None]:
        # If the combination length is met, yield the combination
        if len(path) == r:
            yield path
            return
        # Generate combinations by recursion
        for i in range(start, len(iterable)):
            yield from combine(i + 1, path + [iterable[i]])
    
    return combine(0, [])

# append 
def append_allo(list_input: list[Any], item: Any) -> None:
    list_input += [item]

#min 
# TODO
def min_allo(): 
    pass

# zip 
# TODO
def zip_allo(): 
    pass

# tuple 
# TODO
def tuple_allo(): 
    pass 

# sum 
# TODO
def sum_allo(iterable: tuple[int, ...] | list[int], start: int) -> int: 
    pass


if __name__ == "__main__":
    # TODO: test the functions above here to make sure they work 
