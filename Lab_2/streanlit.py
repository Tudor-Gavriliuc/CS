import streamlit as st
from utils import *


def try_decode(file_content, encodings=['utf-8', 'iso-8859-1', 'windows-1252']):
    for encoding in encodings:
        try:
            return file_content.decode(encoding).upper()
        except UnicodeDecodeError:
            continue
    return None


st.title("Dynamic Interactive Letter Frequency Substitution Tool")

# Initialize session state
if 'encrypted_text' not in st.session_state:
    st.session_state.encrypted_text = ""
if 'decrypted_text' not in st.session_state:
    st.session_state.decrypted_text = ""
if 'substitution_history' not in st.session_state:
    st.session_state.substitution_history = []
if 'unused' not in st.session_state:
    st.session_state.unused = unused.copy()
if 'previous_states' not in st.session_state:
    st.session_state.previous_states = []  # Store previous states for undo

# File uploader for the encrypted text file
uploaded_file = st.file_uploader("Upload Encrypted File", type=["txt"])

if uploaded_file is not None:
    # Read and display the uploaded encrypted text
    file_content = uploaded_file.read()
    st.session_state.encrypted_text = try_decode(file_content)

    if st.session_state.encrypted_text is None:
        st.error("Unable to decode the file. Please check the file encoding.")
    else:
        if not st.session_state.decrypted_text:
            st.session_state.decrypted_text = st.session_state.encrypted_text
        st.write("### Encrypted Text:")
        st.text_area("Encrypted Text", st.session_state.encrypted_text, height=200)

        # Single replacement input
        col1, col2, col3 = st.columns(3)
        with col1:
            old_letter = st.text_input("Replace:", max_chars=1, key="old_letter").upper()
        with col2:
            new_letter = st.text_input("With:", max_chars=1, key="new_letter").lower()
        with col3:
            if st.button("Apply Substitution"):
                if old_letter and new_letter:
                    # Save current state for undo
                    st.session_state.previous_states.append({
                        "decrypted_text": st.session_state.decrypted_text,
                        "substitution_history": st.session_state.substitution_history.copy(),
                        "unused": st.session_state.unused.copy(),
                    })

                    # Update decrypted text
                    st.session_state.decrypted_text = substitute_letters(st.session_state.decrypted_text, old_letter,
                                                                         new_letter)

                    # Append to substitution history
                    st.session_state.substitution_history.append(f"{old_letter} -> {new_letter}")

                    # Remove new letter from unused list
                    if new_letter.upper() in st.session_state.unused:
                        del st.session_state.unused[new_letter.upper()]

        # Undo button to revert to the last state
        if st.button("Undo Last Substitution") and st.session_state.previous_states:
            last_state = st.session_state.previous_states.pop()  # Restore last saved state
            st.session_state.decrypted_text = last_state["decrypted_text"]
            st.session_state.substitution_history = last_state["substitution_history"]
            st.session_state.unused = last_state["unused"]

        # Show the decrypted text
        st.write("### Decrypted Text:")
        st.text_area("Decrypted Text", st.session_state.decrypted_text, height=200)

        # Display substitution history
        st.write("### Substitution History:")
        for substitution in st.session_state.substitution_history:
            st.write(substitution)

        # Calculate frequencies
        decrypted_frequency = find_frequency(st.session_state.decrypted_text)

        st.write("### Letter Frequencies:")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Decrypted Text")
            fig1, ax1 = plt.subplots()
            ax1.bar(decrypted_frequency.keys(), decrypted_frequency.values())
            ax1.set_xlabel("Letters")
            ax1.set_ylabel("Frequency")
            st.pyplot(fig1)

        with col2:
            st.write("Unused Letters")
            fig2, ax2 = plt.subplots()
            ax2.bar(st.session_state.unused.keys(), st.session_state.unused.values())
            ax2.set_xlabel("Letters")
            ax2.set_ylabel("Frequency")
            st.pyplot(fig2)

        st.write("### English Language Letter Frequency")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.bar(english_language_letters_frequency.keys(), english_language_letters_frequency.values())
        ax3.set_xlabel("Letters")
        ax3.set_ylabel("Frequency")
        st.pyplot(fig3)

        # Download button for decrypted text
        st.download_button("Download Decrypted Text", st.session_state.decrypted_text, file_name="decrypted.txt")