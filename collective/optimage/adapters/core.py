# -*- coding: utf-8 -*-

import subprocess
import tempfile

from collective.optimage import logger

class CoreImageOptimizeAdapter(object):
    """Core class. This is designed to be extended"""
    
    for_image = None
    command = ''
    arguments = []
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def optimize(self):
        context = self.context
        field = context.getField('image')
        filename = context.getFilename('image')
        try:
            blob = field.get(context).getBlob()
            file = blob.open()
        except AttributeError:
            # No blob support? I.E: a news item 
            file = tempfile.NamedTemporaryFile(suffix='.'+self.for_image, prefix='tmp-imageoptim-', delete=False)
            file.write(str(context.getField('image').get(context).data))
        file.close()

        try:
            logger.info('Running %s on %s' % (self.command, context.absolute_url_path()))
            subprocess.check_call([self.command] + self.arguments + [file.name])
            context.setImage(open(file.name))
            context.setFilename(filename, 'image')
            #field.removeScales(context)
            #field.createScales(context)
        except subprocess.CalledProcessError, inst:
            logger.error("Running %s failed (exit status %s)" % (self.command, inst.returncode))
        except OSError:
            logger.error("Cannot run %s" % self.command)
