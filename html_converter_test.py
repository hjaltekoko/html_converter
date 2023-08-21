# Importing the Streamlit library
import streamlit as st

# Defining the text_to_html_final_attempt function
def text_to_html_final_attempt(text):
    # Splitting text into lines and removing empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    # Defining special characters that indicate the end of a sentence
    special_characters = ['.', '!', ';', ':']

    # Helper function to identify the type of line
    def get_line_type(line, next_line=None, prev_line=None):
        # If the line ends with a special character or contains a question mark, it's a paragraph
        if any(char for char in special_characters if line.endswith(char)) or '?' in line:
            return 'paragraph'
        # If the next line isn't a new sentence and the previous line wasn't either, it's a list item
        elif next_line and not any(char for char in special_characters if next_line.endswith(char)):
            return 'listitem'
        elif prev_line and not any(char for char in special_characters if prev_line.endswith(char)):
            return 'listitem'
        # Otherwise, it's a headline
        else:
            return 'headline'

    # Storing the HTML output
    html_output = []
    # Flag to track if we're currently inside a list
    is_list = False
    prev_line = None

    # Looping through each line in the input text
    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else None
        # Determining the type of the current line
        line_type = get_line_type(line, next_line, prev_line)

        # Handling list items
        if line_type == 'listitem':
            # If not already in a list, start a new unordered list
            if not is_list:
                html_output.append('<ul>')
                is_list = True
            # Adding the current line as a list item
            html_output.append(f'<li>{line}</li>')
        else:
            # If inside a list, close the list
            if is_list:
                html_output.append('</ul>')
                is_list = False

            # Handling headlines and paragraphs
            if line_type == 'headline':
                # Adding the current line as a headline
                html_output.append(f'<h2>{line}</h2>')
            elif line_type == 'paragraph':
                # Adding the current line as a paragraph
                html_output.append(f'<p>{line}</p>')

        # Storing the current line as the previous line for the next iteration
        prev_line = line

    # Closing any open list tag if applicable
    if is_list:
        html_output.append('</ul>')

    # Joining the HTML lines to form the final HTML output
    return "\n".join(html_output)

# Streamlit interface
st.title("HTML Converter")

# Text area for user input
user_input = st.text_area("Enter your text here:")

# Button to trigger the conversion process
if st.button("Convert to HTML"):
    # Calling the conversion function and storing the HTML output
    html_output = text_to_html_final_attempt(user_input)
    # Displaying the generated HTML in a text area
    st.text_area("Generated HTML:", html_output, height=300)
    # Displaying the rendered HTML using markdown (unsafe_allow_html=True is required for HTML rendering)
    st.markdown("### Rendered HTML:")
    st.markdown(html_output, unsafe_allow_html=True)
