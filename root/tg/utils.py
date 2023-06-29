import re


def check_message_for_buzz_words(message: str):
    patterns = create_patterns(['сметана'])
    
    # Combine the patterns into a single regular expression
    regex = re.compile('|'.join(patterns), re.IGNORECASE)
    
    # Find matches in the text
    matches = re.findall(regex, message)
    
    return matches  


def create_patterns(words: list[str]):
    res = []
    for word in words:
        for letter in word:
            res.append(r'\b' + word.replace(letter, '.', 1) + r'\b')
        res.append(r'\b' + word[:-1] + '.' + r'\b')
        res.append(r'\b' + word + '.' + r'\b')
        res.append(r'\b' + '.' + word + r'\b')
    print(set(res))
    return list(set(res))


# create_patterns(['сметана'])

print(check_message_for_buzz_words('см*тана Смметана Пароль сметана*'))
