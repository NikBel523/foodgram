import io


def generate_shopping_cart_txt(ingredients):
    """Функция для генерации txt файла со списком покупок."""

    buffer = io.StringIO()

    buffer.write('Список покупок\n')
    buffer.write('=====================\n')

    for name, details in ingredients.items():
        text = f"{name}: {details['amount']} {details['measurement_unit']}\n"
        buffer.write(text)

    buffer.seek(0)
    return buffer.getvalue()
