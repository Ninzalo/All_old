import config
import logging
import time
import requests
import os

from selenium.webdriver.common.keys import Keys
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver

# log level
logging.basicConfig(level=logging.INFO)
logging = logging.getLogger(__name__)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

if os.path.exists(f'{os.getcwd()}\\Music'):
	pass
else:
	os.mkdir(f'{os.getcwd()}\\Music')

music_path = f"{os.getcwd()}\\Music\\"


class TgBot():
	@dp.message_handler(commands=['start', "help"])
	async def filter_massages(message: types.Message):
		await message.answer('1) Введите автора и название трека (Пример: Post Malone motley crew)\n2) Ожидайте около минуты')
		print(f"сообщение {message.text} получено")


	@dp.message_handler()
	async def filter_massages(message: types.Message):
		name = message.text
		print("Пользователь ищет - " + name)

		options = webdriver.ChromeOptions()
		options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0")
		options.add_argument("--disable-blink-features=AutomationControlled")
		options.add_argument("--headless")
		driver = webdriver.Chrome(
			executable_path=f"{os.getcwd()}\\chromedriver\\chromedriver.exe",
			options=options
		)

		driver.get("https://downloadmusicvk.ru/")
		time.sleep(3)
		try:
			name_input = driver.find_element_by_xpath("/html/body/div[1]/nav/div/div[2]/form/div/div/span/input[2]")
			name_input.clear()
			name_input.send_keys(name, Keys.ENTER)
			time.sleep(2)
			driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div[3]/a[3]").click()
			time.sleep(2)
			# get current window handle
			p = driver.current_window_handle

			# get first child window
			chwd = driver.window_handles

			for w in chwd:
				# switch focus to child window
				if (w != p):
					driver.switch_to.window(w)

			audio_src = "/html/body/div[2]/div/a[1]"
			audio_src_url = driver.find_element_by_xpath(audio_src).get_attribute('href')

			get_audio = requests.get(audio_src_url, stream=True)
			with open(f"{music_path}{name}.mp3", "wb") as audio_file:
				for chunk in get_audio.iter_content(1024):
					if chunk:
						audio_file.write(chunk)

			await message.answer_document(open(f"{music_path}{name}.mp3", "rb"))
			print(f"Трек {name} отправлен")
			driver.close()
			driver.quit()
			os.remove(f"{music_path}{name}.mp3")
		except Exception as ex:
			await message.answer("Не получилось, попробуйте еще раз" + '\n' + "Возможно, неправильное название")
			print(ex)


	# run long-polling
	if __name__ == "__main__":
		executor.start_polling(dp, skip_updates=True)
