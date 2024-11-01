from PIL import Image, ImageDraw, ImageFont, ImageOps

def create_news_image(image_path, headline, important_words, output_path, resolution, logo_path=None):
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
    gradient_height = total_text_height + 5 * margin
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
        space_width = draw.textlength(' ', font=font) + 10  # Adjusted word spacing
        
        for word in words:
            color = highlight_color if word in important_words else text_color
            word_width = draw.textlength(word, font=font)
            draw.text((x, y), word, font=font, fill=color)
            x += word_width + space_width
        y += 10 + draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]

    # Add logo if provided
    if logo_path:
        logo = Image.open(logo_path).convert('RGBA')
        logo_height = image_height // 10
        logo_width = int(logo_height * logo.width / logo.height)
        logo = logo.resize((logo_width, logo_height))

        # Ensure logo background is transparent
        logo = logo.convert('RGBA')
        logo_data = logo.getdata()
        new_data = []
        for item in logo_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        logo.putdata(new_data)

        image.paste(logo, (10, 10), logo)

    # Add line separator below headline
    separator_y = text_position_y + total_text_height + margin // 2
    draw.line([(text_position_x, separator_y), (image_width - text_position_x, separator_y)], fill=(255, 255, 255), width=2)

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

# Example logo path (replace with your actual logo path)
logo_path = "./news_logo.png"

create_news_image(image_path, headline, important_words, output_path, resolutions[post_type], logo_path)
