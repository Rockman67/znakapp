import base64

def xor_encrypt_decrypt(username, key, min_length=6, pad_char='#'):
    # Определяем, является ли операция шифрованием или расшифровкой
    is_encrypting = not username.startswith(pad_char * min_length)

    # Добавляем padding при шифровании
    if is_encrypting and len(username) < min_length:
        username += pad_char * (min_length - len(username))

    # Если это операция расшифровки, то сначала декодируем из Base64
    if not is_encrypting:
        username = base64.b64decode(username).decode()

    # Выполняем XOR шифрование/расшифровку
    encrypted_decrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(username))

    # Кодируем результат в Base64 при шифровании
    if is_encrypting:
        encrypted_decrypted = base64.b64encode(encrypted_decrypted.encode()).decode()

    # Удаляем padding при расшифровке
    if not is_encrypting:
        encrypted_decrypted = encrypted_decrypted.rstrip(pad_char)

    return encrypted_decrypted
