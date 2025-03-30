import re

def extract_int(string):
    string = string.upper()
    
    # Define a regular expression pattern for Roman numerals (up to IV)
    roman_numeral_pattern = r'\b[IVXLCDM]+\b'
    
    # Use re.findall to extract all Roman numerals
    roman_numerals = re.findall(roman_numeral_pattern, string)

    num = 0

    if roman_numerals:
        # Extract the first match (if there are multiple Roman numerals)
        roman_numeral = roman_numerals[0]
        
        if roman_numeral == 'I':
            num = 1
        elif roman_numeral == 'II':
            num = 2
        elif roman_numeral == 'III':
            num = 3
        elif roman_numeral == 'IV':
            num = 4
    
    else:
        # Check for the word representations of numbers
        if 'FIRST' in string:
            num = 1
        elif 'SECOND' in string:
            num = 2
        elif 'THIRD' in string:
            num = 3
        elif 'FOURTH' in string:
            num = 4

    return num
