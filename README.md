# arches-docs

This repo holds the documentation that is published at https://arches.readthedocs.io, which is the official location for Arches documentation.

A separate branch is maintained for each recent release of Arches, from the last official v3 release (3.1.2) to the current v4 release. Read the docs will recognize the branch with the latest version number as the `stable` build. The `latest` build is made from the `master` branch, so any documentation for new features that are in development should be committed to master.

To update or add documentation for the current stable release of Arches, for example 4.1.0 (the current release as of this writing), please make a new branch `docfix_4.1.0` based on the `4.1.0` branch and then make a PR against the `4.1.0` branch. We can then `cherry-pick` those commits into `master`.
    
## make a local build

to install

    git clone https://github.com/archesproject/arches-docs
    cd arches-docs
    pip install -r requirements.txt
    
to build

    cd docs
    make html
    
to view, enter `_build/html` and open `index.html` in a browser

to build a non-master version, checkout the appropriate branch

    git checkout 4.0.1
    make html
    
you may want to delete the `_build` directory between builds of different versions, or if big changes have been made
