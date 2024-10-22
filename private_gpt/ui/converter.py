import base64

# Load your PNG image
with open("png.png", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read()).decode('utf-8')

# Print or save the Base64 string
print(f"data:image/png;base64,{b64_string}")
