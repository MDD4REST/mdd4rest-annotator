
from __future__ import with_statement

from message import Messager
from annotation import open_textfile
from common import ProtocolError
from config import DATA_DIR
from document import real_directory
from annotation import JOINED_ANN_FILE_SUFF, TEXT_FILE_SUFFIX
from os.path import join as join_path
from os.path import isdir, isfile, exists, abspath
from os import access, W_OK, makedirs

import json
import urllib


def auto_annotate(collection, docid):
    if len(docid) > 4 and docid[-4] == '.':
        docid = docid[:-4]

    directory = collection

    if directory is None:
        dir_path = DATA_DIR
    else:
        #XXX: These "security" measures can surely be fooled
        if (directory.count('../') or directory == '..'):
            raise InvalidDirError(directory)

        dir_path = real_directory(directory)

    # Is the directory a directory and are we allowed to write?
    if not isdir(dir_path):
        raise InvalidDirError(dir_path)
    if not access(dir_path, W_OK):
        raise NoWritePermissionError(dir_path)

    ############################
    from session import get_session
    try:
        username = get_session()['user']
    except KeyError:
        username = None
    if username != 'admin':
        if (not username) or username + '/' not in dir_path:
            raise NoWritePermissionError(dir_path)
    ############################

    base_path = abspath(join_path(dir_path, docid))
    txt_path = base_path + '.' + TEXT_FILE_SUFFIX
    ann_path = base_path + '.' + JOINED_ANN_FILE_SUFF
    
    #Messager.info("base_path: " + base_path)

    with open(txt_path) as infile:
        txtdata = [s for s in infile.read().split('\n')]
    
    i = 0
    data = {}
    data["project_name"] = docid
    data["project_requirements"] = []
    for req in txtdata:
        i += 1
        data["project_requirements"].append({"id": "FR" + str(i), "text": req})
    data["annotation_format"] = "ann"
    
    url = "http://nlp.scasefp7.eu:8010/nlpserver/project"
    data = json.dumps(data)
    req = urllib.Request(url, data, {'Content-Type': 'application/json'})
    content = urllib.urlopen(req).read()
    content = json.loads(content)
    rsize = 0
    
    annTid = 1
    annRid = 1
    idmap = {}
    for i, ann_req in enumerate(xx["annotation"] for xx in content["annotations"]):
        for ann in ann_req:
            ann = ann.split()
            if ann[2].isdigit():
                idmap[str(i) + ":" + ann[0]] = "T" + str(annTid)
                annTid += 1
            else:
                idmap[str(i) + ":" + ann[0]] = "R" + str(annRid)
                annRid += 1
    
    ann_output = ""
    for i, ann_req in enumerate(xx["annotation"] for xx in content["annotations"]):
        for ann in ann_req:
            ann = ann.split()
            if ann[2].isdigit():
                ann4 = txtdata[i][int(ann[2]):int(ann[3])]
                ann_output += idmap[str(i) + ":" + ann[0]] + '\t' + ann[1] + ' ' + str(int(ann[2]) + rsize) + ' ' + str(int(ann[3]) + rsize) + '\t' + ann4 + "\n"
            else:
                ann_output += idmap[str(i) + ":" + ann[0]] + '\t' + ann[1] + ' Arg1:' + idmap[str(i) + ":" + ann[2][5:]] + ' Arg2:' + idmap[str(i) + ":" + ann[3][5:]] + "\n"
        rsize += len(txtdata[i]) + 1
    
    with open(ann_path, 'w') as annotfile:
        annotfile.write(ann_output)
    
    return {}
