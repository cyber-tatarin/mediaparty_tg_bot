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


def add_name_to_message(message, name):
    # Extract the last number from the string
    print(message)
    numbers = re.findall(r'\n(\d+)\.', message)
    print(numbers)
    if numbers:
        last_number = numbers[-1]
        
        # Increment the last number and add the next name
        next_number = int(last_number) + 1
        
        # Append the new number and name to the string
        new_string = message + f"\n{next_number}. {name}"
    
    else:
        new_string = message + f"\n\nУже помогли:\n1. {name}"
        
    return new_string


def replace_numbers(match, number_to_delete):
    number = int(match.group(1))
    if number > number_to_delete:
        number -= 1
    return f"\n{number}."


def remove_name_from_message(message, name):
    # Find the row with the specified name
    name_pattern = fr"\n(\d+)\.\s{re.escape(name)}(?!\w)"
    matches = re.findall(name_pattern, message)
    
    if matches:
        # Remove the row with the specified name
        number_to_delete = int(matches[0])
        new_string = re.sub(name_pattern, "", message)
        
        # Update the numbers of the remaining rows
        number_pattern = r"\n(\d+)\."
        
        new_string = re.sub(number_pattern, lambda match: replace_numbers(match, number_to_delete), new_string)
        
        number_pattern_for_find = r"1\."
        
        has_people = re.findall(number_pattern_for_find, new_string)
        print(has_people, 'has people')
        
        if not has_people:
            print('inside')
            new_string = new_string.replace('Уже помогли:', '')
        
        return new_string
    else:
        return message
        
        
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


if __name__ == '__main__':
    # print(add_name_to_message('1. Антон', 'Дима'))
    print(remove_name_from_message('1. Антон\n2. Дима', 'Дима'))
    