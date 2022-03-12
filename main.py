from pathlib import Path
import requests
import json
from requests.exceptions import HTTPError

def save_image(url, filename, path):

    response = requests.get(url)
    response.raise_for_status()
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(f'images/{filename}', 'ab') as picture:
        picture.write(response.content)

def fetch_spacex_last_launch(path):
    launch_year = 0
    url = 'https://api.spacexdata.com/v3/launches/'
    response = requests.get(url)
    response.raise_for_status()
    content_list = list(response.json())
    for flights_quantity in range(len(content_list)):
        latest_flight = content_list[-flights_quantity]
        flight_links = latest_flight['links']
        if flight_links['flickr_images']:
            image_links = flight_links['flickr_images']
            break

    for image_link in image_links:
        save_image(image_link, f'flight_picture{image_links.index(image_link)}.jpeg', path)

if __name__ == '__main__':

    filename = 'hubble.jpeg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    path = 'C:/Users/admin/Documents/GitHub/Space-Bot/images'
    fetch_spacex_last_launch(path)

    try:
        save_image(url, filename, path)

    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
