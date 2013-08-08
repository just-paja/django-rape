# django-rape

Django module for managing js, (s)css and other website resources.

## Features

- Merges and compresses javascript and scss files into one
- Manages serial numbers for resource URLs ('path/to/image?serial=1') inside templates, styles and javascripts
- Define multiple css/js packages
- Manage css/js order inside package


## Overview

Simple tool, that helps you minimize your traffic, site loading time and browser image caching.


### Dependencies 

Rape requires scss lib for parsing scss.
https://github.com/klen/python-scss


### Known issues

- Scss @import will not work
- Scss code errors will result into fatal error while parsing


## Usage

1. Add `rape` into `INSTALLED_APPS`
2. Setup `ROOT` to point to your project dir. You wouldn't like the default.
3. Move your scripts and styles into `RAPE_PATH`.
4. Setup `RAPED_SCRIPTS` and `RAPED_STYLES`
5. Use filters `raped_script` and `raped_style` to insert scripts and styles into django templates.


### Example

settings.py

	# Path to project
	ROOT = os.path.abspath(os.path.dirname(__file__) + "/..")
	
	# Script lists under a name
	RAPED_SCRIPTS = {
		"foo":[
			"bar", 
			"jebka"
		]
	}
	
	# Style lists under names
	RAPED_STYLES = {
		"screen":[
			"style1",
			"style1_wide"
		]
	}
	
	# Minify files. Results into generating smaller files.		
	RAPE_PACK = True
		
template.html
	
	<html>
	<head>
		<script type="text/javascript" src="{% raped_script 'foo' %}"></script>
		<link rel="stylesheet" type="text/css" href="{% raped_style 'screen' %}">
		...

And that's it! Rape should handle the rest of it.


## Serial numbers

If need to change scripts, styles and images on production sites, then you might want to use serial numbers.


### Example

Raising serial number will regenerate scripts and styles and also force the browser to download new file instead of reading from cache.

settings.py

	RAPED_SERIAL = 2

There is one template tag for (S)CSS and JS files called raped_url. It adds current serial number to URLs.

style1.scss
	
		...
		background-image:url({% raped_url '../pixmaps/jebka.png' %});
		...
		
Resulting into
	
	...
	background-image:url(../pixmaps/jebka.png?serial=2);
	...
