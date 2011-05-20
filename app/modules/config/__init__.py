# -*- coding: utf-8 -*-
import sys
from app.modules.config.setup import write_config, prompt_update_config


argv = sys.argv[1:]

setup = False

if "setup" in argv[0:1]:
    setup = True
else:
    try:
        import app.modules.config.generated
    except ImportError:
        setup = True
    
if setup:
    write_config(prompt_update_config())
    import  app.modules.config.generated
print dir (app.modules)
