# django-rape

Django module for managing resources.

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
2. Move your scripts and styles into `RAPE_PATH`. It is "`ROOT`/rape" by default.
3. Setup `RAPED_SCRIPTS` and `RAPED_STYLES`
4. Use filters `raped_script` and `raped_style` to insert scripts and styles into django templates.

### Example

	settings.py
	
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
			<script type="text/javascript" src="{{ 'foo' | raped_script }}"></script>
			<link rel="stylesheet" type="text/css" href="{{ 'screen' | raped_style }}">
			...

	And that's it! Rape should handle the rest of it.

## Serial numbers

If need to change scripts, styles and images, then you might want to use serial numbers.

### Example

	This will regenerate scripts and styles and also force the browser to download new file instead of reading from cache.

	settings.py
	
		RAPED_SERIAL = 2

	There is one tmeplate tag for (S)CSS and JS files called raped_url. It adds current serial number to URLs.
	
	style1.scss
	
		...
		background-image:url({% raped_url '../pixmaps/jebka.png' %});
		...
		
	Resulting into
	
	...
	background-image:url(../pixmaps/jebka.png?serial=2);
	...
