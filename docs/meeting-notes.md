
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

