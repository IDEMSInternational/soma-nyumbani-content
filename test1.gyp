def headonly(cms):
    with open(cms.html, r) as f:
        html_string = f.read()
    print(html_string)

headonly(squares)
