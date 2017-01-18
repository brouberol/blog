Title: Découverte de la command line Docker
Date: 2016-10-13
Category: Docker

Connectez vous sur la machine virtuelle installée en première partie de la journée.

1 - Installez docker
```bash
$ sudo su
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

9 - Pullez l'image `brouberol/nginx`
```bash
$ docker pull brouberol/nginx
```

10 - Lancez l'image `brouberol/nginx` avec la commande suivante
```
$ docker run -it --rm --name=nginx-1 -p 80:80 brouberol/nginx
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
CONTAINER ID    IMAGE             COMMAND              CREATED         STATUS          PORTS                NAMES
76ee1a3f4ce2    brouberol/nginx   "./entrypoint.sh"    7 seconds ago   Up 6 seconds    0.0.0.0:80->80/tcp   nginx-1
```
À quoi servait l'option `-p 80:80` de la commande `docker run`?

14 - Listez les ports hosts/conteneurs liés a votre conteneur via `docker port <id>` (dans l'exemple précédent, `<id>` vallait `76ee1a3f4ce2`).

15 - Interrogez votre conteneur nginx via `curl localhost`

16 - Recuperez l'IP publique de votre VM via `ip -o -4 addr show eth0 | awk '{print $4}' | cut -d'/' -f `

17 - Ouvrez votre navigateur et visitez `http://<public_ip>`

18 - Inspectez votre conteneur via la commande `docker inspect`.

19 - Lancez la commande `docker history --no-trunc brouberol/nginx` et tentez de comprendre la différence entre l'image `nginx` de base et l'image `brouberol/nginx`.

20 - Inspectez le Dockerfile et l'entrypoint utilisés via les commandes suivantes:

   * `docker exec nginx-1 cat Dockerfile`
   * `docker exec nginx-1 cat entrypoint.sh`

21 - À quoi sert `docker exec`?

22 - Selon vous, pourquoi utilisons nous un `exec` dans l'entrypoint? Indice: la commande `docker stop` envoie un SIGTERM au process PID 1 du conteneur.

23 - Visitez [https://hub.docker.com/explore/](https://hub.docker.com/explore/), et tentez de deployer une autre application officiellement supportée par Docker!
