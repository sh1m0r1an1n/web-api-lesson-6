import random
import requests
import telegram
from environs import Env, EnvError
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
    response = requests.get(url='https://xkcd.com/info.0.json', timeout=10)
    response.raise_for_status()
    return response.json()['num']


def main():
    """Основная логика работы скрипта"""
    env = Env()
    first_comic_number = 1

    try:
        env.read_env()
        bot_token = env.str("TG_BOT_TOKEN")
        channel_id = env.str("TG_CHANNEL_ID")
    except FileNotFoundError:
        print("🚨 Ошибка: файл .env не найден")
        return
    except EnvError as e:
        print(f"🚨 Ошибка конфигурации: {str(e)}")
        print("🔧 Проверьте переменные TG_BOT_TOKEN и TG_CHANNEL_ID в .env")
        return

    try:
        bot = telegram.Bot(bot_token)
        latest_comic_number = get_latest_comic_number()
        comic_number = random.randint(first_comic_number, latest_comic_number)
        comic_data = download_xkcd_comic(comic_number)
        send_comic_to_telegram(bot, channel_id, comic_data)
        print("✅ Комикс успешно опубликован!")
    except (RequestException, TelegramError) as e:
        print(f"🚨 Ошибка сети или API: {str(e)}")
        print("🔧 Проверьте подключение и настройки бота")
    except KeyError as e:
        print(f"🔍 Ошибка данных: отсутствует ключ {str(e)}")
        print("🔄 Попробуйте снова или обновите скрипт")


if __name__ == "__main__":
    main()