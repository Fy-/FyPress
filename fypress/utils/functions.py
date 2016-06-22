from flask import g
from unidecode import unidecode
import string, random, re, os
from werkzeug.utils import secure_filename


def get_template(key, config):
    key  = os.path.normpath(key)
    path = os.path.join('themes', g.options['theme'], key)
    path_child = os.path.join('themes', '_current', key)
    if os.path.isfile(os.path.join(config.TEMPLATE_FOLDER, path_child)):
      return path_child
    return path

def get_template_static(key, file, config):
    key  = os.path.normpath(key)
    file = secure_filename(file)
    path = get_template(os.path.join('public',key), config)
    return [os.path.join(config.TEMPLATE_FOLDER, path), file]

def slugify(text, delim=u'-'):
  _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

  """Generates an ASCII-only slug."""
  result = []
  for word in _punct_re.split(text.lower()):
      result.extend(unidecode(word).split())
  return unicode(delim.join(result))

def url_unique(url, Obj, ignore=False, sep='-'):
  exist = Obj.filter(Obj.guid==url)
  if ignore:
    exist.where(Obj.id!=ignore)

  if not exist:
    return url

  i = 1
  last = 0

  while exist.one():
    add  = '{}{}'.format(sep, i)
    if last:
      url = url[:last]+add
    else:
      url = url+add
      
    last = -1*len(add)
    i += 1 

    exist = Obj.filter(Obj.guid==url)
    if ignore:
      exist.where(Obj.id!=ignore)
      
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