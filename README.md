# OSD status dashboard _(wp2.2_dev)_

[![Demo backend API](https://img.shields.io/badge/Demo-CLICK%20HERE-red.svg?style=flat)](https://wp22dev.herokuapp.com/)
[![Python version](https://img.shields.io/badge/Python-3.10-blue.svg?style=flat&logo=Python&logoColor=white)](https://docs.python.org/3.8/)
![CodeQL](https://github.com/OPEN-NEXT/wp2.2_dev/workflows/CodeQL/badge.svg)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat)](https://github.com/RichardLitt/standard-readme)
[![REUSE compliance status](https://api.reuse.software/badge/github.com/OPEN-NEXT/wp2.2_dev)](https://api.reuse.software/info/github.com/OPEN-NEXT/wp2.2_dev)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](./CODE_OF_CONDUCT.md)
[![GitHub license](https://img.shields.io/github/license/OPEN-NEXT/wp2.2_dev.svg?style=flat)](./LICENSE)

*Initial proof-of-concept of data-mining backend for an open source development status dashboard*

Targeted at hosters of version control platforms (such as [Wikifactory](https://wikifactory.com/), [GitLab](https://gitlab.com/), or [GitHub](https://github.com/)), this Python backend program mines open source hardware repositories for metadata and calculates metrics based on it. This backend exposes a representational state transfer ([REST](https://en.wikipedia.org/wiki/Representational_state_transfer)) application programming interface ([API](https://en.wikipedia.org/wiki/Web_API)) where requests for those metrics can be made.

***This software is not for general consumers to just "double click" on and install on their devices***.

**Please see the [Install](#install) and [Usage](#usage) sections to get up and running with this tool**. For more details on its background and design considerations, please see the [Background](#background), ~~[Design notes](#design-notes), and [Future work](#future-work) sections. There is also a detailed [step-by-step walkthrough](docs/usage-example.md).~~
## Table of Contents

- [OSD status dashboard _(wp2.2\_dev)_](#osd-status-dashboard-wp22_dev)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
    - [Running from source](#running-from-source)
    - [Deploy as container](#deploy-as-container)
  - [Usage](#usage)
    - [Making requests to the REST API](#making-requests-to-the-rest-api)
    - [API response format](#api-response-format)
    - [Custom Wikifactory URLs](#custom-wikifactory-urls)
  - [Design notes](#design-notes)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [Acknowledgements](#acknowledgements)
  - [License](#license)

## Background

> Today’s industrial product creation is expensive, risky and unsustainable. At the same time, the process is highly inaccessible to consumers who have very little input in the design and distribution of the finished product. Presently, SMEs and maker communities across Europe are coming together to fundamentally change the way we create, produce, and distribute products.

[OPENNEXT](https://opennext.eu/) is a collaboration between 19 industry and academic partners across Europe. Funded by the [European Union](https://europa.eu/)'s [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) programme, this project seeks to enable small and medium enterprises (SMEs) to work with consumers, makers, and other communities in rethinking how products are designed and produced. [Open source hardware](https://www.oshwa.org/definition/) is a key enabler of this goal where the design of a physical product is released with the freedoms for anyone to study, modify, share, and redistribute copies. These essential freedoms are based on those of [open source software](https://opensource.org/osd), which is itself derived from [free software](https://www.gnu.org/philosophy/free-sw.en.html) where the word free refers to freedom, *not* free-of-charge. When put in practice, these freedoms could potentially not only reduce proprietary vendor lock-in, planned obsolescence, or waste but also stimulate novel – even disruptive – business models. The SME partners in OPENNEXT are experimenting with producing open source hardware and even opening up the development process to wider community participation. They produce diverse products ranging from [desks](https://stykka.com/), [cargo bike modules](http://www.xyzcargo.com/), to a [digital scientific instrument platform](https://pslab.io/) (and [more](https://opennext.eu/project-team/#sme)).

Work package 2 of OPENNEXT is gathering theoretical and practical insights on best practices for company-community collaboration when developing open source hardware. This includes running [Delphi studies](https://www.edelphi.org/) to develop a maturity model to describe the collaboration and developing a precise definition for what the "source" is in open source hardware. In particular, task 2.2 in this work package is developing a project status dashboard with "health" indicators showing the evolution of a project within the maturity model; design activities; or progress towards success based on project goals.

~~To that end, the month 18 deliverable for task 2.2 is focused on establishing the underlying "behind the scenes" infrastructure to mine data about open source hardware projects from version control repositories that they are hosted on (`osmine`). The Python scripts in this repository currently query the public [application programming interfaces](https://en.wikipedia.org/wiki/API) (APIs) of [GitHub](https://www.github.com/) and [Wikifactory](https://www.wikifactory.com/). Both platforms host version control repositories with the latter having a focus on supporting open source hardware projects. There is also a barebones proof-of-concept user-facing demonstration dashboard (`osdash`) which computes core metrics from the mined data and presents interactive visualisations. This dashboard is only to show that the underlying data could be displayed, and is not meant to confer immediate usefulness at this time.~~

To be clear, this deliverable ***is***: Designed to be deployed on a server operated by version control platforms such as Wikifactory or GitHub.

This deliverable ***is not***: For general end-users to install on consumer devices and "double click" to open.

There are other excellent open source software for open source project analytics and data visualisation, with [Grimoirelab](https://chaoss.github.io/grimoirelab/) being a prime example. However, the full Grimoirelab pipeline requires a full server stack necessitating advanced skills in heavy-duty (but potentially complicated) web technologies such as [Kibana](https://www.elastic.co/products/kibana) or [Elastisearch](https://www.elastic.co/products/elasticsearch). This project aims to create a lighter, more focused solution needing only the use of Python.

This documentation aims to demonstrate practices that facilitate design reuse, including of this repository. In addition to the [Install](#install) and [Usage](#usage) sections that increase reproducibility, ~~[Design notes](#design-notes) and [Future work](#future-work) communicate the thought process and lessons-learned while developing the dashboard. Together, they constitute an intangible body of "know-how" that is very often undocumented. For example, motivations for the internal data model or the approach to compressing data at the end of the section [Internal data structure](#internal-data-structure) which reduces disk usage are of practical benefit. But "snippets" of practical experience like these are seldom recorded.~~

In addition, this repository aims to follow international standards and good practices in open source development such as, but not limited to: 

* [SDPX 3](https://spdx.dev/) compliance with a [LICENSE](./LICENSE) file (also see [License](#license) section)
* [REUSE 3.0](https://reuse.software/) compliance with appropriate machine-readable SPDX metadata for all files and license texts in [`LICENSES`](./LICENSES/) directory
* README file (this document) conforming to the [Standard Readme Specification](https://github.com/RichardLitt/standard-readme)
* [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct for participants
* [CONTRIBUTING](./CONTRIBUTING.md) document outlining ways to contribute to this repository
* Naming the primary branch of this repository `main` instead of `master` following [modern best practices](https://github.blog/changelog/2020-10-01-the-default-branch-for-newly-created-repositories-is-now-main/)

## Install

This section assumes knowledge of Python, Git, and using a GNU/Linux-based server including installing software from package managers and running a terminal session.

**Note:** This software is designed to be deployed on a server by system administrators or developers, not on generic consumer devices.

This project requires [Python](https://www.python.org/) version 3.10 or later on your server and running it in a [Python virtual environment](https://docs.python.org/3.10/tutorial/venv.html) is optional but recommended. Detailed external library dependencies are listed in the standard-conformant [`requirements.txt`](./requirements.txt) file and also here: 

* [`aiohttp>=3.8.1`](https://pypi.org/project/aiohttp/)
* [`fastapi>=0.70`](https://pypi.org/project/fastapi/)
* [`gql>=3.0.0`](https://pypi.org/project/gql/)
* [`PyYAML>=5.4`](https://pypi.org/project/pyyaml/)
* [`requests>=2.28`](https://requests.readthedocs.io/en/latest/)
* [`uvicorn>=0.15`](https://pypi.org/project/uvicorn/)

In addition to Python and the dependencies listed above, the following programs must be installed and accessible from the command line: 

* [`git`](https://git-scm.com/) (version 2.7.4 or later)
* [`pip`](https://pip.pypa.io/) (version 19.3.1 or later)

A [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) is required top be available as an environmental variable. This is because the Python scripts will use it for GitHub API queries. This token is an alphanumeric string in the form of "ghp_2D5TYFikFsQ4U9KPfzHyvigMycePCPqkPgWc".

### Running from source

The code can be run from source and has been tested on updated versions of GNU/Linux server operating systems including [Red Hat Enterprise Linux](https://redhat.com/en/technologies/linux-platforms/enterprise-linux) 8.5. While effort has been made to keep the Python scripts platform-agnostic, they have not been tested under other operating systems such as [BSD](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution)-derivatives, [Apple macOS](https://www.apple.com/macos/) or [Microsoft Windows](https://www.microsoft.com/windows/) as they are rarely used for hosting code such as this (especially the latter two).

On your server, with the tools [`git`](https://git-scm.com/) and [`pip`](https://pip.pypa.io/) installed, run the following commands in a terminal session to retrieve the latest version of this repository and prepare it for development and running locally (usually for testing): 

```sh
git clone https://github.com/OPEN-NEXT/wp2.2_dev.git
pip install --user -r requirements.txt
```

The [`git`](https://git-scm.com/) command will download the files in this repository onto your server into a directory named `wp2.2_dev`, and [`pip`](https://pip.pypa.io/) installs the Python dependencies listed in [`requirements.txt`](./requirements.txt).

In a terminal window at the root directory of this repository, start the server with the [`uvicorn`](https://www.uvicorn.org/) Asynchronous Server Gateway Interface ([ASGI](https://en.wikipedia.org/wiki/Asynchronous_Server_Gateway_Interface)) server by running this command: 

```sh
uvicorn oshminer.main:app --reload
```

There will be some commandline output which ends with something like the following line: 

```
INFO:     Application startup complete.
```

This means the server API is up an running, and should be accessible on your local machine on port 8000 at 127.0.0.1.

### Deploy as container

There is a [`Dockerfile`](./Dockerfile) in this repository that defines a [container](https://en.wikipedia.org/wiki/OS-level_virtualization) within which this program can run.

To build and use the container, you need to have programs like [Podman](https://podman.io) or [Docker](https://en.wikipedia.org/wiki/Docker_(software)) installed.

With the repository cloned by `git` onto your system, navigate to it and build the container with this command:

```sh
podman build -t wp22dev ./ --format=docker
```

Replace the command `podman` with `docker` depending on which one is available (this project has been tested with Podman 4.0.2), and `wp22dev` can be replaced with any other name. `--format=docker` is needed to explicitly build this as a Docker-formatted container that will be accepted by cloud services like [Heroku](https://www.heroku.com/).

Then, the run the container on port 8000 at 127.0.0.1 with this command: 

```sh
podman run --env PORT=8000 --env GITHUB_TOKEN=[token] -p 127.0.0.1:8000:8000 -d wp22dev
```

Where `token` is the 40 character alphanumeric string of your GitHub API personal access token. It is in the form of "ghp_2D5TYFikFsQ4U9KPfzHyvigMycePCPqkPgWc".

The image built this way can be pushed to cloud hosting providers such as [Heroku](https://www.heroku.com/). With Heroku as an example: 

1. Set up an empty app from your Heroku dashboard.

2. In the Settings page for your Heroku app, set a [Config Var](https://devcenter.heroku.com/articles/config-vars) with Key "GITHUB_TOKEN" and Value being your GitHub API personal access token.

3. With the [Heroku commandline interface](https://devcenter.heroku.com/categories/command-line) installed, first login from your terminal: 

```sh
heroku container:login
```

4. Push the container image built above to your Heroku app: 

```sh
podman push wp22dev registry.heroku.com/[your app name]/web
```

5. Release the pushed container into production: 

```sh
heroku container:release web --app=[your app name]
```

A demo of this is hosted on Heroku with this API endpoint: 

```
https://wp22dev.herokuapp.com/data
```

This demo instance will go into a sleep state after a period of inactivity. If your API calls to this endpoint is taking more than a few seconds, it might be the demo waking from that state.

## Usage

The backend server listens to requests for information about a list of open source hardware (and software) repositories hosted on Wikifactory or GitHub. The GitHub backend is a placeholder for now, but the Wikifactory backend is now accessible.
### Making requests to the REST API

[GET requests](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) to the API are formed as [JSON](https://www.json.org/json-en.html) payloads to the `/data` endpoint.

There are two components to each request: 

1. `repo_urls`: An array of strings of repository [URL](https://en.wikipedia.org/wiki/URL)s, such as `https://wikifactory.com/+elektricworks/pikon-telescope`. Currently, metadata retrieval for Wikifactory project URLs is implemented. Each URL is composed of the Wikifactory domain (`wikifactory.com`), space (e.g. `+elektricworks`), and project (e.g. `pikon-telescope`).

2. `requested_data`: An array of strings representing the types of repository metrics desired for each repository. Currently, the following are implemented for Wikifactory projects: 
   1. `files_info`: The numbers and proportions of mechanical and electronic computer-assisted design (CAD), image, data, document, and other file types in the repository.
   2. `license`: The license for the repository.
   3. `tags`: Aggregated tags for the repository and any associated with the maintainers of that repsitory.
   4. `commits_level`: The hash identifier (contribution `id` for Wikifactory projects) and timestamp of each commit to the repository. This can be used to graph the commit activity level in a frontend visualisation.
   5. `issues_level`: Similar to `commits_level`, but for all issues in the repository.

The following is an example request that could be sent to the API for three Wikifactory projects: 

```
{
    "repo_urls": [
        "https://wikifactory.com/+dronecoria/dronecoria-frame", 
        "https://wikifactory.com/@luzleanne/community-composter", 
        "https://wikifactory.com/+elektricworks/pikon-telescope"
    ], 
        "requested_data": [
        "files_info", 
        "license", 
        "tags",
        "commits_level", 
        "issues_level"
    ]
}
```

### API response format

The API will respond with a JSON array containing the `requested_data` for each repository in `repo_urls`.

Specifically, for each repository, the response will include: 

* `repository`: String containing the repository URL.
* `platform`: String, only `Wikifactory` for now.
* `requested_data`: Object containing the following: 
  * `files_info`: Object containing the following: 
    * `total_files`: Integer of total number of files in the repository.
    * `ecad_files`: Integer number of electronic CAD files.
    * `mcad_files`: Integer number of mechanical CAD files.
    * `image_files`: Integer number of image files.
    * `data_files`: Integer number of data files.
    * `document_files`: Integer number of documentation files.
    * `other_files`: Integer number of other types of files.
    * `ecad_proportion`: Floating point proportion of electronic CAD files.
    * `mcad_proportion`: Floating point proportion of mechanical CAD files.
    * `image_proportion`: Floating point proportion of image files.
    * `data_proportion`: Floating point proportion of data files.
    * `document_proportion`: Floating point proportion of documentation files.
    * `other_proportion`: Floating point proportion of other types of files.
  * `license`: Object containing license information: 
    * `key`: String of license idenfifier. Currently the same as `spdx_id`.
    * `name`: Full name of license.
    * `spdx_id`: String of the SPDX license identifier.
    * `url`: URL to license text.
    * `node_id`: For some licenses, this will be an identifier in GitHub's license list.
    * `html_url`: URL to license information.
    * `permissions`: Array of strings containing the permissions given by the license, which could include: 
      * `commercial-use`: This work and derivatives may be used for commercial purposes.
      * `modifications`: This work may be modified.
      * `distribution`: This work may be distributed.
      * `private-use`: This work may be used and modified in private.
      * `patent-use`: This license provides an express grant of patent rights from contributors.
    * `conditions`: Array of strings expressing the conditions under which the work could be used, which could include a combination of: 
      * `include-copyright`: A copy of the license and copyright notice must be included with the work.
      * `include-copyright--source`: A copy of the license and copyright notice must be included with the work in when distributed in source form.
      * `document-changes`: Changes made to the source/documentation must be documented.
      * `disclose-source`: Source code/documentation must be made available when the work is distributed.
      * `network-use-disclose`: Users who interact with software via network are given the right to receive a copy of the source code.
      * `same-license`: Modifications must be released under the same license when distributing the work. In some cases a similar or related license may be used.
      * `same-license--file`: Modifications of existing files must be released under the same license when distributing the work. In some cases a similar or related license may be used.
      * `same-license--library`: Modifications must be released under the same license when distributing software. In some cases a similar or related license may be used, or this condition may not apply to works that use the software as a library.
    * `limitations`: Limitations of the license, which could include a combination of: 
      * `trademark-use`: This license explicitly states that it does NOT grant trademark rights, even though licenses without such a statement probably do not grant any implicit trademark rights.
      * `liability`: This license includes a limitation of liability.
      * `patent-use`: This license explicitly states that it does NOT grant any rights in the patents of contributors.
      * `warranty`: The license explicitly states that it does NOT provide any warranty.
  * `tags`: Aggregated array of strings representing the tags associated with the repository, and tags associated with users who are maintainers/owners of the repository. The implementation of this might change as Wikifactory implements their skill-based matchmaking features.
    * Examples: `open-source`, `raspberry-pi`, `space`, `3d-printing`
  * `commits_level`: Array of objects representing commits (contributions in Wikifactory), where each one would contain:
    * `hash`: A string, where for Git-based repositories, the unique hash identifier for the commit. For Wikifactory, this is the `id` field of the contribution.
    * `committed`: String containing the timestamp for the commmit in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, e.g. `2018-04-25T20:35:59.614973+00:00`.
  * `issues_level`: Array of objects representing issues, where each one would contain: 
    * `id`: String containing the URL to the issue.
    * `published`: String containing the creation date of the issue in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, e.g. `2018-04-25T20:35:59.614973+00:00`.
    * `isResolved`: Boolean (`true` or `false`) of whether the issue has been marked as closed or resolved.
    * `resolved`: String containing [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted timestamp representing the last time there was activity in the issue (such as comments), or if the issue `isResolved`, the time it happened.

Notes: 

* For `files_info` above, filetypes are identified by file extensions. The categories and mapping are located in [`oshminer/filetypes.py`](./oshminer/filetypes.py).
* The `license` information and formatting is largely based on that from the GitHub-managed [choosealicense.com repository](https://github.com/github/choosealicense.com), with the exception of some open source hardware licenses which were manually added.

### Custom Wikifactory URLs

By default, this tool will: 

1. Identify whether a provided repository URL in the JSON request body as a Wikifactory project if it is under the domain `wikifactory.com`
2. Use the public Wikifactory GraphQL API endpoint at `https://wikifactory.com/api/graphql`

Both can be customised with the following environmental variables: 

1. `WIF_BASE_URL` - (default: `wikifactory.com`) The base domain used for pattern-matching and identifying Wikifactory project URLs in the JSON request body in the form of `example.com`. If this is customised, then the requested Wikifactory project URLs passed to this tool should also use that domain instead of `wikifactory.com`. Otherwise, an "Repository URL domain not supported" error will be returned.
2. `WIF_API_URL` - (default: `https://wikifactory.com/api/graphql`) The full URL of the GraphQL API endpoint to make queries regarding Wikifactory projects in the form of `https://example.com[:port]/foo/bar`.

## Design notes

[to be updated]

## Maintainers

Dr Pen-Yuan Hsing ([@penyuan](https://github.com/penyuan)) is the current maintainer.

Dr Jérémy Bonvoisin ([@jbon](https://github.com/jbon)) was a previous maintainer who contributed greatly to this repository during the first year of the OPENNEXT project and is now an external advisor.

## Contributing

Thank you in advance for your contribution. Please [open an issue](https://github.com/OPEN-NEXT/wp2.2_dev/issues/new) or submit a [GitHub pull request](http://help.github.com/pull-requests/). For more details, please look at [CONTRIBUTING.md](./CONTRIBUTING.md).

This project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/) Code of Conduct 2.0.

## Acknowledgements

The maintainer would like to gratefully acknowledge:

* Dr Jérémy Bonvoisin ([@jbon](https://github.com/jbon)) not only for the initial contributions to this work, but also for continued practical and theoretical insight, generosity, and guidance.
* Dr Elies Dekoninck ([@elies30](https://github.com/orgs/OPEN-NEXT/people/elies30)) and Rafaella Antoniou ([@rafaellaantoniou](https://github.com/orgs/OPEN-NEXT/people/rafaellaantoniou)) for valuable feedback and support.
* Max Kampik ([@mkampik](https://github.com/mkampik)), Diego Vaquero, and Andrés Barreiro from Wikifactory for close collaboration, design insights, and technical support throughout the project.
* OPENNEXT internal reviewers Dr Jean-François Boujut ([@boujut](https://github.com/boujut)) and Martin Häuer ([@moedn](https://github.com/moedn)) for constructive criticism.
* OPENNEXT project researchers Robert Mies ([@MIE5R0](https://github.com/MIE5R0)), Mehera Hassan ([@meherrahassan](https://github.com/meherahassan)), and Sonika Gogineni ([@GoSFhg](https://github.com/GoSFhg)) for useful feedback and extensive administrative support.
* The Linux Foundation [CHAOSS](https://chaoss.community/) group for insights on open source community health metrics.

[![EU flag](./docs/images/EU_flag.svg)](https://commons.wikimedia.org/wiki/File:Flag_of_Europe.svg)

The work in this repository is supported by a European Union [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) programme grant (agreement ID [869984](https://cordis.europa.eu/project/id/869984)).

## License

[![GitHub AGPL-3.0-or-later license](https://img.shields.io/github/license/OPEN-NEXT/wp2.2_dev)](./LICENSE)

The Python code in this repository is licensed under the [GNU AGPLv3 or any later version](./LICENSE) © 2022 Pen-Yuan Hsing

[![CC BY-SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

This README is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International license (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) © 2022 Pen-Yuan Hsing

Details on other files are in the REUSE specification [dep5](./.reuse/dep5) file.