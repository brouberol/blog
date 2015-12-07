Title: Installing Guitar Pro 6 on Fedora 22+
Date: 2015-12-06
Category: Linux

I've been playing guitar for the last 10 years now, but I spent the last 4 years only playing and singing alone. I decided to improve my technique, and to treat me with [Guitar Pro 6](http://www.guitar-pro.com/en/index.php?pg=guitar-pro-6). I was happy to see they even supported Linux natively! Sadly, they only provide a deb file, and no rpm. I'll thus describe here how I managed to install it on Fedora 22, ♬ *with a little help from my friends* ♫.

![GuitarPro screenshot](https://upload.wikimedia.org/wikipedia/en/0/0a/GP6-pic2.png)

### Installing the dependencies

First, download the Guitar Pro deb file. Mine was called ``gp6-full-linux-demo-r11686.deb``
Extract the archive called ``data.tar.gz`` from the deb, and then de-archive it:

    :::bash
    $ cd /tmp
    $ mv ~/Downloads/gp6-full-linux-demo-r11686.deb .
    $ ar vx gp6-full-linux-demo-r11686.deb
    $ tar -xvf data.tar.gz

Create the installation directory for Guitar Pro.

    :::bash
    $ sudo mkdir -p /opt/GuitarPro6

Move the GuitarPro files to the installation directory.

    :::bash
    $ sudo mv ./opt/GuitarPro6/ /opt/GuitarPro6/

We now need to install Guitar Pro's dependencies, and of course, they're 32 bit...

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

You might have to download other packages as well, as Guitar Pro was not my first 32 bit program I had to install.

*Note*: The required packages will be listed when you execute the ``/opt/GuitarPro6/launcher.sh`` script, and you can use the ``dnf whatprovides`` command to find the package that provides each required library.

Sadly, that's not it yet. GuitarPro also depends on both ``libcrypto`` and ``libssl`` 0.9.8, and they're not packaged anymore in Fedora 22.
We'll use a very cool trick: by a great stroke of luck, the libraries contained in the ``openssl`` Ubuntu deb package are usable as a drop-in replacement!

    :::bash
    $ wget -q http://security.ubuntu.com/ubuntu/pool/universe/o/openssl098/libssl0.9.8_0.9.8o-7ubuntu3.2.14.04.1_i386.deb 1>/dev/null
    $ ar x libssl0.9.8_0.9.8o-7ubuntu3.2.14.04.1_i386.deb data.tar.xz
    $ tar --strip-components 3 \
        -xf data.tar.xz \
        ./lib/i386-linux-gnu/libcrypto.so.0.9.8 \
        ./lib/i386-linux-gnu/libssl.so.0.9.8
    $ chmod 755 libssl.so.0.9.8 libcrypto.so.0.9.8
    $ mv libssl.so.0.9.8 libcrypto.so.0.9.8 /opt/GuitarPro6

Seriously, how cool is that [^1]?

*Note*: I moved both shared libraries to the ``/opt/GuitarPro6`` directory, because it also contained numerous other ones. My guess, which turned out to be correct, was that the executable uses will look for shared objects in its directory. This way, I didn't have to fiddle with ``LD_LIBRARY_PATH`` and ``ldconfig``.

### Installing the sound banks

We now need to install the sound banks. First, download them from the official website. Then, install them via the ``/opt/GuitarPro6/GPBankInstaller`` script:

    :::bash
    $ sudo mv Banks-r370.gpbank /opt/GuitarPro6
    $ sudo /opt/GuitarPro6/GPBankInstaller /opt/GuitarPro6/Soundbanks.gpbank /opt/GuitarPro6/Data/Soundbanks/

### Make Guitar Pro the default program for tab files

We then install the desktop and icon file that were packaged in the Guitar Pro deb, so that it can be executed from the app launcher.

    :::bash
    $ sudo cp ./usr/share/applications/GuitarPro6.desktop /usr/share/applications/GuitarPro6.desktop
    $ sudo cp ./usr/share/pixmaps/guitarpro6.png /usr/share/pixmaps/

The last and final step is the cherry on the cake: we're going to make Guitar Pro open automatically when opening the tab files. We first define the ``application/x-guitar-pro`` MIME-type and then associate it with the ``gp3``, ``gp4``, ``gp5`` and ``gp6`` extensions.

    :::bash
    $ cat <<EOF > guitarpro-mime.xml
    <?xml version="1.0"?>
        <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
        <mime-type type="application/x-guitar-pro">
            <glob pattern="*.gp3"/>
            <glob pattern="*.gp4"/>
            <glob pattern="*.gp5"/>
            <glob pattern="*.gp6"/>
        </mime-type>
    </mime-info>
    EOF
    $ sudo xdg-mime install guitarpro-mime.xml
    $ xdg-mime default GuitarPro6.desktop application/x-guitar-pro

Done. You should now be able to click on a tab file, and enjoy!

### Conclusion

I managed to make everything work, with both some help and luck. I would however had prefered if the Guitar Pro binary was compiled statically, to ease the installation process.

Also, when you advertise Linux compatibility, please, PLEASE, at least mention the package format (deb, rpm, other), and also mention the distributions you support natively.

Finally, when you want to support Linux, do not **ever** redirect Linux users to the Windows installation guide, by stating that both processes are ["substantially similar"](https://support.guitar-pro.com/hc/fr/articles/201863332-GP6-Je-viens-d-acheter-Guitar-Pro-6-que-dois-je-faire-). They are not.

On that note (get it?), keep on rocking in a free world!


### Sources

* [https://www.linux.com/community/blogs/128-desktops/494464](https://www.linux.com/community/blogs/128-desktops/494464)
* [https://github.com/dpurgin/guitarpro6-rpm/](https://github.com/dpurgin/guitarpro6-rpm/)
* [https://stackoverflow.com/questions/30931/register-file-extensions-mime-types-in-linux](https://stackoverflow.com/questions/30931/register-file-extensions-mime-types-in-linux)

[^1]: We can of course try to include them from other [rpm-based distributions](http://www.rpmfind.net/linux/rpm2html/search.php?query=openssl-devel+0.9.8&submit=Search+...&system=&arch=), but I have to admin I found it cooler this way.

