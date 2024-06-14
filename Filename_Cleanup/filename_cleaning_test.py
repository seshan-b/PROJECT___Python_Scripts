import os

def clean_name(name, mode):
    """
    Function to clean the name by removing or replacing special characters.
    """
    # Define a set of special characters to remove (except space and &)
    special_characters = set('<>:"/\\|?*^.()%[]')
    
    # Initialize cleaned_name as an empty string
    cleaned_name = ""
    
    # For each character in name:
    for i, char in enumerate(name):
        # If character is a space, use an underscore
        if char == ' ':
            cleaned_name += '_'
        # If character is &, replace with _and_
        elif char == '&':
            if i > 0 and name[i-1] != '_':
                cleaned_name += '_'
            cleaned_name += 'and'
            if i < len(name) - 1 and name[i+1] != '_':
                cleaned_name += '_'
        # If character is not in special characters set, append it to cleaned_name
        elif char not in special_characters:
            cleaned_name += char

    # Remove leading or trailing underscores or hyphens
    cleaned_name = cleaned_name.strip('_-')
    
    return cleaned_name

def test_clean_name_manual_input():
    # Prompt the user for manual input
    user_input = input("Enter file names separated by commas: ").strip()
    mode = input("Enter mode ('clean' or 'clean_full'): ").strip().lower()
    
    if mode not in ['clean', 'clean_full']:
        print("Invalid mode selected.")
        return
    
    file_names = [name.strip() for name in user_input.split(',')]
    
    print("\nOriginal and cleaned file names:")
    for file_name in file_names:
        cleaned_name = clean_name(file_name, mode)
        print(f"Original: {file_name} -> Cleaned: {cleaned_name}")

if __name__ == '__main__':
    test_clean_name_manual_input()
