Title: Découverte de la command line Docker
Date: 2016-10-13
Category: Docker

Connectez vous sur la machine virtuelle installée en première partie de la journée.

1 - Installez docker
```bash
$ apt-get install docker.io
```

2 - Assurez vous que docker est correctement installé. Si c'est le cas, vous devriez avoir une sortie similaire à celle-ci:
```bash
$ docker info
Containers: 20
 Running: 2
 Paused: 0
 Stopped: 18
Images: 70
Server Version: 1.12.1
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Backing Filesystem: extfs
 Dirs: 153
 Dirperm1 Supported: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
 Volume: local
 Network: bridge host null overlay
Swarm: inactive
Runtimes: runc
Default Runtime: runc
Security Options:
Kernel Version: 3.16.0-4-amd64
Operating System: Debian GNU/Linux 8 (jessie)
OSType: linux
Architecture: x86_64
CPUs: 1
Total Memory: 3.779 GiB
Name: gallifrey
ID: RYUC:5OT6:3JFQ:APQG:QEW7:V7KP:ZDYY:WBBF:LZL5:PSFY:WFEH:MF6V
Docker Root Dir: /var/lib/docker
Debug Mode (client): false
Debug Mode (server): false
Registry: https://index.docker.io/v1/
WARNING: No memory limit support
WARNING: No swap limit support
WARNING: No kernel memory limit support
WARNING: No oom kill disable support
WARNING: No cpu cfs quota support
WARNING: No cpu cfs period support
Insecure Registries:
 127.0.0.0/8
```

3 - Listez les commandes disponibles:
```bash
$ docker
```

4 - Listez les images disponibles localement
```bash
$ docker images
```

5 - Pullez l'image `ubuntu`
```bash
$ docker pull ubuntu
```

6 - Listez les images disponibles localement
```bash
$ docker images
```

7 - Lancez un `echo "hello world!"` dans votre image `ubuntu`
```bash
$ docker run ubuntu echo "hello world"
```

8 - Listez *tous* les conteneurs. Pourquoi le conteneur est-il en status `Exited`?
```
$ docker ps -a
```

9 - Pullez l'image `nginx`
```bash
$ docker pull nginx
```

10 - Lancez l'image nginx avec la commande suivante
```
$ docker run -it --rm --name=nginx-1 -P nginx
```

11 - Lancez un `docker run --help` et tentez de comprendre les options passées dans la commande précédente

12 - Ouvrez un second terminal et ouvrez une session ssh dans votre VM

13 - Inspectez les conteneurs:
```
$ docker ps
```

Vous devriez avoir une sortie telle que
```
$ docker ps
CONTAINER ID    IMAGE     COMMAND                  CREATED         STATUS          PORTS                                           NAMES
76ee1a3f4ce2    nginx-1   "nginx -g 'daemon off"   7 seconds ago   Up 6 seconds    0.0.0.0:32769->80/tcp, 0.0.0.0:32768->443/tcp   nginx-1
```

14 - Listez les ports hosts/conteneurs lies a votre conteneur via `docker port <id>` (dans l'exemple precedent, `<id>` vallait `76ee1a3f4ce2`).

15 - Interrogez votre conteneur nginx via `curl http://localhost:<host_port>` (dans l'exemple precedent, `<host_port>` vallait `32768`)

16 - Recuperez l'IP publique de votre VM via `ip -o -4 addr show eth0 | awk '{print $4}' | cut -d'/' -f 1`

17 - Ouvrez votre navigateur et visitez `http://<public_ip>:<host_port>`
