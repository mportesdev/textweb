# coding: utf-8

import bottle

content = """
<!DOCTYPE html>
<html>
<head lang="cs">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Roští.cz</title>
</head>
<body>
        <p>
Nyní můžete obsah adresáře <code>/srv/app</code> vymazat a nahradit ho svoji aplikací. K aplikaci také nezapomeňte nahrát soubor app.py (místo tohoto) a vložit do něj volání své aplikace pro webový server gunicorn.
        </p>
        <p>
Nejčastěji naši uživatelé používají Django. V takovém případě vypadá soubor <code>app.py</code> takto:
        </p>
        <pre>
import os

# Pokud se settings nachází v /srv/app/moje_aplikace,
# bude obsah pro DJANGO_SETTINGS_MODULE: moje_aplikace.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moje_aplikace.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
        </pre>
        <p>
Pravděpodobně nemáte svou aplikaci bez závislostí, takže během příprav spuštění vaší aplikace nezapomeňte nahrát soubor requirements.txt do adresáře <code>/srv/app/</code>. Po restartu kontejneru proběhne instalace závislostí automaticky.
        </p>
        <p>
Do souboru <code>/srv/app/init.sh</code> můžete napsat příkazy, které se mají spustit po každém restart kontejneru. Můžete si tak usnadnit třeba deployment.
        </p>
</body>
</html>
"""

@bottle.route('/')
def home():
    return content

application = bottle.default_app()
