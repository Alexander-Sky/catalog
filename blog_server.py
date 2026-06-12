from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 8080


class BlogHandler(BaseHTTPRequestHandler):

    def _read_html(self, filename):
        """Читает HTML-файл из папки templates"""
        try:
            with open(f"templates/{filename}", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index":
            content = self._read_html("index.html")
        elif parsed.path == "/contacts":
            content = self._read_html("contacts.html")
        elif parsed.path == "/about":
            content = self._read_html("about.html")
        else:
            content = self._read_html("404.html")
            if content is None:
                content = "<h1>404 - Страница не найдена</h1>"

        if content is None:
            content = "<h1>500 - Внутренняя ошибка сервера</h1>"
            self.send_response(500)
        else:
            self.send_response(200)

        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_POST(self):
        """Обрабатывает отправку формы на странице Контакты"""
        if self.path == "/contacts":
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode('utf-8')
            params = parse_qs(data)

            print("\n" + "=" * 50)
            print("📬 Получено новое сообщение:")
            print(f"  Имя:      {params.get('name', [''])[0]}")
            print(f"  Email:    {params.get('email', [''])[0]}")
            print(f"  Сообщение: {params.get('message', [''])[0]}")
            print("=" * 50 + "\n")

            # Ответ после отправки формы
            response = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Сообщение отправлено</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="container mt-5">
                <div class="alert alert-success">
                    <h4>Спасибо за ваше сообщение!</h4>
                    <p>Мы ответим вам в ближайшее время.</p>
                    <a href="/" class="btn btn-primary">Вернуться на главную</a>
                </div>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run():
    server = HTTPServer((HOST, PORT), BlogHandler)
    print(f"✅ Сервер запущен: http://{HOST}:{PORT}")
    print("Нажми Ctrl+C для остановки")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
        server.server_close()


if __name__ == "__main__":
    run()