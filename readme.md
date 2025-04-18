My custom Path of Exile 2 item filter.

# Development

## Requirements

1. [GNU Make](https://www.gnu.org/software/make/)
2. Python 3.4 or later (for [virtual environment support](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments))

If you're on most Linux distributions, these will already be pre-installed so you don't need to do anything.

## Building

Open a terminal in root of this repostory and run:

```shell
make
```

The first time it's run,it will automatically create the [Python virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) and install [Jinja](https://jinja.palletsprojects.com/en/stable/) and [jinja-cli](https://github.com/mattrobenolt/jinja2-cli) to it, before attempting to build the filter. Subsequent builds should be instant and not require it to install anything.
