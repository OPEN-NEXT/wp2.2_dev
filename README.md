# OSD status dashboard _(wp2.2_dev)_

[![Live demo link](https://img.shields.io/badge/Demo-CLICK%20HERE-red.svg?style=flat)](https://psaltyi.pythonanywhere.com/)
[![Python version](https://img.shields.io/badge/Python-3.8-blue.svg?style=flat)](https://www.python.org/)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat)](https://github.com/RichardLitt/standard-readme)
[![REUSE compliance status](https://api.reuse.software/badge/github.com/OPEN-NEXT/wp2.2_dev)](https://api.reuse.software/info/github.com/OPEN-NEXT/wp2.2_dev)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](./CODE_OF_CONDUCT.md)
[![GitHub license](https://img.shields.io/github/license/OPEN-NEXT/wp2.2_dev.svg?style=flat)](./LICENSE)

*Initial proof-of-concept of open source development status dashboard with data-mining & visualisation components*

This repository contains a set of Python scripts and associated files to host a prototype data visualisation dashboard for open source development projects. It is composed of (a) a data-mining Python module (`osmine`) which retrieves publicly-viewable metadata from a user-supplied list of open source version control repositories; and (b) an interactive [Dash](https://dash.plotly.com/)-based web module (`osdash`) that computes and visualises basic metrics on those repositories. Please see [Install](#install) and [Usage](#usage) to get up and running with this tool. Click [**here**](https://psaltyi.pythonanywhere.com/) to access a demo instance of the prototype dashboard.

This work is an *initial* demonstrator delivered at month 18 of the [OPENNEXT](https://opennext.eu/) project as part of task 2.2: "Creating a design process facilitation dashboard". It is to establish the foundational infrastructure on which the ambition to facilitate company-community collaboration on open source hardware projects described [below](#background) can be pursued. Future iterations of this tool should allow the community developing an open source hardware product to track the the health of their project and if their needs are being met.

## Table of Contents

- [OSD status dashboard _(wp2.2_dev)_](#osd-status-dashboard-wp22_dev)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
    - [`osmine` data-mining module](#osmine-data-mining-module)
    - [`osdash` dashboard module](#osdash-dashboard-module)
      - [Running the test server](#running-the-test-server)
      - [User interface of the prototype dashboard](#user-interface-of-the-prototype-dashboard)
  - [Design notes](#design-notes)
    - [Sequence of execution](#sequence-of-execution)
    - [Data-mining considerations](#data-mining-considerations)
    - [Data visualisation considerations](#data-visualisation-considerations)
  - [Future work](#future-work)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [Acknowledgements](#acknowledgements)
  - [License](#license)

## Background

> Today’s industrial product creation is expensive, risky and unsustainable. At the same time, the process is highly inaccessible to consumers who have very little input in the design and distribution of the finished product. Presently, SMEs and maker communities across Europe are coming together to fundamentally change the way we create, produce, and distribute products.

[OPENNEXT](https://opennext.eu/) is a collaboration between 19 industry and academic partners across Europe. Funded by the European Union's Horizon 2020 programme, this project seeks to enable small and medium enterprises (SMEs) to work with consumers, makers, and other commnities in rethinking how products are designed and produced. [Open source hardware](https://www.oshwa.org/definition/) is a key enabler of this goal where the design of a physical product is released with the permission for anyone to study, modify, share, and redistribute it. These essential freedoms are based on those of [open source software](https://opensource.org/osd), which is itself derived from [free software](https://www.gnu.org/philosophy/free-sw.en.html) where the word free refers to freedom, *not* free-of-charge. When put in practice, these freedoms could potentially not only reduce planned obsolescence, waste, or proprietary vendor lock-in, but also stimulate novel – even disruptive – business models. The SME partners in OPENNEXT are experimenting with producing open source hardware and even opening up the development process to wider community participation. They produce diverse products range from [desks](https://stykka.com/), [cargo bike modules](http://www.xyzcargo.com/), to a [digital scientific instrument platform](https://pslab.io/) (and [more](https://opennext.eu/project-team/#sme)).

Work package 2 of OPENNEXT is gathering theoretical and practical insights on best practices for company-community colloration when developing open source hardware. This includes running Delphi studies to develop a maturity model to describe the collaboration or developing a precise definition for what the "source" in open source hardware. In particular, task 2.2 in this work package is developing a project status dashboard with "health" indicators showing the evolution of a project within the maturity model; design activities; or progress towards success based on project goals.

To that end, the month 18 deliverable for task 2.2 is focused on developing the underlying infrastructure to mine metadata from version control repositories that open source hardware projects are hosted on (`osmine`). The Python scripts in this repository currently query the public application programming interfaces (APIs) of GitHub and Wikifactory. There is also a user-facing demonstration dashboard (`osdash`) which computes core metrics from the the mined data and present interactive visualisations. Currently, post-month-18 development is envisaged to include, but not limited to: 

* Modules to query other platforms such as GitLab or generic Git repositories;
* Logging
* Network visualisations of file co-edition histories and participation in tickets (e.g. GitHub Issues) with cluster analyses
* Compute indicators for the dashboard derived from the company-community collaboration community model under development
* Validate with OPENNEXT SME partners

This documentation aims to demonstrate practices that facilitate design reuse, including of this repository. In addition to the [Install](#install) and [Usage](#usage) sections that increase reproducibility, [Design notes](#design-notes) and [Future work](#future-work) communicate the thought process and lessons-learned while developing the dashboard. Together, they constitute an intangible body of "know-how" that is very often undocumented. In addition, this repository aims to follow international standards and good practices in open source development such as: 

* SDPX compliance with a [LICENSE](./LICENSE) file (also see [License](#license) section)
* REUSE compliance with appropriate machine-readable SPDX metadata for all files
* README file conforming to the [Standard Readme specification](https://github.com/RichardLitt/standard-readme)
* Contributor Covenant Code of Conduct
* [CONTRIBUTING](./CONTRIBUTING.md) document outlining ways to contribute to this repository

## Install

*This section assumes basic knowledge of Python and using a terminal session in a GNU/Linux operating system*.

This project requires [Python](https://www.python.org/) 3.8 or later and setting up a Pyenv virtual environment is optional but recommended. Detailed dependencies are listed in the standard [`requirements.txt`](./requirements.txt): 

* `dash>=1.16.0`
* `dash-bootstrap-components>=0.11.1`
* `numpy~=1.17.3`
* `pandas~=0.25.2`
* `plotly>=4.10.0`
* `PyYAML~=5.1.2`
* `requests~=2.22.0`

A [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) is required because the Python scripts will use it for GitHub API queries. Future versions may make this optional if none of the repositories for the data-miner and dashboard to work on are hosted on GitHub.

Currently, the code is set up to be run from source and has been tested on updated versions of GNU/Linux operating systems including [Red Hat Enterprise Linux](https://redhat.com/en/technologies/linux-platforms/enterprise-linux) 8.3 and [Debian](https://www.debian.org/) 10. With the tools [`git`](https://git-scm.com/) and [`pip`](https://pip.pypa.io/) installed, the following commands will retrieve the latest version of this repository and prepare it for development and running locally (usually for testing): 

```sh
git clone https://github.com/OPEN-NEXT/wp2.2_dev.git
pip install -r requirements.txt
```

For production, one could host the code on a Web Server Gateway Interface (WSGI) server such as [Pythonanywhere](https://eu.pythonanywhere.com/) (where [the demo instance](https://psaltyi.pythonanywhere.com/) is hosted). To do so, please follow the instructions [here](https://csyhuang.github.io/2018/06/24/set-up-dash-app-on-pythonanywhere/) where `from dashing_demo_app import app` would be replaced by `from osdash import app`.

## Usage

*This section assumes basic knowledge of Python and using a terminal session in a GNU/Linux operating system*.

### `osmine` data-mining module

Command line arguments.

Github API personal access token file:

* A two-line file with any name, but placed besides `start.py`.
* First line is username
* Second line is the token string

Configuration file.

Mined data will be in `data`. It *could* be viewed by extracting it from the zip file.

### `osdash` dashboard module

The `osmine` data-mining module must first be run at least once so that there is data for the dashboard to visualise.

#### Running the test server

The test server can be accessed in a web browser at 127.0.0.1:[`port`] where `port` can be specified in the function app.serve() in `osdash\__main__.py`.

#### User interface of the prototype dashboard

Explain UI usage.

Can be embedded in other pages with `iframe`s.

## Design notes

### Sequence of execution

The data-mining module `osmine` is always expected to be run first to produce a dataset for the user-facing dashboard `osdash` to visualise. The following is the general order of events after running the command `python osmine`: 

1. Configuration options (see [Usage](#usage)) are read by the script `prepreprocess.read_config.py` to parameterise the behaviour of `osmine`.
2. A comma separated values (CSV) formatted list of version control repositories is read 

The following is a high-level diagram of the dashboard with its main data-mining backend (`osmine`) and user-facing Dash visualisation frontend (`osdash`).

![Dashboard architecture diagram](./docs/images/architecture.drawio.svg)

```
.
├── config.yaml
├── data
│   └── mined_data.zip
├── docs
├── input
│   └── OSH-repos.csv
├── LICENSE
├── osdash
│   ├── __init__.py
│   ├── __main__.py
│   ├── dash_app.py
│   ├── assets
│   │   └── css
│   │       └── bootstrap.min.css
│   └── preprocess
│       ├── __init__.py
│       ├── stage_data.py
│       └── wrangle_data.py
├── osmine
│   ├── __main__.py
│   ├── miner
│   │   ├── GitHub.py
│   │   ├── __init__.py
│   │   ├── mine.py
│   │   └── Wikifactory.py
│   ├── postprocess
│   │   ├── exporter.py
│   │   └── __init__.py
│   └── preprocess
│       ├── __init__.py
│       ├── past_data.py
│       ├── read_config.py
│       ├── read_mining_list.py
│       └── stage_data.py
├── README.md
└── requirements.txt
```

### Data-mining considerations

Users requests library for API calls to prevent cloning Git repository locally. For Wikifactory there isn't anything other than the API anyway.

[brief history investigating how to do this and settling on just using requests library and Dash for visualisations]

GitHub v3 vs v4 API thoughts.

Uses DEFLATE algorithm as implemented by the `zipfile` module in Python 3.8 set to compression level 9.

### Data visualisation considerations

## Future work

Connect with Wikibase or whatever it ends up being.

Need file change histories for repositories, looks like we will need to download at least partial Git repos to get this with libraries like pydriller.

Ideas for constructing file, ticket, and file/ticket networks to look at product and community architecture.

Based on file metadata, derive the skills that have been used in a repository (hardware design e.g. use of OpenSCAD, programming with Python (or even more specific like Python frontend development with Flask?)), and allow repositories to express what skills they are looking for, so something in the dashboard like: "Skills used", "Skills wanted", etc.

Badges for the above?

Better connect with SMEs who are going through the user journey.

On technical side, proper logging and testing would be ideal but challenging. At least try to support generic Git repositories.

If resources permit, unit testing will be incorporated into all Python code.

Improve documentation through extensive code comments and reaching level four or five in the [README Maturity Model](https://github.com/LappleApple/feedmereadmes/blob/master/README-maturity-model.md#level-five-product-oriented-readme).

## Maintainers

[@penyuan](https://github.com/penyuan)

@jbon is past maintainer who has contributed greatly during the first year of the project.

## Contributing

[Open an issue](https://github.com/OPEN-NEXT/wp2.2_dev/issues/new) or submit a GitHub Pull Request.

This project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/) Code of Conduct 2.0.

## Acknowledgements

Elies and Rafaella at UBA.

Max and Andres from Wikifactory.

OPENNEXT internal reviewers: JF and @moedn.

Rober, Mehera, and Sonika for useful feedback and admin support.

Useful discussions at CHAOSS con 2020 and the people there.

@jbon for continued practical and theoretical insight.
Funders: EU H2020 grant numbers.

## License

[![GitHub license](https://img.shields.io/github/license/OPEN-NEXT/wp2.2_dev)](./LICENSE)

[GNU AGPLv3 or later](./LICENSE) © 2021 Pen-Yuan Hsing