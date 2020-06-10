# Notes on existing OSH literature

This document is to collate notes on relevant open source hardware (OSH) literature, such as academic papers.

## Design structure matrices (DSM)

### Automatic design structure matrices: A comparison of two formula student projects

Citation:

Gopsill, J. A., Snider, C. M., Emmanuel, L., Joel-Edgar, S., & Hick, B. J. (2017). Automatic design structure matrices: A comparison of two formula student projects. 6. https://jamesgopsill.github.io/Publications/papers/conference/2017-iced/2017-iced.pdf
Gopsill, J. A., Snider, C. M., & Hicks, B. J. (2019). The emergent structures within digital engineering work: What can we learn from dynamic DSMs of near-identical systems design projects? Design Science, 31.


Notes:

* In practice, design structure matrices (DSMs) allow the strength of relationships between elements of an engineering design to be visualised in a matrix.
* Gopsill et al. applied a DSM to the evolution of two parallel efforts to design Formula Student racecars where computer-aided design (CAD) file changes are tracked. Here:
  * Elements in the DSM are CAD files.
  * Strength of connection are - generally speaking - how often a group of files are edited in close temporal proximity. E.g. if file B is always edited soon after changes to file A, that forms a strong directional connection.
* The *evolution* of projects can be examined by tracking DSM metrics such as its modularity, number of partitions, etc.
* **What it means for us:** We can apply this idea to the GitHub repositories we are mining, where e.g. files edited within the same commit count towards the strength of connections in a DSM.
  * In this case, files would be edited "simultaneously" in the same commit, so there's no directionality.
  * We need to consider whether there are enough files in a repository to form a meaningful DSM for a project.