from .settings import settings

html = f"""
<html>
<head>
  <meta charset="utf-8"> <!-- Important: rapi-doc uses utf8 charecters -->
  <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
</head>
<body>
  <rapi-doc
    spec-url="{settings.OPENAPI_URL}"></rapi-doc>
</body>
</html>
"""
