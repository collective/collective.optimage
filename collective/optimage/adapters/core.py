# -*- coding: utf-8 -*-

import subprocess
import tempfile
import shutil
import os, os.path

from Acquisition import aq_base

from plone.app.blob.config import blobScalesAttr

from collective.optimage import logger

class CoreImageOptimizeAdapter(object):
    """Core class. This is designed to be extended"""
    
    for_image = None
    command = ''
    arguments = []
    
    def __init__(self, instance, request):
        self.instance = instance
        self.request = request
        self.input = None
        self.output_name = None

    def _optimize(self, temp_output_file=False):    
        instance = self.instance
        field = instance.getField('image')
        filename = instance.getFilename('image')
        blob = field.get(instance).getBlob()
        self._optimize_blob(blob, temp_output_file)

    def _optimizeScales(self, temp_output_file=False):
        """Optimize also scaled version of images"""
        instance = self.instance
        fields = getattr(aq_base(self.instance), blobScalesAttr, {})
        if not fields:
            instance.getField('image').createScales(self.instance)
        fields = getattr(aq_base(self.instance), blobScalesAttr, {})
        for img in fields.values():
            for format, data in img.items():
                blob = data['blob']
                self._optimize_blob(blob, temp_output_file, format="image_%s" % format)

    def _optimize_blob(self, blob, temp_output_file=False, format="image"):
        """
        Internal optimization for blobs
        Use temp_output_file to use a temporay file for storing output
        (this for processes that do not change the input inline)
        """
        instance = self.instance
        self.input = blob.open()
        input_size = os.path.getsize(self.input.name) 
        self.input.close()

        if temp_output_file:
            output = tempfile.NamedTemporaryFile(suffix='.'+self.for_image,
                                                 prefix='tmp-imageoptim-',
                                                 delete=False)
            output.close()
            self.output_name = output.name
        else:
            oname = os.path.join(os.path.dirname(self.input.name),
                                 "tmp-imageoptim-" + os.path.basename(self.input.name) + '.'+self.for_image)
            shutil.copyfile(self.input.name, oname)
            self.output_name = oname

        try:
            logger.info('Running %s on %s (%s)' % (self.command, instance.absolute_url_path(), format))
            subprocess.check_call(self._getArguments())
        except subprocess.CalledProcessError, inst:
            logger.error("Running %s failed (exit status %s)" % (self.command, inst.returncode))
        except OSError:
            logger.error("Cannot run %s" % self.command)

        # Some optimizers don't work inline, so a bigger output file can happen
        if input_size > os.path.getsize(self.output_name):
            blob.consumeFile(self.output_name)
        
        # cleanup
        try:
            os.remove(self.output_name)
        except OSError:
            pass
    
    def _getArguments(self):
        """Get arguments for the external process"""
        return [self.command] + self.arguments + [self.output_name]
    
    def optimize(self):
        self._optimize()
        self._optimizeScales()

