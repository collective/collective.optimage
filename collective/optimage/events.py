# -*- coding: utf-8 -*-

from zope.component import getAdapters
from collective.optimage.interfaces import IOptimageProvider

def optimage_event(context, event):
        
        image_file = context.REQUEST.form.get('image_file')
        if image_file:
            field = context.getField('image')
            content_type = field.getContentType(context)
            if content_type.find('/')>-1:
                image_type = content_type.split('/')[-1]
                adapters = getAdapters((context, context.REQUEST), provided=IOptimageProvider)
                for name,adapter in adapters:
                    if adapter.for_image==image_type:
                        adapter.optimize()
