# -*- coding: UTF-8 -*-
from werkzeug import secure_filename
from flask import flash, jsonify
import datetime, magic, os, hashlib, json
from fypress.utils import FyImage, FyOembed, slugify, url_unique
from fypress.admin.static import messages
from fypress.local import _fypress_
from fypress.models import FyPressTables
from fysql import CharColumn, DateTimeColumn, IntegerColumn, TextColumn, DictColumn

import urllib2, shutil

config  = _fypress_.config

class Media(FyPressTables):
    # todo allowed {type, icon, }
    allowed_upload_types  = ('image/jpeg', 'image/png', 'image/gif')
    upload_types_images   = ('image/jpeg', 'image/png')

    uid             = CharColumn(unique=True, index=True, max_length=150)
    modified        = DateTimeColumn(default=datetime.datetime.now)
    type            = CharColumn(index=True, max_length=150)
    guid            = CharColumn(unique=True, index=True, max_length=255)
    name            = CharColumn(max_length=150)
    data            = DictColumn()
    icon            = CharColumn(max_length=75)
    html            = TextColumn()

    def generate_html(self):
        pass

    def urlify(self, image=False):
        if image:
            try:
                return config.UPLOAD_DIRECTORY_URL + self.data['var'][image]['guid']
            except:
                return ''
        else:
            return config.UPLOAD_DIRECTORY_URL + self.guid

    @staticmethod
    def add_from_web(url):
        oembed_ = FyOembed().get(url) 
        return jsonify(result=oembed_)

    @staticmethod
    def add_oembed(attrs):
        data = json.loads(attrs['data'])
        data['oembed'] =  json.loads(data['oembed'])
        
        now = datetime.datetime.now()
        media_hash          = Media.hash_string(data['url'])

        if Media.get(Media.uid==media_hash):
            media = Media.get(Media.uid==media_hash)
            media.modified = datetime.datetime.now()
            media.save()
            return jsonify(success=True), 200
        
        media = Media.create()
        media.uid           = media_hash
        media.type          = 'oembed'
        media.name          = data['title']
        media.guid          = "{}/{}/".format(now.year, now.month)+media_hash
        media.source        = data['url']
        media.icon          = data['fa']
        media.html          = data['html']
        media.data          = {}

        media.data['provider_url'] = data['oembed']['provider_url'].encode('utf8')
        media.data['provider']     = data['oembed']['service']
        if data['oembed'].has_key('author_name'):
            media.data['author_name']  = data['oembed']['author_name']
            media.data['author_url']   = data['oembed']['author_url']
        else:
            media.data['author_name']  = ''
            media.data['author_url']   = ''

        media.save()

        if data['oembed'].has_key('thumbnail_url'):
            response = urllib2.urlopen(data['oembed']['thumbnail_url'])
            Media.upload_save(response, os.path.join(Media.upload_path(config.CHUNKS_DIRECTORY), media_hash))

            mime = magic.Magic(mime=True)
            mime_file = mime.from_file(os.path.join(Media.upload_path(config.CHUNKS_DIRECTORY), media_hash))
            mimes = {'image/jpeg': 'jpg', 'image/jpg': 'jpg', 'image/png':'png'}

            ext         = '.'+mimes[mime_file]
            filename    = 'oembed-'+media_hash+ext
            fdir        = Media.upload_path(config.UPLOAD_DIRECTORY)
            fpath       = os.path.join(fdir, filename)

            shutil.move(os.path.join(Media.upload_path(config.CHUNKS_DIRECTORY), media_hash), fpath)

            images      = FyImage(fpath).generate()
            sizes = {}
            for image in images:
                sizes[image[3]] = {'name': image[1], 'source': os.path.join(Media.upload_path(config.UPLOAD_DIRECTORY), image[0]), 'guid': "{}/{}/".format(now.year, now.month)+image[2]}

            media.data['var'] = sizes
            media.save()

        flash(messages['added']+' ('+str(media)+')')

        return jsonify(success=True), 200

    @staticmethod
    def upload_path(config):
        now = datetime.datetime.now()
        tmp = "{}/{}".format(now.year, now.month)
        if 'chunks' in config:
            return os.path.join(config)
        return os.path.join(config, tmp)

    @staticmethod
    def upload_save(f, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, 'wb+') as destination:
            destination.write(f.read())

    @staticmethod
    def upload_combine_chunks(total_parts, total_size, source_folder, dest):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        with open(dest, 'wb+') as destination:
            for i in xrange(int(total_parts)):
                part = os.path.join(source_folder, str(i))
                with open(part, 'rb') as source:
                    destination.write(source.read())

    @staticmethod
    def upload(file, attrs):        
        fhash   = attrs['qquuid']
        upload_type = 'file'
        upload_icon = 'fa-file-o'
        filename = secure_filename(attrs['qqfilename'])

        def is_unique(url):
            now = datetime.datetime.now()
            exist = Media.get(Media.guid == "{}/{}/".format(now.year, now.month)+url)
            if not exist:
                return url

            i = 1
            ext = url.split('.')
            while Media.get(Media.guid == "{}/{}/".format(now.year, now.month)+url):
                add  = '{}{}'.format('-', i)
                url = ext[0]+add+'.'+ext[1]
                i += 1 

            return url

        filename = is_unique(filename)
        chunked = False
        fdir    = Media.upload_path(config.UPLOAD_DIRECTORY)
        fpath   = os.path.join(fdir, filename)
        

        if attrs.has_key('qqtotalparts') and int(attrs['qqtotalparts']) > 1:
            chunked = True
            fdir    = Media.upload_path(config.CHUNKS_DIRECTORY)
            fpath   = os.path.join(fdir, filename, str(attrs['qqpartindex']))

        Media.upload_save(file, fpath)

        if chunked and (int(attrs['qqtotalparts']) - 1 == int(attrs['qqpartindex'])):
            Media.upload_combine_chunks(attrs['qqtotalparts'], attrs['qqtotalfilesize'], os.path.dirname(fpath), os.path.join(Media.upload_path(config.UPLOAD_DIRECTORY), filename))
            shutil.rmtree(os.path.dirname(os.path.dirname(fpath)))

        mime = magic.Magic(mime=True)
        mime_file = mime.from_file(os.path.join(Media.upload_path(config.UPLOAD_DIRECTORY), filename))

        if mime_file not in Media.allowed_upload_types:
            os.remove(os.path.join(Media.upload_path(config.UPLOAD_DIRECTORY), filename))
            return jsonify(success=False, error='File type not allowed.'), 400

        if mime_file in Media.upload_types_images:
             upload_type = 'image'
             upload_icon = ' fa-file-image-o'

        media_hash = Media.hash_file(fpath)
        if Media.get(Media.uid == media_hash):
            media = Media.get(Media.uid == media_hash)
            media.modified = datatime.datetime.now()
            media.save()

            return jsonify(success=True), 200

        now = datetime.datetime.now()
        media = Media.create()
        media.uid           = media_hash
        media.type          = upload_type
        media.name          = filename
        media.guid          = "{}/{}/".format(now.year, now.month)+filename
        media.source        = fpath
        media.icon          = upload_icon

        media.save()

        if upload_type == 'image':
            images = FyImage(fpath).generate()
            sizes = {}

            for image in images:
                sizes[image[3]] = {'name': image[1], 'source': os.path.join(Media.upload_path(config.UPLOAD_DIRECTORY), image[0]), 'guid': "{}/{}/".format(now.year, now.month)+image[2]}

            media.data = {'var':sizes}
            media.save()
            
        flash(messages['added']+' ('+str(media)+')')

        return jsonify(success=True), 200

    @staticmethod
    def hash_string(txt):
        hasher = hashlib.sha1()
        hasher.update(txt)
        return hasher.hexdigest() 

    @staticmethod
    def hash_file(file):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()

        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

        return hasher.hexdigest()