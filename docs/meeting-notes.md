
# Minutes 2020-07-24

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

# Minutes 2020-07-31

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

# Inter-WP meeting notes 2020-08-12

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

# Preparation notes 2020/08/21

Agenda:
 - look at the [new mockup](mockups/M18.svg) and decide on a list of features for M18
 - review to-do-s from last meeting
 - discuss the propositions below
 - AOB

Process of selecting features for mockup M18:
  - converted relevance rankings high, medium, low into 3, 2, 1. 
  - computed relevance ranking (averaged ranking from WIF and UBA with 1:1 weighing)
  - computed an overall ranking relevance * easiness to implement
  - filtered all features ranked >= 6

Propositions to discuss:
- Involvement of WIF for M18 deliverable: implement the prototype in their platform already, so they frontload the efforts they will have to do later to implement the software developed by UoB and will have more chances to participate and give feedback.
- From now on, PYH takes over the responsibility of organizing the weekly meetings with WIF, including keeping trace of the decisions and leading the agenda and discussions.
- 
# Meeting notes 2020/08/21

Process of agreeing on the features to be implemented for M18:
- We had a look at the [new mockup](mockups/M18.svg) resulting from the feature selection process described in the preparation notes above
- Features were discussed one by one. Some features were eventually amended and some other related features added as "nice to have"
  - For example, nice to haves include a view of how metrics change over time, graph visualisation, or metrics based on Sonika and Wikifactory's discussions outlined below in "Inter-WP meeting notes 2020-08-21T13:00+02:00" below.
- We had a veto round where each of us could remove a feature that finally seems not so relevant. We removed the component showing number of CAD files in the repository, because it is not so useful on its own, and can be incorporated into the language bar.
- We had a look at features which were on the edge of the arbitrary selection threshold. Each of us had the possibility to reintegrate these borderline features in the dashboard.

Final agreement:
- We agree on the dashboard features as described in [new mockup](mockups/M18.svg) as of commit 3b25c3c and in [the list of selected features for M18](mockups/selectedFeaturesM18.csv)
- We agree that what we deliver in M18 is a functional dashboard prototype implemented in WIF.

Remaining action items from last meeting: 
- MK asks community team at WIF for a list of a few projects that represent differnt types of projects, so UBA has a few reference data to play with the GraphQL API

# Inter-WP meeting notes 2020-08-21T13:00+02:00

With Sonika, @jbon, and @penyuan.

Today Sonika talked about their discussions with Wikifactory. They are planning to work on four main things:

* Community management - It is hard to find and attract collaborators and motivate them to contribute.
    * Develop skill based ontology in Wikibase (which will be open source) for matching contributors to projects, will be implemented by Wikifactory
    * Wikifactory can already consider a new contributor's interests in matching with tags e.g. Arduino, robotics, etc.
* Documentation and guidelines for product development
    * Will work with Grenoble people to develop good practices as part of those guidelines
    * Wikifactory has template for new projects, so maybe add documentation and development guidelines to those templates
    * With these guidelines, make projects aware of open source tools during PLM process
* Interoperability
    * It is currently hard to work with other platforms like GitLab, GitHub or Google Drive
    * So we want to develop import/export tools to aid interoperability
    * @penyuan: I suggest making these tools independent/stand-alone
* Collaborative production engineering & manufacturing
    * Develop a Manufacturer List with archetypes, capabilities, and location so that open source hardware developers can be referred to them
    * Product Metadata Information (like tolerances, material, etc.) in CAD files will be used to recommend manufacturers
* @moe is developing Wikibase ontology based on Open Know How and preparing to set up the instance
* Sonika: We came up with 15 points to work on based on most mentioned issues from user stories
* @penyuan: We are meeting with Wikifactory today, and will try to narrow down which features we want to implement for the first dashboard draft.
    * Once we have this draft, we will circulate it among Sonika and Moe for feedback.

# Dashboard meeting 2020-09-04T11:00+02:00

With Elies, @mkampik, and @penyuan

* @jbon couldn't make it today
* Update on month-18 (M18) dashboard
    * The rationales for the design are:
        * Features prioritised (a combination of user-need and technical low-hanging fruits) by @jbon, @mkampik, @rafaellaantoniou, and @penyuan
            * Spreadsheet of feature selection process can be seen [here](https://github.com/OPEN-NEXT/wp2.2_dev/tree/docs/docs/mockups)
        * They tie at least partially into needs identified from Sonika's user stories
        * They can be built as a demonstrator tied into Wikifactory project
* As for finding representative projects on Wikifactory, @mkampik suggested that we use the Wikifactory [Discover page](https://wikifactory.com/discover) to filter for projects with many contributions. In particular, [Project CAROLA](http://viralresponse.io/+carola/project-carola-alpha) is likely the most decentralised one where 12 contributors have made contributions (in contrast with centralised projects with only 1-2 contributors). The rest can come from the Wikifactory API.
* We discussed the challenges around version control when dealing with large binary files such as CAD files.
    * This is one reason Wikifactory didn't just use git
    * Instead, Wikifactory adds an abstraction around the binary files such as a tree history of file changes, but you don't pull the actual files all the time when handling the data/metadata (Wikifactory still keeps all versions of binary files)
    * There is a system called Git-LFS designed to solve the problem of version-controlling large files, but so far it seems to be mainly used for handling large data science datasets, and the barrier to adoption seems to be bandwidth costs. @mkampik found [this relevant article](https://medium.com/@megastep/github-s-large-file-storage-is-no-panacea-for-open-source-quite-the-opposite-12c0e16a9a91).
* Summary of previous meeting with Sonika, i.e. the four things they derived from user stories:
    * Community management - i.e. contributor attraction, retention, and motivation
        * It's focused on defining an open source hardware skills ontology in Wikibase to aid skill-based matching on Wikifactory
        * Both Elies and @penyuan mentioned that a contributor is often more motivated by the topic of the project rather than matching skills
    * Documentation and guidelines for new projects
        * Wikifactory will develop new templates for new projects at different stages with appropriate guides
        * The folks are Grenoble are involved since their research focus is on design re-use
    * Interoperability
        * To overcome vendor lock-in of proprietary platforms such as GitHub, Google Docs, etc.
        * Wikifactory will help implement a modular solution beginning with file import/export, and eventually issues and user mapping, and ideally sync and mirror functions
    * Collaborative production engineering & manufacturing
        * Implement in Wikibase a list of willing and able fablabs and manufacturers along with their capabilities and locations so they can be suggested to projects on e.g. Wikifactory

Next meeting(s):

* @penyuan is setting up a meeting with @moedn and Sonika to look at technical aspects of hooking dashboard up to the Wikibase instance
* Between Elies, @mkampik, @jbon, and @penyuan: 2020-09-18 at 09:00 BST/10:00 CEST
* With Elies, @jbon, and @penyuan: 2020-09-11 afternoon (@penyuan will find a time)