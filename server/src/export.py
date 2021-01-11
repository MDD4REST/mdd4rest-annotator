#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

'''
Export functionality.
'''

from __future__ import with_statement

import os
from os.path import join as path_join
from message import Messager
from config import DATA_DIR
from session import get_session
from docimport import NoWritePermissionError, InvalidDirError
from document import real_directory
from os.path import isdir, isfile, abspath
from os import access, W_OK
from annotation import JOINED_ANN_FILE_SUFF, TEXT_FILE_SUFFIX
from common import NoPrintJSONError
from annotation import open_textfile
from auth import allowed_to_read
from owlexport.convertproject import ReadProject

def export_document(document, collection, extension):
    directory = collection
    real_dir = real_directory(directory)
    fname = '%s.%s' % (document, 'txt')
    fpath = path_join(real_dir, fname)
    rr = None
    # data = real_dir
    # hdrs = [('Content-Type', 'application/octet-stream'), ('Content-Disposition', 'inline; filename=%s' % fname)]
    if allowed_to_read(fpath):
        rr = ReadProject()
        owlfile, ttlfile = rr.read_project(real_dir, document, extension)
        fpaths = owlfile if extension[0:3] == 'owl' else ttlfile
        if extension[-1] == 's':
            fname = '%s.%s' % (document, "zip")
            hdrs = [('Content-Type', 'application/octet-stream'), ('Content-Disposition', 'inline; filename=%s' % fname)]
            from zipfile import ZipFile
            with ZipFile(path_join(real_dir, document) + ".zip", "w") as outfile:
                for f in fpaths:
                    with open(f) as infile:
                        outfile.writestr(f.split('/')[-1], infile.read())
            with open(path_join(real_dir, document) + ".zip", 'rb') as tmp_file:
                data = tmp_file.read()
        else:
            fname = '%s.%s' % (document, extension)
            #hdrs = [('Content-Type', 'text/plain; charset=utf-8'), ('Content-Disposition', 'inline; filename=%s' % fname)]
            hdrs = [('Content-Type', 'application/octet-stream'), ('Content-Disposition', 'inline; filename=%s' % fname)]
            with open_textfile(fpaths, 'r') as txt_file:
                data = txt_file.read().encode('utf-8')
    else:
        data = "Access Denied"

    try:
        raise NoPrintJSONError(hdrs, data)
    finally:
        if rr:
            rr.clean_up()
            if isfile(path_join(real_dir, '%s.%s' % (document, 'zip'))):
                os.remove(path_join(real_dir, '%s.%s' % (document, 'zip')))
     
