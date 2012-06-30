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

By default adding this plugin is not enough. You must include all supported software you have installed
on you server (or limiting it to what you want to use).

To do this, include a proper zcml file in your buildout configuration::

    [instance]
    ...
    eggs =
        Plone
        ...
        collective.optimage
    
    zcml =
        ...
        collective.optimage:wantedoptimizator1.zcml
        collective.optimage:wantedoptimizator2.zcml
        ...

All *wantedoptimizatorX* entries must be one of the supported software below.
An example::

    zcml =
        collective.optimage:jpegoptim.zcml
        collective.optimage:optipng.zcml

To include them all (excluded pngout), just include the "*all.zcml*".

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
``pngcrush``
   For PNG optimization - http://pmt.sourceforge.net/pngcrush/
``pngout`` (*slow*)
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
          factory="your.products.module.YourSoftwareAdapter"
          />

Finally, your adapter class will be something like this::

    from zope.interface import implements
    from collective.optimage.interfaces import IOptimageProvider

    class YourSoftwareAdapter(object):
        """Optimize using yournewsoftware"""
        implements(IOptimageProvider)
    
        for_image = 'jpeg'

        def optimize(self):
            // do stuff, calling external process

Note that you must fill the ``for_image`` providing the image type you want to threat with your plugin.

Tips and know issues
====================

Command line tool position
--------------------------

Right now this product will try to run all of the software given above simply calling them.
If the program is not available at the user that run Zope process you could like to manually specify where
is it.
The same if the software has been manually installed (for example: if you manually downloaded
and installed it inside a buildout installation and not system wide).

To do this, provide a environment var called "*SOFTWARENAME*\_PATH". An example::

    [instance]
    
    ...
    
    environment-vars =
        ...
        JPEGOPTIM_PATH /opt/local/bin/jpegoptim

Content types
-------------

Right now Plone Image content type is the only one supported. Unluckily Plone News item is still not using
Zope BLOB support so it will not gain any optimization.

Performance
-----------

Operations done by external processes are synchronous, so **blocking the Zope thread**.
This will lower your site performance when an editor is providing new images
(or modifying existings ones).

You can make them quicker (but less efficient), playing with configuration options.

On performance (again)
----------------------

Right now optimization are done *after* the image has been loaded on Plone. An event is fired after
the image source change, then the image is put on a temp file and then processed.
After that the optimized image is loaded again.

This is also done for all scaled image versions.

This is inefficient, so probably will change in future, however is the only way I found without monkey-patch
Plone.
