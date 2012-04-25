# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class Gifsicle(CoreImageOptimizeAdapter):
    """Optimize using gifsicle"""
    implements(IOptimageProvider)
    
    for_image = 'gif'
    command = os.environ.get('GIFSICLE_PATH') or 'gifsicle'
    arguments = ['-o3', '-I', '-w']
    
