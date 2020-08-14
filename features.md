## List of available features

**Index :**
- [dj-for](#dj-for)
- [dj-for-data](#dj-for-data)
- [dj-if](#dj-if)
- [dj-block](#dj-block)
- [dj-ref](#dj-ref)
- [dj-load](#dj-load)
- [static links](#static-links)
- [Work in progess](#work-in-progress)

You must use `dj` to prefix all of your attributes inside Bootstrap Studio.

To check example from test, `*.html` file is content inside bss, and `*.render.html` will correspond to rendered attributes.

#### dj-for

From [bss-file](test/html_templates/for_loop/basic.html) to [django-file](test/html_templates/for_loop/basic.render.html)

#### dj-for-data

Used to emulate replace for loop content within Bootstrap Studio.

From [bss-file](test/html_templates/for_loop/for_data.html) to [django-file](test/html_templates/for_loop/for_data.render.html)

#### dj-if

From [bss-file](test/html_templates/if/basic.html) to [django-file](test/html_templates/if/basic.render.html)

#### dj-block

From [bss-file](test/html_templates/block/basic.html) to [django-file](test/html_templates/block/basic.render.html)

#### dj-ref

From [bss-file](test/html_templates/reference/basic.html) to [django-file](test/html_templates/reference/basic.render.html)

#### dj-load

From [bss-file](test/html_templates/load/basic.html) to [django-file](test/html_templates/load/basic.render.html)

#### Static links

Url for local resources will be convert to use static tag, like : `{% static 'folder/with/file' %}`.
`script`, `img` and `link` tag will convert their attributes.

From [bss-file](test/html_templates/static_links/src.html) to [django-file](test/html_templates/static_links/src.render.html)

Css `url()` links inside html will be also convert, for background image as example.

From [bss-file](test/html_templates/static_links/css_url.html) to [django-file](test/html_templates/static_links/css_url.render.html)


## Work in progress
Nothing
