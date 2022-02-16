from flask import Flask as Site
from threading import Thread as BackgroundRunner


site = Site(__name__)

@site.route("/")
def index():
  return "Mts Bot is Hosted!"

def host_site():
  site.run("0.0.0.0", 8080, debug=True)

def host_on_replit(obj, func_name, extra_works: list = None, *args, **kwargs):
  for work in extra_works:
    w = work["work"]+"(" + ", ".join(work["args"])
    if work["args"] and work["kwargs"]:
      w += ", "
    for kn, kv in work["kwargs"].items():
      w = w + kn + "=" + eval(kv) + ", "
      
    w += ")"
    eval(w)

  BackgroundRunner(target=host_site).start()
  run = getattr(obj, func_name)
  run(*args, **kwargs)

def host(bot, token):
  ew = [
    {
      "work": "setattr",
      "args": ["site", "\"bot\"", "obj"],
      "kwargs": {}
    }
  ]
  host_on_replit(bot, "run", ew, token)
