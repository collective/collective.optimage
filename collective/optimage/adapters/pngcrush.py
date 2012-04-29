# -*- coding: utf-8 -*-

import os

from zope.interface import implements
from collective.optimage.interfaces import IOptimageProvider
from collective.optimage.adapters.core import CoreImageOptimizeAdapter

class PngCrush(CoreImageOptimizeAdapter):
    """Optimize using pngcrush"""
    implements(IOptimageProvider)
    
    for_image = 'png'
    command = os.environ.get('PNGCRUSH_PATH') or 'pngcrush'
    arguments = ['-rem', 'alla', '-reduce', '-q'] # -brute option disabled... too slow

    def _getArguments(self):
        """Get arguments for the external process"""
        return [self.command] + self.arguments + [self.input.name, self.output_name]

    def optimize(self):
        self._optimize(temp_output_file=True)
        self._optimizeScales(temp_output_file=True)
