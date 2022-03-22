import argparse
import datetime
import os.path
import time
import urllib.parse
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import HTTPError


def determine_image_type(image_link):
    image_type = os.path.splitext(image_link)
    return image_type[1]


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
    content = list(response.json())
    for flight in content:
        latest_flight = content[-content.index(flight)]
        flight_links = latest_flight['links']
        if flight_links['flickr_images']:
            image_links = flight_links['flickr_images']
            break

    if image_links:
        for image_link in image_links:
            image_type = determine_image_type(image_link)
            image_index = image_links.index(image_link)
            save_image(image_link, f'spacex{image_index}{image_type}', path)


def fetch_nasa_picture(path, token):

    number_of_images = 30
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params ={'count': number_of_images, 'api_key': token}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    content = list(response.json())

    for image_info in content:
        image_info = dict(image_info)
        image_link = image_info['url']
        image_type = determine_image_type(image_link)
        image_index = content.index(image_info)
        save_image(image_link, f'nasa{image_index}{image_type}', path)


def fetch_nasa_epic_picture(path, token):

    number_of_images = 10
    nasa_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': token}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    content = list(response.json())
    for image_number in range(number_of_images):
        image_info = dict(content[image_number])
        image_name = image_info['image']
        image_full_date = image_info['date']
        image_full_date_decoded = datetime.datetime.fromisoformat(image_full_date)
        image_date = str(image_full_date_decoded.strftime('%Y/%m/%d'))
        params_decoded = urllib.parse.urlencode(params)
        image_link = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?{params_decoded}'
        image_index = image_number
        save_image(image_link, f'nasaEPIC{image_index}.png', path)


def sending_pictures(path, bot_token, chat_id, sleep_time):

        gravity_guy_bot = telegram.Bot(token=bot_token)
        for roots, dir, files in os.walk(path):
            for picture in files:
                gravity_guy_bot.send_photo(chat_id=chat_id, photo=open(f'{path}/{picture}', 'rb'))
                time.sleep(sleep_time)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Enter path to save images', type=str)
    arguments = parser.parse_args()
    path = arguments.path
    load_dotenv()

    nasa_token = os.getenv('NASA_TOKEN')
    bot_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    sleep_time = int(os.getenv('SLEEP_TIME'))

    try:
        fetch_spacex_last_launch(path)
        fetch_nasa_picture(path, nasa_token)
        fetch_nasa_epic_picture(path, nasa_token)
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')

    sending_pictures(path, bot_token, chat_id, sleep_time)