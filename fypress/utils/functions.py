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

from urlparse import urlparse, urljoin
from flask import request, url_for

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
  for target in request.values.get('next'), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return target