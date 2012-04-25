# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute

class IOptimageProvider(Interface):
    """Something able to optimize an image"""

    for_image = Attribute("""Image file type""")

    def optimize(source):
        """Optimize the content image(s)"""
