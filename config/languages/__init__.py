import os, json


def generate():
  files = os.listdir("./config/languages/")
  language_files = ["config/languages/"+file for file in files if file.endswith(".json")]
  def _gen(k,fmt):
    class _:
      def __repr__(self): return k
      def __str__(self): return k
      def __init__(self):
        self.__name__ = k.split(".")[-1]
        for key,v in fmt.items():
          if isinstance(v, dict): v = _gen(k+"."+key,v)
          setattr(self, key, v)

    return _()

  languages = {}
  for file in language_files:
    lname = file.split("/")[-1][:-5]
    languages[lname] = _gen(lname, json.load(open(file,"r")))

  languages["languages"] = languages.copy()
  globals().update(languages)

generate()
del generate

def get(lang: str):
  return globals().get(lang)

def all(direct: bool = False):
  return list(
    languages.values()
  ) if direct else list(
    languages.keys()
  )
