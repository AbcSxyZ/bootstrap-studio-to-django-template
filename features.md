## List of available features

**Index :**
- dj-for
- dj-if
- dj-block
- dj-load
- static links

You must use `dj` to prefix all of your attributes inside Bootstrap Studio.

To check example from test, `*.html` file is content inside bss, and `*.render.html` will correspond to rendered attributes.

## dj-for

From [bss-file](test/html_templates/for_loop/basic.html) to [django-file](test/html_templates/for_loop/basic.render.html)

## dj-if

From [bss-file](test/html_templates/if/basic.html) to [django-file](test/html_templates/if/basic.render.html)

## dj-block

From [bss-file](test/html_templates/block/basic.html) to [django-file](test/html_templates/block/basic.render.html)

## dj-load

From [bss-file](test/html_templates/load/basic.html) to [django-file](test/html_templates/load/basic.render.html)

## Static links

Url for local resources will be convert to use static tag, like : `{% static 'folder/with/file' %}`.
`script`, `img` and `link` tag will convert their attributes.

Css `url()` links inside html will be also convert, for background image as example.

From [bss-file](test/html_templates/static_links/src.html) to [django-file](test/html_templates/static_links/src.render.html)
