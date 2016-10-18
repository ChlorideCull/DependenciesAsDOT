#!/usr/bin/python3
import sys
import subprocess
import shlex
import re

#  Configuration constants  #
rdependscmd = "apt-rdepends {PKG}"
packagelistcmd = "aptitude search '~i' -F '%p'"
# packagelistcmd = "echo wget"  # For testing.
debug = False
#  End of configuration constants #
rdepends_depregex = re.compile(r'^  (?:Pre)?Depends: ([A-Za-z0-9\-\.]+).*$')

print("Getting list of packages... ", end="", file=sys.stderr)
sys.stderr.flush()
packages = subprocess.check_output(shlex.split(packagelistcmd), stderr=subprocess.DEVNULL).decode("utf-8")
packages = packages.splitlines()
print(len(packages), file=sys.stderr)

packagesdone = 0
loadeddata = {}
for package in packages:
    package = package.strip()  # For some reason aptitude adds vast amounts of whitespace, we need to remove it.
    packagesdone += 1
    if debug:
        print("Enumerating dependencies... Working on '{}', {count}/{total}".format(package,
                                                                                    count=packagesdone,
                                                                                    total=len(packages)),
              file=sys.stderr)
    else:
        print("Enumerating dependencies... {count}/{total}".format(count=packagesdone, total=len(packages)), end="\r",
              file=sys.stderr)
    sys.stderr.flush()
    if package in loadeddata.keys():
        continue
    rdependsoutput = subprocess.check_output(
        shlex.split(rdependscmd.format(PKG=package)), stderr=subprocess.DEVNULL).decode("utf-8")
    rdependsoutput = rdependsoutput.splitlines()

    currentpkg = [""]
    currentpkgdepends = []
    for line in rdependsoutput:
        if line[0] == " ":
            # Depends/PreDepends entry.
            regexpmatch = rdepends_depregex.fullmatch(line)
            if regexpmatch:
                if debug:
                    print("Adding '{}' as dependency of '{}'".format(regexpmatch.group(1), currentpkg[0]))
                currentpkgdepends.append(regexpmatch.group(1))
            else:
                print()
                print("ERROR: Failed to regexp match.")
                print("Source line: '{}'".format(line))
                exit(1)
        else:
            # Package entry.
            if len(currentpkg[0]) > 0:
                if debug:
                    print("Saving package '{}'".format(currentpkg[0]))
                loadeddata[currentpkg[0]] = currentpkgdepends
            if debug:
                print("Current package is now '{}'".format(line.strip()))
            currentpkg[0] = line.strip()
            currentpkgdepends = []
print("", file=sys.stderr)

print("digraph PackageDeps {")
for packagename in loadeddata:
    for dep in loadeddata[packagename]:
        print("  \"{}\" -> \"{}\";".format(packagename, dep))
print("}")
