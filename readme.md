My custom [Path of Exile 2](https://pathofexile2.com) item filter.

# Path of Exile 1

See also [my Path of Exile 1 item filter](https://gitlab.com/Ambient.Impact/path-of-exile-item-filter).

# Downloading

You can get the item filter via one of these means:

* [The most recent tagged release](https://gitlab.com/Ambient.Impact/path-of-exile-2-item-filter/-/releases/permalink/latest).
* [The most recent development build](https://gitlab.com/Ambient.Impact/path-of-exile-2-item-filter/-/artifacts). Look for the download link on the most recent "build" job.

# Development

## Requirements

1. [GNU Make](https://www.gnu.org/software/make/)
2. [Python](https://www.python.org/) 3.4 or later (for [virtual environment support](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments))
3. [`jq`](https://jqlang.org/)

If you're on most Linux distributions, these will already be pre-installed so you don't need to do anything.

## Building

Open a terminal in root of this repostory and run:

```shell
make
```

The first time it's run, it will automatically create the [Python virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) and install [Jinja](https://jinja.palletsprojects.com/en/stable/) and [jinja-cli](https://github.com/mattrobenolt/jinja2-cli) to it, before attempting to build the filter. Subsequent builds should be instant and not require it to install anything.
