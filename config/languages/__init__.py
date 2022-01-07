import os, json

def generate():
  files = os.listdir("./config/languages/")
  language_files = ["/config/languages/"+file for file in files if file.endswith(".json")]
  def _gen(fmt):
    class _:
      def __repr__(self): return "lang"
      def __init__(self):
        for k,v in fmt.items():
          if isinstance(v, dict): v = _gen(v)
          setattr(self, k, v)

    return _()

  languages = {}
  for file in language_files:
    languages[file.split("/")[-1][:-5]] = _gen(json.load(open(file,"r")))
  print(languages)
  globals().update(languages)

generate()
del generate()

def get(lang: str):
  return globals().get(lang)
