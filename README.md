# arches-docs

This repo holds the official Arches documentation, published at https://arches.readthedocs.io. It uses reStructuredText, built with Sphinx.

## reporting an issue

If you find a problem with the documentation, or feel that something is lacking, first look through the [existing issues](https://github.com/archesproject/arches-docs/issues) in this repo to see if someone has already reported the problem, and then add your input to the ticket (at least a thumbs up!). If no ticket exists for the problem, please [create a new one](https://github.com/archesproject/arches-docs/issues/new) and add as much detail as possible.

## contributing

We welcome content contributions. Please begin by forking this repo. To contribute you will make changes to your fork, and then make pull requests to ask that those changes be incorporated here.

You can edit your fork either directly in Github (good for very small or non-complex edits) or by cloning and building the documentation locally (necessary for substantial edits).

In either case, you'll need to consider whether your documentation contribution should be for the **current stable release** of Arches, for a **new/unreleased feature**, or for both. Because of our branch versioning system (see below), your answer will require slightly different workflows. If you are new to Github, and the answer is "both", then just follow the steps for new/unreleased features below, and we'll help you figure the rest out.

- **To document new/unreleased features (arches.readthedocs.io/en/latest)**

    - Make a new branch from `master`
        - Name it `master_<description of change>`, e.g. `master_update_installation_steps`
    - Commit your changes -- push to your repo
        - Please put the ticket number your commit addresses in the commit message, e.g. "make small text update for #175"
    - Make a PR here against `master`.

- **To update documentation for the current release (arches.readthedocs.io/en/stable)**

    - Make a new branch from the highest numbered branch.
        - Name it `<branch number>_<description of change>`, e.g. `5.0_update_installation_steps`
    - Commit your changes -- push to your repo
        - Please put the ticket number your commit addresses in the commit message, e.g. "make small text update for #175"
    - Make a PR against the original branch, e.g. `5.0`.

- **To update documentation for new *and* stable releases**

    - Make a new branch from `master`
        - Name it `master_<description of change>`, e.g. `master_update_installation_steps`
    - Commit your changes -- push to your repo
    - Run `git reflog` and copy the hashes for all of the new commits you have made.
    - Switch to the highest numbered branch
    - Make a new branch
        - Name it `<branch number>_<description of change>`, e.g. `5.0_update_installation_steps`
    - Run `git cherry-pick <hash>` for each of hashes you have recorded -- push to your repo
    - Make 2 PRs in this repo:
        - One will compare your `master_...` branch to this `master` branch
        - One will compare your `5.0_...` branch to this `5.0` branch

Thank you!

## branch/release versioning

A separate branch is maintained for each minor release of Arches, from 2.1 to the current release. This is mainly to play nice with Read the Docs, but also to allow discrete updates to specific documentation at any time. However, this means that **merging between version branches should never happen.**

In Read the Docs, the branch with the highest version number will be used for the "stable" build ([arches.readthedocs.io/en/stable](https://arches.readthedocs.io/en/stable)), while the `master` branch will be used for the "latest" build ([arches.readthedocs.io/en/latest](https://arches.readthedocs.io/en/latest)).

When a new release of Arches is made, we'll branch `master` off into a new numbered branch, and it will become the new "stable" documentation.

Any documentation for unreleased features should be committed to `master`. Any documentation updates for existing releases should be committed to the appropriate branch, and where applicable we use `git cherry-pick` to apply specific commits to `master` as well.
    
## making a local build

+ to install

  first create and activate a python virtual environment. then:

      git clone https://github.com/<your gh username>/arches-docs
      cd arches-docs
      pip install -r requirements.txt
    
+ to build

      cd docs
      make html
    
+ to view, open `docs/_build/html/index.html` in a browser

+ to build a non-master version, checkout the appropriate branch

      git fetch --all
      git branch 4.1.1 origin/4.1.1
      make html
    
    you may want to delete the `_build` directory between builds of different versions, or if big changes have been made

## patterns to follow when writing

### internal links to other documentation sections

Use the `:ref:` directive to link to **any header anywhere in the docs**, doesn't matter what page it is on. Two examples:

Given that there is a header (of any level) somewhere in the documentation that looks like

    Arches Collector Workflow
    -------------------------

#### Example 1 - Display the header name itself

- reStructured Text

        See :ref:`Arches Collector Workflow` for more information.

- Result

    See [Arches Collector Workflow](https://arches.readthedocs.io/en/stable/using-arches-collector/#arches-collector-workflow) for more information.

#### Example 2 - Display arbitrary text

- reStructured Text

        See the :ref:`collector docs <Arches Collector Workflow>` for more information.

- Result

    See the [collector docs](https://arches.readthedocs.io/en/stable/using-arches-collector/#arches-collector-workflow) for more information.

### images with links to themselves

If you want an image that is a hyperlink to the file itself, use a `figure` instead of an image. The figure is automatically turned into a link, **but only if a height or width attribute is set**.

    .. figure:: images/datamodel-arches-4.4.1-032119.svg
        :width: 100%
        :align: center

        Data model showing only Arches models. (including a caption is optional but encouraged)

Previously we had used

    .. image:: images/datamodel-full-4.4.1-032119.svg
        target: /_images/datamodel-full-4.4.1-032119.svg
    
and while this works on a local build, it does not work when published in RTD (https://github.com/archesproject/arches-docs/issues/120).

## resources

+ Arches code-base: https://github.com/archesproject/arches
+ Arches user forum: https://groups.google.com/forum/#!forum/archesproject
+ reStructuredText primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

### release ticket label greens

`#00ef39` ![#00ef39](https://via.placeholder.com/30/00ef39/000000?text=3.1)
`#00da34` ![#00da34](https://via.placeholder.com/30/00da34/000000?text=4.0)
`#00c52e` ![#00c52e](https://via.placeholder.com/30/00c52e/000000?text=4.1)
`#00a527` ![#00a527](https://via.placeholder.com/30/00a527/000000?text=4.2)
`#00781c` ![#00781c](https://via.placeholder.com/30/00781c/ffffff?text=4.3)
`#006b19` ![#006b19](https://via.placeholder.com/30/006b19/ffffff?text=4.4)
`#005a15` ![#005a15](https://via.placeholder.com/30/005a15/ffffff?text=5.0)
`#00480e` ![#00480e](https://via.placeholder.com/30/00480e/ffffff?text=5.1)
`#003f0a` ![#003f0a](https://via.placeholder.com/30/003f0a/ffffff?text=6.0)
