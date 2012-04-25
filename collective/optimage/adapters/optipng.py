# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class OptiPng(CoreImageOptimizeAdapter):
    """Optimize using optipng"""
    implements(IOptimageProvider)
    
    for_image = 'png'
    command = os.environ.get('OPTIPNG_PATH') or 'optipng'
    arguments = ['-o3', '-quiet']
    
