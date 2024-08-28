from flask import Flask, request, Response
import barcode
from barcode.writer import SVGWriter
from io import BytesIO

app = Flask(__name__)

@app.route('/barcode')
def generate_barcode():
    data = request.args.get('data')
    if not data or len(data) != 12 or not data.isdigit():
        return "Error: Please provide a valid 12-digit EAN-13 data.", 400

    try:
        # Настройки для SVGWriter
        options = {
            'module_width': 1.4,      # Ширина одной полосы штрих-кода
            'module_height': 40,      # Высота полосы штрих-кода (настраивается в соответствии с SVG)
            'quiet_zone': 0,          # Размер внешнего поля
            'font_size': 1,           # Минимальный размер шрифта (1 - почти невидимый)
            'text_distance': 0,       # Расстояние между штрих-кодом и подписью (здесь не используется)
            'write_text': False       # Не писать текстовые подписи
        }

        # Генерация штрих-кода EAN-13 в формате SVG
        ean = barcode.get('ean13', data, writer=SVGWriter())
        buffer = BytesIO()
        ean.write(buffer, options)

        # Получение SVG содержимого
        svg_output = buffer.getvalue().decode('utf-8')

        # Настройка размера SVG
        svg_output = svg_output.replace('width="100%"', 'width="540"')
        svg_output = svg_output.replace('height="100%"', 'height="155"')

        # Отправка SVG как ответа
        return Response(svg_output, mimetype='image/svg+xml')

    except ValueError as e:
        return f"Error generating barcode: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
