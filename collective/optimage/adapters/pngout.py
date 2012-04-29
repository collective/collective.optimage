# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class PngOut(CoreImageOptimizeAdapter):
    """Optimize using ongout"""
    implements(IOptimageProvider)
    
    for_image = 'png'
    command = os.environ.get('PNGOUT_PATH') or 'pngout'
    arguments = ['-y', '-q']

    def _getArguments(self):
        """Get arguments for the external process"""
        return [self.command] + self.arguments + [self.input.name, self.output_name]

    def optimize(self):
        if self.command!='False':
            self._optimize(temp_output_file=True)
            self._optimizeScales(temp_output_file=True)
