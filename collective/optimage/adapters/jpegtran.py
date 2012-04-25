# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class JpegTran(CoreImageOptimizeAdapter):
    """Optimize using jpegtran"""
    implements(IOptimageProvider)
    
    for_image = 'jpeg'
    command = os.environ.get('JPEGTRAN_PATH') or 'jpegtran'
    arguments = ['-copy', 'none', '-progressive', '-outfile']
    
