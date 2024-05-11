from typing import *

def add(values: List[float]) -> float:
    """
    Adds all values.
    """
    total = 0
    for x in values:
        if x < 0:
            total = total + x
    return total

def subtract(values: List[float]) -> float:
    """
    Subtracts all positive values
    """
    positive_v = []
    for value in values:
        if value > 0:
            positive_v.append(value)
    if not positive_v:
        return 0
    sum_of_p = 0
    for value in positive_v:
        sum_of_p = sum_of_p + value
    first_p = positive_v[0]
    difference = 2 * first_p - sum_of_p
    return difference

def multiply(values: List[float]) -> float:
    """
    Multiplies all non-zero values
    """
    product = 1
    non_zero_found = False
    for value in values:
        if value == 0:
            continue
        non_zero_found = True
        product = product * value    
    return product if non_zero_found else 0

def divide(values: List[float]) -> float:
    answer = values[0]
    if answer == 0 and 0 in values[1:]:
        print("Cannot divide by 0")
        sys.exit()
    if any(value == 0 for value in values[1:]):
        print("Cannot divide by 0")
        sys.exit()
    for value in values[1:]:
        answer = answer / value
    return answer

def circle(radius: str) -> Union[str, float]:
    """
    Calculates the area of a circle with radius
    """
    try:
        radius = float(radius)
        if radius <= 0:
            return 'Values must be positive'
        return 3.14159 * radius * radius
    except ValueError:
        return 'Enter numeric values'

def square(side: str) -> Union[str, float]:
    """
    area of a square given side 
    """
    try:
        side = float(side)
        if side <= 0:
            return 'Values must be positive'
        return side * side
    except ValueError:
        return 'Enter numeric values'

def rectangle(length: str, width: str) -> Union[str, float]:
    """
    area of a rectangle given length and width
    """
    try:
        length = float(length)
        width = float(width)
        if length <= 0 or width <= 0:
            return 'Values must be positive'
        return length * width
    except ValueError:
        return 'Enter numeric values'

def triangle(base: str, height: str) -> Union[str, float]:
    """
    area of a triangle given the base and height
    """
    try:
        base = float(base)
        height = float(height)
        if base <= 0 or height <= 0:
            return 'Values must be positive'
        return 0.5 * base * height
    except ValueError:
        return 'Enter numeric values'
