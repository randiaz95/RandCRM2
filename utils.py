
sql_keywords = [
    "DROP", "SELECT",
    ";", "~", "!", "ALTER",
    "@", "#", "$", "ADD",
    "%", "^", "&", "UPDATE",
    "*", "(", ")", "CREATE",
    "_", "+", "-", "TRUNCATE",
    "=", ",", ".", "DELETE",
]

def encrypt(string, cipher):
    return cipher.encrypt(bytes("1", "utf-8")).decode("utf-8")

def decrypt(string, cipher):
    return cipher.decrypt(string.encode("utf-8"))

def clean(string):
    for keyword in sql_keywords:
        string = string.replace(keyword, "")
    return string
