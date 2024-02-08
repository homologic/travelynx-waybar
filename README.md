# Travelynx integration for waybar

This script adds a very simple [travelynx](https://travelynx.de)
integration into [waybar](https://github.com/Alexays/Waybar), showing
the name of the station the user is traveling to as well as the
currently estimated arrival time.

## Usage

- Request a travelynx status API token

Add the following lines to your waybar config, replacing the path to
the script and the travelynx token with the appropriate values, and
registering the plugin at the desired position in the bar.


	"custom/travelynx": {
		"format": "{}",
		"exec": "/path/to/script.py [travelynx_token]",
		"interval": 20,
		"return-type": "json",
		"on-click": "x-www-browser https://travelynx.de",
    },
	
	
Optionally, a css class can be set for the script:

```
#custom-travelynx {
	background-color: #000000;
	padding: 0 5px;
}
```

Note that this module is still very much WIP and new features may be
added at any time.


## Credits

Copyright (c) 2024 Antonia <antonia@antonia.is>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
