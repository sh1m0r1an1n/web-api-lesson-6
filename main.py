import random
import requests
import telegram
from environs import Env
from requests.exceptions import RequestException
from telegram.error import TelegramError


def download_xkcd_comic(comic_number):
    """Загружает данные комикса с xkcd.com"""
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def send_comic_to_telegram(bot, channel_id, comic_data):
    """Отправляет комикс в Telegram-канал"""
    image_response = requests.get(comic_data['img'], timeout=10)
    image_response.raise_for_status()

    bot.send_photo(
        chat_id=channel_id,
        photo=image_response.content,
        caption=f"🎨 {comic_data['alt']}"
    )


def get_latest_comic_number():
    """Получает номер последнего комикса"""
    response = requests.get('https://xkcd.com/info.0.json', timeout=10)
    return response.json()['num']


def main():
    """Основная логика работы скрипта"""
    try:
        env = Env()
        env.read_env()

        bot = telegram.Bot(token=env.str("TG_BOT_TOKEN"))
        channel_id = env.str("TG_CHANNEL_ID")

        first_comic_number = 1
        latest = get_latest_comic_number()
        comic_number = random.randint(first_comic_number, latest)
        comic_data = download_xkcd_comic(comic_number)
        send_comic_to_telegram(bot, channel_id, comic_data)

        print("✅ Комикс успешно опубликован!")

    except (RequestException, TelegramError) as e:
        print(f"🚨 Ошибка сети или API: {str(e)}")
        print("🔧 Проверьте подключение к интернету и настройки бота")
    except KeyError as e:
        print(f"🔍 Ошибка в структуре данных: отсутствует ключ {str(e)}")
        print("🔄 Попробуйте запустить скрипт снова")


if __name__ == "__main__":
    main()