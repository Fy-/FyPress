import string, random, re
from unidecode import unidecode

def slugify(text, delim=u'-'):
  _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

  """Generates an ASCII-only slug."""
  result = []
  for word in _punct_re.split(text.lower()):
      result.extend(unidecode(word).split())
  return unicode(delim.join(result))

def url_unique(url, Obj, ignore=False, sep='-'):
  exist = Obj.query.exist('guid', url, ignore)
  if not exist:
    return url

  i = 1
  last = 0

  while Obj.query.exist('guid', url, ignore):
    add  = '{}{}'.format(sep, i)
    if last:
      url = url[:last]+add
    else:
      url = url+add
      
    last = -1*len(add)
    i += 1 

  return url