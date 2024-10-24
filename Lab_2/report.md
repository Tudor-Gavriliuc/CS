# Letter Frequency Substitution Tool

## Overview

This report outlines the functionality of a dynamic interactive tool for decrypting text using letter frequency substitution. The tool processes an encrypted text file and allows for user-defined substitutions of letters based on frequency analysis.

## Functionality

1. **Reading Encrypted Text**:
   - The tool reads an encrypted text file, decoding it to upper case using various encodings.

2. **Letter Substitution**:
   - Users can replace specific letters in the decrypted text with new letters through a simple input interface.
   - The substitutions are recorded for potential undo actions.

3. **Frequency Analysis**:
   - The frequency of each letter in the decrypted text is calculated and displayed graphically.
   - The frequency of letters in the English language is also plotted for comparison.

4. **Output**:
   - The decrypted text can be downloaded after the substitutions are applied.

## Key Functions

- `find_frequency(text)`: Calculates the frequency of each letter in the provided text.
- `plot_frequency(frequency, label)`: Generates bar charts for visual representation of letter frequencies.
- `substitute_letters(text, original_letter, new_letter)`: Performs the substitution of letters in the text.
- `write_to_file(text, filename)`: Saves the modified text to a specified file.
- `read_from_file(filename)`: Reads text from a specified file.

## Usage

- **Upload** an encrypted text file to the application.
- Specify the **letter to replace** and the **new letter**.
- Click the **Apply Substitution** button to update the text.
- Review the **Decrypted Text** and its **Frequency Analysis**.
- Use the **Undo Last Substitution** feature to revert changes if necessary.
- Finally, download the decrypted text using the **Download** button.

## Visualizations

- The tool provides multiple visualizations:
  - **Decrypted Text Letter Frequencies**
  - **Unused Letters Frequencies**
  - **English Language Letter Frequency Comparison**

## Conclusion

This interactive tool effectively assists users in decrypting text through letter substitution and frequency analysis, providing a user-friendly interface for real-time updates and visual feedback.

