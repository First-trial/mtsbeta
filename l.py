def b(f):
  f.__doc__=getattr(globals().get("g"), "p").__doc__
