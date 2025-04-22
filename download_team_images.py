import urllib.request
import os

# Create the static/images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# URLs for team member images (using randomuser.me)
image_urls = [
    ('https://randomuser.me/api/portraits/men/1.jpg', 'static/images/team1.jpg'),
    ('https://randomuser.me/api/portraits/women/1.jpg', 'static/images/team2.jpg'),
    ('https://randomuser.me/api/portraits/men/2.jpg', 'static/images/team3.jpg'),
    ('https://randomuser.me/api/portraits/women/2.jpg', 'static/images/team4.jpg'),
]

# Download each image
for url, filename in image_urls:
    try:
        print(f"Downloading {url} to {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

print("Download completed!") 