# Installation

<span class="status status-real">REAL</span>

The CLI is a single Rust binary called `noetl`, with a short alias
`ntl`. There are three documented ways to install it. They do **not**
all give you the same version.

Each channel below was installed on a clean CI runner by the book's
`install-paths` workflow (`.github/workflows/install-paths.yml`), which
then ran `noetl --version` and the Chapter 1 example. Results as of
**2026-11-14**:

| Channel | Command | Version installed | Example ran |
|---|---|---|---|
| APT (Ubuntu 24.04) | see below | **6.4.0** (package `6.4.0-1`) | yes |
| PyPI | `pip install noetl` | **5.3.2** | yes |
| Homebrew (macOS) | `brew tap noetl/tap`, `brew trust noetl/tap`, `brew install noetl` | **6.4.0** (built from source) | yes |

The latest CLI release is **v6.4.0** (2026-11-11). The book's examples
are tested against it.

## APT (Debian / Ubuntu)

```console
$ echo 'deb [trusted=yes] https://noetl.github.io/apt noble main' | sudo tee /etc/apt/sources.list.d/noetl.list
$ sudo apt-get update
$ sudo apt-get install noetl
$ noetl --version
noetl 6.4.0
```

Use `jammy` instead of `noble` on Ubuntu 22.04. The source is marked
`trusted=yes`: the repository is not signed, so APT does not verify
its packages' origin.

## PyPI

```console
$ python -m venv .venv
$ .venv/bin/pip install noetl
$ .venv/bin/noetl --version
noetl 5.3.2
```

The PyPI package is **not** a Python implementation. It is the same
Rust CLI compiled as a Python extension, so it has no runtime
dependencies, and both `noetl` and `ntl` land on your path
(noetl/noetl README, "What is in this repository"). It is useful when
you want NoETL inside a Python environment, for example to call
`noetl.run(...)` from Python.

```admonish warning title="PyPI is behind"
As of 2026-11-14 the newest PyPI release is **5.3.2**, uploaded
2026-10-17. The CLI itself is at **6.4.0**. Behaviour in this book is
checked against 6.4.0. Where you need a newer CLI, install it from APT
or Homebrew.
```

## Homebrew (macOS)

```console
$ brew tap noetl/tap
$ brew trust noetl/tap
$ brew install noetl
$ noetl --version
noetl 6.4.0
```

```admonish warning title="`brew trust` is needed with current Homebrew"
The tap's own instructions say only `brew tap noetl/tap` and
`brew install noetl`. With **Homebrew 7.0.11** (the CI runner's version
on 2026-11-14), that fails: "Refusing to load formula noetl/tap/noetl
from untrusted tap noetl/tap." Homebrew's suggested fix,
`brew trust noetl/tap`, makes it work.
```

The formula (`noetl/homebrew-tap`, `Formula/noetl.rb`) builds the CLI
from the **v6.4.0** source tarball, so the first install compiles Rust
code. On a `macos-latest` GitHub runner it took **16 minutes**
(MEASURED: 2026-11-14, n = 1, including installing the Rust
toolchain).

## Check it works

```console
$ noetl --version
$ noetl run --help
```

## Check your understanding

{{#quiz ../quizzes/ch01-01.toml}}
