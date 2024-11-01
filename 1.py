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

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), headline, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = image.size

    # Add margin around the heading
    margin = 20
    text_position = (10 + margin, image_height - text_height - 10 - margin)

    # Create a gradient background
    gradient_height = text_height + 2 * margin
    gradient = Image.new('RGBA', (image_width, gradient_height), (0, 0, 0, 0))
    for y in range(gradient_height):
        opacity = int(150 * (y / gradient_height))  # Decreased opacity
        draw_gradient = ImageDraw.Draw(gradient)
        draw_gradient.line([(0, y), (image_width, y)], fill=(0, 0, 0, opacity))

    # Paste the gradient onto the original image
    image.paste(gradient, (0, image_height - gradient_height - 10), gradient)

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



# 2
from PIL import Image, ImageDraw, ImageFont, ImageOps

def create_news_image(image_path, headline, important_words, output_path, resolution):
    # Load the image and resize if necessary
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)  # Correct orientation if needed
    image = image.resize(resolution)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Define the font properties based on resolution
    base_font_size = min(image_width, image_height) // 20
    font_path = "./Arial.ttf"  # Provide the path to a font file
    font = ImageFont.truetype(font_path, base_font_size)

    # Define text color and highlight color
    text_color = (255, 255, 255)  # White color
    highlight_color = (255, 255, 0)  # Yellow color for highlights

    # Calculate maximum text width and manage word wrapping
    max_text_width = image_width - 2 * (image_width // 10)
    lines = []
    line = []
    words = headline.split()
    
    for word in words:
        if line:
            line.append(' ')
        line.append(word)
        if draw.textlength(' '.join(line), font=font) > max_text_width:
            lines.append(' '.join(line[:-1]))
            line = [word]
    
    if line:
        lines.append(' '.join(line))

    # Calculate total text height needed
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)

    # Add margin around the heading
    margin = image_height // 10
    text_position_y = image_height - total_text_height - margin
    text_position_x = image_width // 15

    # Create a gradient background adjusted to text height
    gradient_height = total_text_height + 5* margin            #hight of gradient
    gradient = Image.new('RGBA', (image_width, gradient_height), (0, 0, 0, 0))
    for y in range(gradient_height):
        opacity = int(255 * (y / gradient_height))  # Adjust opacity
        draw_gradient = ImageDraw.Draw(gradient)
        draw_gradient.line([(0, y), (image_width, y)], fill=(0, 0, 0, opacity))

    # Paste the gradient onto the original image
    image.paste(gradient, (0, image_height - gradient_height), gradient)

    # Draw the text with highlighting
    y = text_position_y
    for line in lines:
        x = text_position_x
        words = line.split()
        space_width = draw.textlength(' ', font=font)+10  # word spacing 
        for word in words:
            color = highlight_color if word in important_words else text_color
            word_width = draw.textlength(word, font=font)
            draw.text((x, y), word, font=font, fill=color)
            x += word_width + space_width
        y += 10+ draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]

    # Save the new image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage
image_path = "./input_image.jpg"
headline = "Ajit Doval reappointed as the National Security Adviser for the third term"
important_words = ["Ajit Doval", "reappointed", "National Security Adviser", "third term"]

# Define resolutions for different post types
resolutions = {
    "Square": (1080, 1080),
    "Landscape": (1080, 566),
    "Portrait": (1080, 1350),
    "Instagram Stories": (1080, 1920),
    "Reels": (1080, 1920),
    "Profile Picture": (320, 320)
}

# Specify the type of post
post_type = "Square"
output_path = f"./output_image_{post_type.lower().replace(' ', '_')}.jpg"

create_news_image(image_path, headline, important_words, output_path, resolutions[post_type])
