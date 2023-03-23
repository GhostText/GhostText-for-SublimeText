# Contributing


## Download

Download it zipped:

https://github.com/GhostText/GhostText-for-SublimeText/archive/refs/heads/main.zip

or via git:

```sh
git clone https://github.com/GhostText/GhostText-for-SublimeText.git
```

## Install

Place the folder in your Sublime Text "Packages" directory, or create a link to it, for example:

```sh
ln -s \
    ~/repos/GhostText-for-SublimeText \
    ~/Library/Application Support/Sublime Text 3/Packages/ghosttext-local
```

### Package directory

The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 3/Packages/

* Linux:

        ~/.config/sublime-text-3/Packages/

* Windows:

        %APPDATA%/Sublime Text 3/Packages/

## Running a local version

Sublime Text will automatically load the plugin, you can see it in its console. However it seems that it doesn't properly reload it when the extension changes, you will have to restart Sublime Text.

## Publishing

Package Control automatically picks up new tags, so they can be [created on GitHub](https://github.com/GhostText/GhostText-for-SublimeText/releases/new).
