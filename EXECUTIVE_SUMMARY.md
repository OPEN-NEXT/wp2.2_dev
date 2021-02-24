# Executive summary

The work presented here is an *initial* demonstrator delivered at month 18 of the [OPENNEXT](https://opennext.eu/) project as part of task 2.2: "Creating a design process facilitation dashboard" (deliverable number 2.3). This work is part of work package 2, and is the primary responsiblity of the OPENNEXT academic partner at the University of Bath (UBA) in the United Kingdom. It is to establish the foundational infrastructure on which the ambition to facilitate company-community collaboration on open source hardware projects can be pursued.

To that end, this deliverable contains two primary components: 

1. A [Git](https://git-scm.com/) version control repository containing 15,000 lines of Python scripts: https://www.github.com/OPEN-NEXT/wp2.2_dev/ This source code is composed of (a) a data-mining Python module (`osmine`) which mines publicly-viewable metadata from a user-supplied list of open source [version control](https://en.wikipedia.org/wiki/Version_control) repositories; and (b) an interactive [Dash](https://dash.plotly.com/)-based web module (`osdash`) that computes and visualises basic metrics on those repositories. For the purposes of OPENNEXT, the list of open source repositories would eventually be those in use by the OPENNEXT small and medium enterprises (SMEs) partners for their open source hardware development work.

2. A live demo instance of `osdash` which can be visited here: https://opennextwp22.eu.pythonanywhere.com/ This illustrates basic elements of interactive data visualisations based on data retrieved from the version control repositories of open source projects. It is meant to serve as a base for what future visualisations of data analyses on open source project health metrics.

The primary results of this deliverable are that: 

* The Python codebase is functionally complete providing the capabilities described above. Notably, it adheres to several international standards and best practices on open source software development including, but not limited to: the [Software Package Data Exchange](https://spdx.dev/) (SPDX) format; [REUSE standard](https://reuse.software/) for open source licensing; using a README file as the primary documentation that follows the [Standard Readme Specification](https://github.com/RichardLitt/standard-readme); and the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct for participants.
* The live demo shows examples of how project metadata can be visualised, which will serve as the basis for collaboration with and getting input from SME partners on what metrics on project health would be most helpful for their open source hardware efforts.

With this foundation, we hope to: 

* Investigate community collaboration patterns in open source development by analysing the file-change histories of their version control repositories.
* Work with other work packages and SME partners to identify project health metrics and assess which ones are suitable for an interactive dashboard based on quantitative data.
* Continue technical improvements to the underlying Python code.

For review purposes, please note the primary documentation for this deliverable - with more detailed and thorough descriptions of its background, design, installation, and usage - is the industry-standard README file contained in its Git repository, which can be viewed here: https://www.github.com/OPEN-NEXT/wp2.2_dev/