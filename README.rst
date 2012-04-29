.. contents:: **Table of contents**

Introduction
============

This Plone add-on perform (lossless) optimization image content types, using external processes.

.. Note::
   This software is in **alpha version**. Using this in a production site can hurt your performance.
   
   Read documentation *carefully*.

How it works
============

Your site users will continue to load image contents normally, but the data loaded will be taken from
external optimization software (that must live on the server) for executing
**image lossless transformation**.

In this way the final result will be commonly an smaller image, loaded quickly by browsers.

Supported software
------------------

Right now this product supports those command line tools:

``jpegoptim`` 
    For JPEG optimization - http://freecode.com/projects/jpegoptim
``jpegtran``
    For JPEG optimization - http://jpegclub.org/jpegtran/
``gifscicle``
    For GIT optimization - http://www.lcdf.org/gifsicle/
``optipng``
   For PNG optimization - http://optipng.sourceforge.net/
``pngout``
   For PNG optimization- http://advsys.net/ken/util/pngout.htm

Adding your own
---------------

If you like to provide support for additional software, you can do it using ZCA in your own products.
You need to provide a named adapter for the `IOptimageProvider interface`__.

__ https://github.com/keul/collective.optimage/blob/master/collective/optimage/interfaces.py#L5

An example::

      <adapter
  	      name="yournewsoftware"
          for="plone.app.blob.interfaces.IATBlobImage
               zope.publisher.interfaces.browser.IHTTPRequest"
          provides="collective.optimage.interfaces.IOptimageProvider"
          factory="yout.products.module.YourSoftwareAdapter"
          />

Finally, you adapter class will be comething like this::

    from zope.interface import implements
    from collective.optimage.interfaces import IOptimageProvider

    class YourSoftwareAdapter(object):
        """Optimize using yournewsoftware"""
        implements(IOptimageProvider)
    
        for_image = 'jpeg'

        def optimize(self):
            ...

Note that you must fill the ``for_image`` providing the image type you want to threat with this plugin.

Tips and know issues
====================

Command line tool position
--------------------------

Right now this product will try to run all of the software given above simply calling them.
If the program is not available at the user that run Zope process you could like to manually
specify it. The same if the software has been manually installed (for example: inside a buildout
installation and not system wide).

To do this, provide a environment var called "*SOFTWARENAME*\_PATH". An example::

    [instance]
    
    ...
    
    environment-vars =
        ...
        JPEGOPTIM_PATH /opt/local/bin/jpegoptim

Disable software
----------------

If you have problems with one or more of external programs you can disable it using the same kind
of environment vars given above. An example::

    [instance]
    
    ...
    
    environment-vars =
        ...
        PNGOUT_PATH False

Performance
-----------

Operations done by external processes are synchronous, so blocking the Zope thread.
This will for sure lower your site performance when a user is providing new images
(or modifying existings ones).
 