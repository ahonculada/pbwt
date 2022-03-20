import webbrowser

def main():
    with open('/tmp/sample.html', 'w') as sample:
        message = """
            <html>
            <head></head>
            <body><p>Hello Girl!</p></body>
            </html>
        """
        sample.write(message)
    filename = 'file:///tmp/sample.html'
    webbrowser.open_new_tab(filename)

if __name__ == '__main__':
    main()
