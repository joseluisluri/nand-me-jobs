#!/usr/bin/env python3
import logging
import re
import os
import sys
import urllib
import zipfile
import xml.etree.ElementTree as etree
import utils
import mongodb
import time

COLLECTION_NAME = 'datomatic'

# model
class Rom:
    def __init__(self):
        self.name = ""
        self.size = ""
        self.crc = ""
        self.md5 = ""
        self.sha1 = ""

class Game:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.roms = []

class DatObject:
    def __init__(self):
        self.tag = ""
        self.name = ""
        self.description = ""
        self.version = ""
        self.timestamp = time.time()
        self.updated = True
        self.games = []

def do():
    # init
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log = logging.getLogger('datomatic')

    CWD_PATH = os.path.abspath(os.path.dirname(__file__))
    CURRENT_DIR = '.'
    INPUT_DIR = 'datfiles'

    os.chdir(CWD_PATH)
    os.chdir(INPUT_DIR)

    files = os.listdir(CURRENT_DIR);
    for dat_zip in files:
        # extract
        log.debug('Extracting ' + dat_zip)
        zip_ref = zipfile.ZipFile(dat_zip, 'r')
        zip_ref.extractall(CURRENT_DIR)
        zip_ref.close()
        log.debug('Done')

        # xml parse
        basename = os.path.splitext(dat_zip)[0]
        datfile = basename + '.dat'
        log.debug('DAT file: ' + datfile)

        tree = etree.parse(datfile)
        os.remove(datfile)
        root = tree.getroot()

        datobject = DatObject()
        for node in root:
            if node.tag == 'header':
                datobject.name = node.find('name').text
                datobject.description = node.find('description').text
                datobject.version = node.find('version').text
                datobject.tag = re.sub('[ ]+', '-', re.sub('[^a-z0-9 ]', '', datobject.name.lower()))

            elif node.tag == 'game':
                game = Game()
                game.name = node.attrib['name']
                game.description = node.find('description').text

                for subnode in node.findall('rom'):
                    rom = Rom()
                    rom.name = subnode.attrib['name']
                    rom.size = subnode.attrib['size'] if 'size' in subnode.attrib else ""
                    rom.crc = subnode.attrib['crc'] if 'crc' in subnode.attrib else ""
                    rom.md5 = subnode.attrib['md5'] if 'md5' in subnode.attrib  else ""
                    rom.sha1 = subnode.attrib['sha1'] if 'sha1' in subnode.attrib  else ""
                    game.roms.append(rom)

                datobject.games.append(game)

        try:
            document = utils.jsony(datobject)
            collection = mongodb.get_collection(COLLECTION_NAME)
            collection.remove({'name': datobject.name})
            mongodb.insert(COLLECTION_NAME, document)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    do()