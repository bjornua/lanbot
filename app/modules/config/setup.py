# -*- coding: utf-8 -*-
import os.path

def user_query(itemname, converter, default=None):
    while True:
        if default == None:
            answer = input("Indtast %s: " % (itemname,))
        else:
            answer = input("Indtast %s [%s]: " % (itemname, default))
            if answer == "":
                return default
        try:
            answer = converter(answer)
        except:
            print("Kunne ikke forstå værdien, prøv igen.")
            continue
        return answer

def prompt_update_config():
    try:
        from app.modules.config.generated import config
    except ImportError:
        from app.modules.config.default import config
        config = config()

    for name, key, converter in [
        ("CouchDB Server URL", "couchdb_server_url", str),
        ("CouchDB db", "couchdb_db", str),
    ]:
        config[key] = user_query(name, converter, config[key])
    return config

def write_config(config):
    filename = os.path.join(os.path.dirname(__file__), "generated.py")
    fhandle = open(filename, "w")
    fhandle.write(
        "# -*- coding: utf-8 -*-\n"
      + "from app.modules.config.default import config\n"
      + "config = config()\n"
      + "config.update(" + repr(config) + ")"
    )

