# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class JpegOptim(CoreImageOptimizeAdapter):
    """Optimize using jpegoptim"""
    implements(IOptimageProvider)
    
    for_image = 'jpeg'
    command = os.environ.get('JPEGOPTIM_PATH') or 'jpegoptim'
    arguments = ['--strip-all', '-q']
    
