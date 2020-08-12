
# 2020-07-24

## Feature selection processing
- each of us four (Max, Pen, Rafaella and Jérémy) assess the relevance of each features in the "wish list" (dashboard features list) prior to next Wednesday. 
- Jérémy sends a mail in short to explain how to do this.
- UBA and WI have one voice each. That is, Rafaella's, Pen's and Jérémy's inputs will be averaged.
- each of us can freely add new features if relevant. The wish list is a "live document".
- next week we finalise the priorisation and "slice" the wish list and decide what goes in the M18 deliverable.
- Jérémy clarifies in the meantime when M18 actually is. 

## Organisation

We agreed on weekly meetings from now on, Fridays at 10 UK time. We did not discuss the length but I suggest 1.5h. Meeting frequency may be amended/reduced once we entered development, at best in combination with some other communication channel (e.g. element).

Share of responsibilities between WIF and UBA:
- WIF cares about visualisation and rendering on the WIF platform
- UBA delivers:
    - to WIF and the world an open source data processing module 
    - to the world some sort of visualisation and rendering that is hopefully looking like WIF's visualisation because we will aim to we use the same technologies as WIF

Misc:
- WIF has 7 developer and 2 manager months booked in for WP2, mostly for WP2.2
- Max in vacation after next week for two weeks

## Technologies

WIF uses the following technologies:
- [Flask](https://www.fullstackpython.com/flask.html) backend to build project features
- [postgres](https://www.postgresql.org/) and [Dgraph](https://dgraph.io/) databases (but this may not be relevant since we have the GraphQL API)
- [react](https://fr.reactjs.org/) for UI rendering
- [MobX](https://mobx.js.org/README.html) for state management 
- generally: python/javascript 

Architecture decision to take: will the data processing module happen through
- a fairly contained python module/lib
- a server?

Developing a python module/library would make more sense because:
- UBA does not have the funds to maintain a server indefinitely
- it would create a dependency for WIF
- it is more interesting for UBA to develop an open source contained module

However the decision should be discussed at WIF internally. Decision on technologies are generally pending. The wish list needs to be refined first.

# 2020-07-31

We had a look at the assessment of the feature's relevance and decided on the following:
- We implement a base of low hanging fruits for the M18 deadline. M18 is Feb 28th but due to the internal review process in OpenNext, a pre-release should be planned for Jan 31st.
- A second wave of development will be dedicated to original features. The expert system-like features seemed to be more original than the graph-like ones, but are also more risky. 

Consequently, until M18, we dedicate:
- approx. 80% of our time in the development of the M18 release
- approx. 20% refining concepts of original features, their feasibiltiy and getting a better idea of user requirements

To-do's for mext meeting:
- Based on the assesment of features relatively to relevance and developent effort, JB develops a new dashboard design mockup
- MK asks community team at WIF for a list of a few projects that represent differnt types of projects, so UBA has a few reference data to play with the GraphQL API

About software architecture:
- we go for an open source package, not for a separated server. 
- consequently, we will need interface requirements from WIF at some point. This is pending for now, the time for the M18 mockup to be agreed upon.

# 2020-08-12

At 11:00 CEST with Sonika, @jbon, @moedn, and @penyuan.

For this meeting, work package (WP) 2.2 gave a summary of progress on dashboard development followed by discussions about how our respective WPs can inform each other's efforts.

* @jbon's summary of dashboard mock ups
    * We're getting lots of data from OSH projects, it is a pity not to make use of it
    * We doing this as an opportunistic technology push, i.e.:
        * In parallel to other WPs asking what practitioners want, we are creating a demonstration of what we *can* do in the form of an interactive dashboard
        * This is inspired by the Ford Motors saying "if you ask people what they want, they'll tell you they want a faster horse",  i.e. there's value is just doing things sometimes
    * @penyuan and @rafaellaantoniou have been looking at existing communities (such as [CHAOSS](https://chaoss.community/)) to see what metrics we might use    
    * Summary of ["low hanging fruit" mockup](https://github.com/OPEN-NEXT/wp2.2_dev/blob/docs/docs/mockups/low_hanging_fruits.svg)
        * This shows quantifiable metrics that we often see implemented on other platform such as GitHub
        * Already kind of useful to get a sense of which programming languages or CAD software are used by a project and the intensity of their activities
    * Mentioned achievement badges -> Which can include things like # of commits, number of contributors, etc.
    * Network visualisation ("mid-hanging fruit") mockup
        * Community graph/network of participants, which you can compute metrics like centrality or modularity of the team or the bus/elephant factor
        * Idea of core-mutant-external contributors
            * Core are the main and direct contributors to the repository
            * Mutant are contributions from forks
            * External are other people submitting contributions
        * A more advanced thing is replay button for you to watch how the network changes over time
    * Archetypes ("high-hanging fruit")
        * Define project archetypes
            * Highest activity
            * Few committers
            * etc.
            * The challenge is how do we define project archetypes and which metrics inform them?
    * We've wrapped the above into [the spreadsheet](https://github.com/OPEN-NEXT/wp2.2_dev/blob/docs/docs/mockups/Dashboard_Features.csv) to prioritise which ones we want to work on more for first month-18 deliverable in 2020-02 and what comes after
* Sonika had a couple questions:
    * Are you developing the code right now?
        * @jbon Yes, and we want something other people can take and use
    * What about programming language/tools?
        * JB: We'll try to make something suitable for WF, and since Python is almost everywhere so hopefully easier for others to adapt and adopt. Right now we're more focused on the data-mining and data analyses backend.
* @moedn:
    * I think this should connect well to results from project Open!
    * Maybe integrate into the Wikibase instance?
        * The Wikibase instance is being set up right now, will probably end up being hosted by Open Source Ecology Germany
        * We'll need what data you can provide and questions you want to answer (e.g. how active the project is, is documentation complete, which data formats are used, what software I need, Sonika: e.g. what queries you make of the data) to help be design ontology of the Wikibase instance
            * @jbon: As an example, we could give you a list of file types per repo and number of each file
    * Also talked about crawlers for a bit
        * @moedn's group might have resources to develop one, but what would it actually crawl for?
            * File type and/or license to identity an open source hardware project? Both can be challenging
        * Or have the crawler look for manifest files, which also implies that a project wants to be found
        * @jbon: Of course there's the risk at the DIN SPEC effort might fail
* Would be good to hear from Sonika too at next meeting so let's plan that, @penyuan will email everyone (let me know if I missed someone!)
