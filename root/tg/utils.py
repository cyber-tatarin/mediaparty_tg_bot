import re

pattern = "подпишитесь|лайкните|поставьте лайк|ищу|оставите реакцию|помогите|нужна помощь|инстаграм|в профиле|" \
          "instagram|подписывайтесь|прайс|подпиской|комментариями|комментарий|лайки|в директ|\.by|https|http|\.ru|" \
          "мастер-класс|практики|для записи|цена"


def check_message_for_buzz_words(message: str):
    
    # # Combine the patterns into a single regular expression
    # regex = re.compile('|'.join(patterns), re.IGNORECASE)
    
    # Find matches in the text
    matches = re.findall(pattern, message.lower())
    
    return matches


# def create_patterns(words: list[str]):
#     res = []
#     for word in words:
#         for letter in word:
#             res.append(r'\b' + word.replace(letter, '.', 1) + r'\b')
#         res.append(r'\b' + word[:-1] + '.' + r'\b')
#         res.append(r'\b' + word + '.' + r'\b')
#         res.append(r'\b' + '.' + word + r'\b')
#     print(set(res))
#     return list(set(res))


# create_patterns(['сметана'])

# print(check_message_for_buzz_words('см*тана Смметана Пароль сметана*'))
# print(check_message_for_buzz_words("""14 июня, сегодня, 19. 00
# На сцене Молодёжного театра эстрады.
# Билеты в кассе театра и на kvitki.by"""))
