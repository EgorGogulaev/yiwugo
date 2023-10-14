import g4f
import json


class TurboGPT:
    """ Класс представляющий собой чат GPT 3.5 turbo """

    def __init__(self):
        """ Инициализатор класса """
        self.__model: str = 'gpt-3.5-turbo'
        self.text_answer = ""

    def send_request(self, prompt: str, role: str = 'user'):
        """
        Посылает запрос провайдеру (источнику халявного gpt).

        role: по умолчанию user
        content: представляет собой текст запроса

        Рабочие провайдеры:
        - Aichat (ограниченное количество запросов)
        - Ails (Читает хорошо, обязательно уточнять про то что ответ должен быть на русском, стрим)
        """
        response = g4f.ChatCompletion.create(
            model=self.__model,
            provider=g4f.Provider.Ails,
            messages=[{'role': role, 'content': prompt}],
            stream=True
        )
        for message in response:
            self.text_answer += message
    
    def processing_gpt_answer(self) -> dict:
        self.text_answer = self.text_answer.replace('\n', '')
        dict_info = json.loads(self.text_answer)
        return dict_info




if __name__ == '__main__':

    # Запускать этот файл при тестах, не запускать при релизе. Читает первую статью в журнале и посылет запрос в gpt

    import PyPDF2
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    with open(BASE_DIR + f'/data/test.pdf', 'rb') as file:

        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[26]
        content = page.extract_text()

        # with open(BASE_DIR + f'/data/text.txt', 'w') as text:
        #     text.write(content)

        prompt_text = """Я даю тебе текст научной статьи. Мне нужно из данного текста извлечь: 1) Название статьи; 2) Аннотацию статьи;
        3) Ключевые слова статьи; 4) Авторов статьи, перечисленных через запятую, если авторов несколько 5) Универистет работы авторов 
        также через запятую, если авторов больше одного 6) email автора 7) Идентификатор doi; 8) УДК статьи. Всю инфрмацию представь в виде словаря {} - python, 
        где извлеченный текст - это значения, а ключи название того, что ищем. Очень важно: не меняй оргинальный текст, сохраняй текст такой
        какой я даю тебе его. В ответе предоставь мне только словарь, не нужно писать ничего от себя. Результат в виде строки, в которой лежит словарь. 
        """
        gpt = TurboGPT()
        gpt.send_request(prompt=f"{prompt_text} Текст для поиска следующий: {content}")
        gpt.processing_gpt_answer()
