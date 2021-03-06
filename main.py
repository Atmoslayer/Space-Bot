import argparse
import datetime
import os.path
import time
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import HTTPError


def determine_image_type(image_link):
    image_type = os.path.splitext(image_link)
    return image_type[1]


def save_image(url, filename, params=None):

    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(f'images/{filename}', 'ab') as picture:
        picture.write(response.content)


def fetch_spacex_last_launch():
    spasex_url = 'https://api.spacexdata.com/v3/launches/'
    response = requests.get(spasex_url)
    response.raise_for_status()
    content = response.json()
    image_links = None
    for flight in reversed(content):
        flight_links = flight['links']
        if flight_links['flickr_images']:
            image_links = flight_links.get("flickr_images", None)
            break

    if image_links:
        for image_link in image_links:
            image_type = determine_image_type(image_link)
            image_index = image_links.index(image_link)
            save_image(image_link, f'spacex{image_index}{image_type}')


def fetch_nasa_picture(token):

    number_of_images = 30
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params ={'count': number_of_images, 'api_key': token}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    content = response.json()

    for image_info in content:
        image_info = image_info
        image_link = image_info['url']
        image_type = determine_image_type(image_link)
        image_index = content.index(image_info)
        save_image(image_link, f'nasa{image_index}{image_type}')


def fetch_nasa_epic_picture(token):

    number_of_images = 10
    nasa_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': token}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    content = response.json()
    for image_number in range(number_of_images):
        image_info = content[image_number]
        image_name = image_info['image']
        image_full_date = image_info['date']
        image_full_date_decoded = datetime.datetime.fromisoformat(image_full_date)
        image_date = image_full_date_decoded.strftime('%Y/%m/%d')
        image_link = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png'
        image_index = image_number
        save_image(image_link, f'nasaEPIC{image_index}.png', params)


def send_pictures(path, bot_token, chat_id, sleep_time):

    gravity_guy_bot = telegram.Bot(token=bot_token)
    for roots, dir, files in os.walk(path):
        for picture in files:
            with open(f'{path}/{picture}', 'rb') as photo:
                gravity_guy_bot.send_photo(chat_id=chat_id, photo=photo)
            time.sleep(sleep_time)
    gravity_guy_bot.send_photo(chat_id=chat_id, photo=photo)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Enter path to save images', type=str)
    arguments = parser.parse_args()
    path = arguments.path
    Path(path).mkdir(parents=True, exist_ok=True)
    load_dotenv()

    nasa_token = os.getenv('NASA_TOKEN')
    bot_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    sleep_time = int(os.getenv('SLEEP_TIME'))

    try:
        fetch_spacex_last_launch()
        fetch_nasa_picture(nasa_token)
        fetch_nasa_epic_picture(nasa_token)
        # print(123)
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')

    send_pictures(path, bot_token, chat_id, sleep_time)