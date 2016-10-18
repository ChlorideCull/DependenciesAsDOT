# DependenciesAsDOT
Enumerate all package dependencies, export as a DOT directed graph.

## Usage
If using Debian/Ubuntu/Other APT based distro, make sure you have `apt-rdepends` and `aptitude` installed, then run `dependsasdot.py`. DOT file is printed to stdout, so you should probably pipe it.

### Other package managers
In the `# Configuration constants #` block, set `rdependscmd` to an rdepends compatible command. It needs to output data in the following form:

    wget
      Depends: libc6 (>= 2.17)
      Depends: libidn11 (>= 1.13)
      Depends: libssl1.0.0 (>= 1.0.0)
      Depends: libuuid1 (>= 2.16)
      Depends: zlib1g (>= 1:1.1.4)
    libc6
      Depends: libgcc1
    libgcc1
      Depends: gcc-4.9-base (= 4.9-20140406-0ubuntu1)
      Depends: libc6 (>= 2.14)
      PreDepends: multiarch-support
    gcc-4.9-base
    multiarch-support
      Depends: libc6 (>= 2.3.6-2)
    libidn11
      Depends: libc6 (>= 2.14)
      PreDepends: multiarch-support

Set `packagelistcmd` to a command which outputs all installed packages, one per line.