import streamlit as st

# The text_to_html_final_attempt function goes here
def text_to_html_final_attempt(text):
    # Split text into lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    special_characters = ['.', '!', ';', ':']

    # Helper function to identify type of line
    def get_line_type(line, next_line=None, prev_line=None):
        # If line ends with a special character, it's always a paragraph
        if any(char for char in special_characters if line.endswith(char)) or '?' in line:
            return 'paragraph'
        elif next_line and not any(char for char in special_characters if next_line.endswith(char)):
            return 'listitem'
        elif prev_line and not any(char for char in special_characters if prev_line.endswith(char)):
            return 'listitem'
        else:
            return 'headline'

    html_output = []
    is_list = False
    prev_line = None

    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else None
        line_type = get_line_type(line, next_line, prev_line)

        # Handle list items
        if line_type == 'listitem':
            if not is_list:
                html_output.append('<ul>')
                is_list = True
            html_output.append(f'<li>{line}</li>')
        else:
            if is_list:
                html_output.append('</ul>')
                is_list = False

            # Handle headlines and paragraphs
            if line_type == 'headline':
                html_output.append(f'<h2>{line}</h2>')
            elif line_type == 'paragraph':
                html_output.append(f'<p>{line}</p>')

        prev_line = line

    # Close any open tags
    if is_list:
        html_output.append('</ul>')

    return "\n".join(html_output)


# Streamlit interface
st.title("HTML Converter")

user_input = st.text_area("Enter your text here:")

if st.button("Convert to HTML"):
    html_output = text_to_html_final_attempt(user_input)
    st.text_area("Generated HTML:", html_output, height=300)
    st.markdown("### Rendered HTML:")
    st.markdown(html_output, unsafe_allow_html=True)