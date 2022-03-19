import argparse
import datetime
import json
import os.path
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError


def determine_image_type(image_link):
    image_type = os.path.splitext(image_link)
    image_name = os.path.basename(image_type[0])
    return image_name, image_type[1]


def save_image(url, filename, path):

    response = requests.get(url)
    response.raise_for_status()
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(f'images/{filename}', 'ab') as picture:
        picture.write(response.content)


def fetch_spacex_last_launch(path):
    spasex_url = 'https://api.spacexdata.com/v3/launches/'
    response = requests.get(spasex_url)
    response.raise_for_status()
    content_list = list(response.json())
    for flights_quantity in range(len(content_list)):
        latest_flight = content_list[-flights_quantity]
        flight_links = latest_flight['links']
        if flight_links['flickr_images']:
            image_links = flight_links['flickr_images']
            break

    for image_link in image_links:
        image_name, image_type = determine_image_type(image_link)
        save_image(image_link, f'{image_name}{image_type}', path)


def fetch_nasa_picture(path, token):

    number_of_images = 30
    nasa_url = f'https://api.nasa.gov/planetary/apod?count={number_of_images}&api_key={token}'
    response = requests.get(nasa_url)
    response.raise_for_status()
    data_list = list(response.json())

    for data in data_list:
        data_dict = dict(data)
        image_link = data_dict['url']
        image_name, image_type = determine_image_type(image_link)
        save_image(image_link, f'{image_name}{image_type}', path)


def fetch_nasa_epic_picture(path, token):

    number_of_images = 10
    nasa_url = f'https://api.nasa.gov/EPIC/api/natural/images?count={number_of_images}&api_key={token}'
    response = requests.get(nasa_url)
    response.raise_for_status()
    data_list = list(response.json())

    for data in data_list:
        data_dict = dict(data)
        image_name = data_dict['image']
        image_full_date = data_dict['date']
        image_full_date_decoded = datetime.datetime.fromisoformat(image_full_date)
        image_date = str(image_full_date_decoded.strftime('%Y/%m/%d'))
        image_link = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?api_key={token}'
        save_image(image_link, f'{image_name}.png', path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Enter path to save images', type=str)
    arguments = parser.parse_args()
    path =arguments.path
    load_dotenv()
    token = os.getenv('NASA_TOKEN')
    filename = 'hubble.jpeg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    try:
        fetch_spacex_last_launch(path)
        fetch_nasa_picture(path, token)
        fetch_nasa_epic_picture(path, token)
        save_image(url, filename, path)
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
