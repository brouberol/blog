{% from "note.j2" import note %}
---
Title: Pinning your SQLite version across environments
Date: 2023-08-25
Category: Programming
Description: A walkthrough of how to pin an sqlite version and feature set accross multiple environments, architectures and OSes.
Summary: This article discusses the challenges of maintaining consistent versions of the SQLite library in different environments for a project that relies heavily on it. Unlike traditional databases, where server versions can be easily pinned, SQLite is embedded in applications, leading to potential feature mismatches due to what version is made available by each environment's system package manager.
Tags: SQLite
status: draft
Keywords: sqlite, fastapi, python, docker
---


The [project](https://github.com/brouberol/5esheets) I'm currrently working on only has a single external dependency: [SQLite](https://www.sqlite.org/), with [full text search](https://www.sqlite.org/fts5.html) enabled. As a result, the application is extremely easy to package and run. However, I found out that ensuring that you have the _exact same_ SQLite [version and feature](https://github.com/brouberol/5esheets/pull/207#issuecomment-1672131123) set in all your environments (development machines running macOS and linux, CI and production) is trickier than I expected.

When you rely on a traditional database server (PostgreSQL, MySQL, mongoDB, etc), you can achieve this by running the same server version in all your environments.

{{ note("Docker really shines there, as it allows to do just that in a single command.
```extbash
$ docker run postgres:15.4
```
") }}

Things are a bit different with SQLite, as it is _not_ an SQL server. It is a _library_ that you embed in your program (either by compiling it alongside your code, or by relying on a shared library and language bindings). Python does the latter: its `sqlite3` package is written in C using the CPython API, and [includes](https://github.com/python/cpython/blob/4ae3edf3008b70e20663143553a736d80ff3a501/Modules/_sqlite/connection.h#L32) the `sqlite3.h` header file. Where does this header file come from though?

### Inspecting the sqlite version on linux

If we have a look at a `python3.11` installation directory on a random Ubuntu server, we see that it bundles an `_sqlite.so` shared object, that itself dynamically loads `libsqlite3.so.0`.

```extbash
$ find /usr/lib/python3.11  -name "*sqlite3*.so"
/usr/lib/python3.11/lib-dynload/_sqlite3.cpython-311-x86_64-linux-gnu.so
$ ldd /usr/lib/python3.11/lib-dynload/_sqlite3.cpython-311-x86_64-linux-gnu.so
	linux-vdso.so.1 (0x00007ffcda976000)
	libsqlite3.so.0 => /lib/x86_64-linux-gnu/libsqlite3.so.0 (0x00007fab44d9c000) # <--
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fab44a00000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fab44cb3000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fab44f17000)
```

Same question: where does `/lib/x86_64-linux-gnu/libsqlite3.so.0` come from then?

```extbash
$ apt-file search /lib/x86_64-linux-gnu/libsqlite3.so.0
libsqlite3-0: /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
libsqlite3-0: /usr/lib/x86_64-linux-gnu/libsqlite3.so.0.8.6
$ apt-cache search libsqlite3-0
libsqlite3-0 - SQLite 3 shared library
```

This means that python relies on whatever `libsqlite3` version is installed by the _system package manager_. We can double check this by having a look at the `python3` package recursive dependencies: [`python3`](https://packages.ubuntu.com/lunar/python3) -> [`libpython3-stdlib`](https://packages.ubuntu.com/lunar/libpython3-stdlib) -> [`libpython3.11-stdlib`](https://packages.ubuntu.com/lunar/libpython3.11-stdlib) -> [`libsqlite3-0`](https://packages.ubuntu.com/lunar/libsqlite3-0).

To know what version is installed on that system, we can inspect the version of the `libsqlite3-0` apt package:

```extbash
$ apt-cache show libsqlite3-0 | grep Version
Version: 3.40.1-1
```

We can check that we're getting this exact version via python:

```python
>>> import sqlite3
>>> conn = sqlite3.connect(":memory:")
>>> conn.execute("select sqlite_version()").fetchone()
('3.40.1',)
```

### Inspecting the sqlite version on macOS

Assuming you are installing your packages via `brew` on macOS, you'll find that it does things a bit differently than `apt`. The `python3` formula [depends on `sqlite`](https://github.com/Homebrew/homebrew-core/blob/1aa36b1d93b4ee968d8d355640735f5ec21e7262/Formula/p/python@3.11.rb#L30), which itself [downloads](https://github.com/Homebrew/homebrew-core/blob/1aa36b1d93b4ee968d8d355640735f5ec21e7262/Formula/s/sqlite.rb#L4) an `sqlite` archive pinned to a given version (`3.43.0` at the time of writing), and then [compiles `libsqlite3.dylib`](https://github.com/Homebrew/homebrew-core/blob/1aa36b1d93b4ee968d8d355640735f5ec21e7262/Formula/s/sqlite.rb#L36-L56).

Indeed, we see this library when inspecting the content of the `sqlite` brew package:

```extbash
~ ❯ ls -alh /opt/homebrew/opt/sqlite/lib/libsqlite3.dylib
lrwxr-xr-x    18 br   16 May 15:45  /opt/homebrew/opt/sqlite/lib/libsqlite3.dylib -> libsqlite3.0.dylib
```

And sure enough, we see that we're running the expected version in python:

```python
>>> import sqlite3
>>> conn = sqlite3.connect(":memory:")
>>> conn.execute("select sqlite_version()").fetchone()
('3.43.0',)
```

### Pinning the sqlite version by vendoring the compiled library


To pin the `sqlite` version across all environments and OSes, we can compile these shared/dynamically loaded libraries ourselves for all architectures we plan to support, vendor them in our codebase, and inject them into our application via `LD_PRELOAD`.

We'd need to cover all the ways we run the app:

- running `make run`, which runs the app on the host, against the version of `sqlite` installed by the package manager
- running `make docker-run`, which runs the application in a docker container against the `sqlite` version available through the image OS package manager
- running `make test` in CI (Github Actions), which runs the test against the `sqlite` version made available by the runner OS package manager

Compiling the sqlite source code into a shared library was made easy to do as [Simon Willison](https://simonwillison.net/) already [documented](https://til.simonwillison.net/sqlite/sqlite-version-macos-python) the process.

#### Compiling `libsqlite3` for linux

The following script compiles `libsqlite3` for linux, with full text search enabled:

```extbash
# script/compile-libsqlite-linux.sh
#!/usr/bin/env bash
set -e

apt-get install -y build-essential wget tcl

# link associated with sqlite 3.42.0, found on https://www.sqlite.org/src/timeline?t=version-3.42.0
# pointing to https://www.sqlite.org/src/info/831d0fb2836b71c9
sqlite_ref=831d0fb2
wget https://www.sqlite.org/src/tarball/${sqlite_ref}/SQLite-${sqlite_ref}.tar.gz
tar -xzvf SQLite-${sqlite_ref}.tar.gz
pushd SQLite-${sqlite_ref}

CPPFLAGS="-DSQLITE_ENABLE_FTS5" ./configure
make

popd
mv SQLite-${sqlite_ref}/.libs/libsqlite3.so ./lib/
rm -r SQLite-${sqlite_ref}.tar.gz SQLite-${sqlite_ref}
```


#### Compiling `libsqlite3` for macOS

The following script compiles `libsqlite3` for macOS, with full text search enabled:


```extbash
# script/compile-libsqlite-macos.sh
#!/usr/bin/env bash

set -eu

sqlite_version=3420000

wget https://www.sqlite.org/2023/sqlite-amalgamation-${sqlite_version}.zip
unzip sqlite-amalgamation-${sqlite_version}.zip
pushd sqlite-amalgamation-${sqlite_version}

gcc -dynamiclib sqlite3.c -o libsqlite3.0.dylib -lm -lpthread -DSQLITE_ENABLE_FTS5

popd
mv sqlite-amalgamation-${sqlite_version}/libsqlite3.0.dylib ./lib/
rm -r sqlite-amalgamation-${sqlite_version}.zip sqlite-amalgamation-${sqlite_version}
```


#### Compiling the right version on-demand

We then define a `$(libsqlite)` `make` target, either pointing to `lib/libsqlite3.so` if you run the app on linux, or `lib/libsqlite3.0.dylib` if you run it on macOS. We finally make sure to override the system shared library by the vendored one when running the app, via `LD_PRELOAD` on linux and `DYLD_LIBRARY_PATH` on macOS.

```makefile
# Makefile

UNAME_S := $(shell uname -s)
PWD := $(shell pwd)
ifeq ($(UNAME_S),Linux)
	libsqlite = lib/libsqlite3.so
	ld_preload = LD_PRELOAD=$(PWD)/$(libsqlite)
else ifeq ($(UNAME_S),Darwin)
	libsqlite = lib/libsqlite3.0.dylib
	ld_preload = DYLD_LIBRARY_PATH=$(PWD)/lib
endif

app-root = dnd5esheets
poetry-run = $(ld_preload) poetry run

lib/libsqlite3.so:
	@./scripts/compile-libsqlite-linux.sh

lib/libsqlite3.0.dylib:
	@./scripts/compile-libsqlite-macos.sh

build: $(libsqlite) ...

test:
	@$(poetry-run) pytest

run: build ...
	@cd $(app-root) && $(poetry-run) uvicorn --factory $(app-root).app:create_app --reload
```

#### Compiling `libsqlite3` in docker

While the previous steps work, they also prove to be quite brittle, as they only works for a given CPU architecture. For example, the `libsqlite3.0.dylib` library will not load on an Intel Mac if it was compiled on a M1 or M2.

The most robust way to go remains building `libsqlite3` in a [build stage](https://docs.docker.com/build/building/multi-stage/) of the docker image process. This way, you _know_ that you only need to build it for linux, whatever the host OS is, and you're guaranteed that it will be built for your CPU architecture, thanks to the [multi-arch property](https://hub.docker.com/layers/library/python/3.11.4-slim-bullseye/images/sha256-1226f32ad1c1c36e0b6e79706059761c58ada308f4a1ad798e55dab346e10e91?context=explore) of the `python:3.11.4-slim` base image.


```Dockerfile
# Dockerfile
...
# -- Build the libsqlite3.so shared object for the appropriate architecture
FROM python:3.11.4-slim AS sqlite-build

WORKDIR /app/src/build

COPY scripts/compile-libsqlite-linux.sh ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential wget tcl && \
    ./compile-libsqlite-linux.sh && \
    apt-get remove -y build-essential wget tcl && \
    apt-get auto-clean


# -- Main build combining the FastAPI and compiled frontend apps
FROM python:3.11.4-slim
...
COPY --from=sqlite-build /app/src/build/libsqlite3.so ./lib/libsqlite3.so
CMD ["./start-app.sh"]
```

```extbash
# start-app.sh
#!/bin/bash

set -e

exec \
    env LD_PRELOAD=./lib/libsqlite3.so \ # inject the LD_PRELOAD environment variable in the process
    uvicorn --factory dnd5esheets.app:create_app --host "0.0.0.0" --port 8000
```

### Unit testing the SQLite version and feature set

With all of that said and done, we can now expose the `sqlite` version and compilation options through a debug API handler:

```python
# dnd5esheets/api/debug.py
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session

debug_api = APIRouter(prefix="/debug")


@debug_api.get("/sqlite")
async def sqlite_info(
    session: AsyncSession = Depends(create_scoped_session),
):
    """Return debug information about the sqlite database"""
    version = (await session.execute(text("select sqlite_version()"))).scalar_one()
    pragma_compile_options = (
        (await session.execute(text("pragma compile_options"))).scalars().all()
    )
    return {
        "version": version,
        "compile_options": pragma_compile_options,
    }

```

We can then query the `sqlite` version through the API:
```extbash
❯ curl -s localhost:8000/api/debug/sqlite | jq .version
"3.42.0"
```

However, we can go even further! By unit-testing the version and compile options, we ensure that our CI uses the exact required `sqlite` version and feature set.

```python
# dnd5esheets/tests/test_api_debug.py

def test_sqlite_version(client):
    sqlite_debug_info = client.get("/api/debug/sqlite").json()
    assert sqlite_debug_info["version"] == "3.42.0"
    assert "ENABLE_FTS5" in sqlite_debug_info["compile_options"]

```

{{ note("
See the effect of vendoring the compiled library in CI: [before](https://github.com/brouberol/5esheets/actions/runs/5956139650/job/16156271800#step:8:49) / [after](https://github.com/brouberol/5esheets/actions/runs/5960929753/job/16169158344#step:8:24).
")}}

### Sources
- [https://til.simonwillison.net/sqlite/python-sqlite-environment](https://til.simonwillison.net/sqlite/python-sqlite-environment)
- [https://til.simonwillison.net/sqlite/sqlite-version-macos-python](https://til.simonwillison.net/sqlite/sqlite-version-macos-python)
