A custom [Path of Exile 2](https://pathofexile2.com) item filter for cool and attractive people.

# Path of Exile 1

See also [my Path of Exile 1 item filter](https://gitlab.com/Ambient.Impact/path-of-exile-item-filter).

# Downloading

You can get the item filter via one of these means:

* [Following the filter on my profile](https://www.pathofexile.com/item-filter/vrYnkxuJ); this will automatically update the filter whenever you launch the game, but you still have to manually download the sound files and place them in the correct location.
* [The most recent tagged release](https://gitlab.com/Ambient.Impact/path-of-exile-2-item-filter/-/releases/permalink/latest/downloads/assets/Ambient.Impact.filter.zip).
* [The most recent development build](https://gitlab.com/Ambient.Impact/path-of-exile-2-item-filter/-/artifacts). Look for the download link on the most recent "package" job for the `main` branch.

# Development

All development of this item filter is done on Linux. While it may be possible to get this working on Windows, I have no intention of spending time on that. [Gaming on Linux](https://ambientimpact.com/gaming/linux) is really good now, so why not join us?

## Requirements

1. [GNU Make](https://www.gnu.org/software/make/)
2. [GNU Core Utilities](https://en.wikipedia.org/wiki/GNU_Core_Utilities) and related tools like [xargs](https://en.wikipedia.org/wiki/Xargs)
3. [Python](https://www.python.org/) 3.9 or later required for [Poetry](https://python-poetry.org/)
4. [`jq`](https://jqlang.org/)

These are usually pre-installed on most flavours of Linux so you don't need to do anything if you're one of us.

## Building

Open a terminal in root of this repostory and run:

```shell
make
```

The first time this is run, it will automatically create the [Python virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) and install various Python dependencies to it before attempting to build the filter. Subsequent builds should be nearly instant and not require it to install anything. This will build the filter, assemble the sound files, and copy everything to the correct location in the Path of Exile 2 item filter directory under Steam on Linux.

To build just the filter, run:

```shell
make build
```

# Disclaimer

*This project isn't affiliated with nor endorsed by Grinding Gear Games in any way.*
