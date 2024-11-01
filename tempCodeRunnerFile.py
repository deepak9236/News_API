from PIL import Image, ImageDraw, ImageFont

def create_news_image(image_path, headline, important_words, output_path):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define the font and text properties
    font_path = "./Arial.ttf"  # You may need to provide the path to a font file
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)

    # Define text color and highlight color
    text_color = (255, 255, 255)  # White color
    highlight_color = (255, 255, 0)  # Yellow color for highlights
    background_color = (0, 0, 0)  # Black background

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), headline, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = image.size
    text_position = (10, image_height - text_height - 10)

    # Draw the background rectangle for the text
    draw.rectangle([text_position, (image_width, image_height)], fill=background_color)

    # Draw the text with highlighting
    words = headline.split()
    x, y = text_position
    space_width = draw.textlength(' ', font=font)
    
    for word in words:
        color = highlight_color if word in important_words else text_color
        word_width = draw.textlength(word, font=font)
        draw.text((x, y), word, font=font, fill=color)
        x += word_width + space_width

    # Save the new image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage
image_path = "./input_image.jpg"
headline = "Ajit Doval reappointed as the National Security Adviser for the third term"
important_words = ["Ajit Doval", "reappointed", "National Security Adviser", "third term"]
output_path = "./output_image.jpg"

create_news_image(image_path, headline, important_words, output_path)
