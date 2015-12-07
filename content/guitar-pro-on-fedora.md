Title: Installing Guitar Pro 6 on Fedora 22+
Date: 2015-12-06
Category: Linux

I've been playing guitar for the last 10 years now, but I spent the last 4 years only playing and singing alone. I decided to improve my playing and technique, and to treat me with [Guitar Pro 6](http://www.guitar-pro.com/en/index.php?pg=guitar-pro-6). I was happy to see they even supported Linux natively! However, they only provide a deb file, and no rpm. I'll describe here how I managed to install it on my Fedora 22, with a little help from my friends ♬♫.

![GuitarPro screenshot](https://upload.wikimedia.org/wikipedia/en/0/0a/GP6-pic2.png)

First, download the Guitar Pro deb file. Mine was called ``gp6-full-linux-demo-r11686.deb``
Extract the archive called ``data.tar.gz`` from the deb, and then de-archive it:

    :::bash
    $ tar -xvf data.tar.gz

Create the installation directory for Guitar Pro

    :::bash
    $ sudo mkdir -p /opt/GuitarPro6

Move the GuitarPro files to the installation directory

    :::bash
    $ sudo cp -R opt/GuitarPro6/ /opt/GuitarPro6/

We now need to install GuitarPro's dependencies, and of course, they're 32 bit.

    :::bash
    $ sudo dnf install libICE.i686 \
        libSM.i686 \
        libssh.i686 \
        libxml2.i686 \
        libxslt.i686 \
        libpng12.i686 \
        libvorbis.i686 \
        alsa-lib.i686 \
        portaudio.i686 \
        pulseaudio-libs.i686

You might have to download other packages as well, as Guitar Pro was not my first 32bit program I had to install. The required packages will be listed when you execute the ``/opt/GuitarPro6/launcher.sh`` script, and you can use the ``dnf whatprovides`` command to find the package that provides each required library.

Sadly, that's not it yet. GuitarPro also depends on both libcrypto and libssl 0.9.8, and they're not packaged anymore in Fedora 22. The trick is to download them from a Ubuntu deb file, and install them manually.

    :::bash
    $ wget -q http://security.ubuntu.com/ubuntu/pool/universe/o/openssl098/libssl0.9.8_0.9.8o-7ubuntu3.2.14.04.1_i386.deb 1>/dev/null
    $ ar x libssl0.9.8_0.9.8o-7ubuntu3.2.14.04.1_i386.deb data.tar.xz
    $ tar -xf data.tar.xz ./lib/i386-linux-gnu/libcrypto.so.0.9.8 --strip-components 3
    $ tar -xf data.tar.xz ./lib/i386-linux-gnu/libssl.so.0.9.8 --strip-components 3
    $ chmod +x libssl.so.0.9.8 libcrypto.so.0.9.8
    $ mv libssl.so.0.9.8 libcrypto.0.9.8 /opt/GuitarPro6

We now need to install the sound banks. First, download them from the official website. Then, install them via the ``/opt/GuitarPro6/GPBankInstaller`` script:

    :::bash
    $ sudo mv Banks-r370.gpbank /opt/GuitarPro6
    $ sudo /opt/GuitarPro6/GPBankInstaller /opt/GuitarPro6/Soundbanks.gpbank /opt/GuitarPro6/Data/Soundbanks/

We then install the desktop and icon file, so that Guitar Pro can be executed from the App launcher.

    :::bash
    $ sudo cp usr/share/applications/GuitarPro6.desktop /usr/share/applications/GuitarPro6.desktop
    $ sudo cp usr/share/pixmaps/guitarpro6.png /usr/share/pixmaps/

The last and final step is the cherry on the cake: we're going to make Guitar Pro open automatically when opening the tab files. We first define the ``application/x-guitar-pro`` MIME-type and then associate it with the ``gp3``, ``gp4``, ``gp5`` and ``gp6`` extensions.

    :::bash
    $ echo '<?xml version="1.0"?>
     <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
       <mime-type type="application/x-guitar-pro">
       <glob pattern="*.gp3"/>
       <glob pattern="*.gp4"/>
       <glob pattern="*.gp5"/>
       <glob pattern="*.gp6"/>
      </mime-type>
     </mime-info>
    ' > guitarpro-mime.xml
    $ sudo xdg-mime install guitarpro-mime.xml
    $ xdg-mime default GuitarPro6.desktop application/x-guitar-pro

Done. Keep on rocking in a free world!

Sources:

* [https://www.linux.com/community/blogs/128-desktops/494464](https://www.linux.com/community/blogs/128-desktops/494464)
* [https://github.com/dpurgin/guitarpro6-rpm/](https://github.com/dpurgin/guitarpro6-rpm/)
* [https://stackoverflow.com/questions/30931/register-file-extensions-mime-types-in-linux](https://stackoverflow.com/questions/30931/register-file-extensions-mime-types-in-linux)