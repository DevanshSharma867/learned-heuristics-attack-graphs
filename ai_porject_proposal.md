| Learned |                | Heuristics   | for A*     | Search       | over      | Attack     | Graphs: |
| ------- | -------------- | ------------ | ---------- | ------------ | --------- | ---------- | ------- |
|         | Generalization |              | to Unseen  |              | Network   | Topologies |         |
|         |                | CS F407/U407 | Artificial | Intelligence | — Project | Proposal   |         |
Overview
Project name LearnedHeuristicsforASearchoverAttackGraphs: GeneralizationtoUnseen
|       |         | Network  | Topologies |               |     |     |     |
| ----- | ------- | -------- | ---------- | ------------- | --- | --- | --- |
| Team  | name    | Devansh  |            |               |     |     |     |
| Team  | members | Devansh  | Sharma ID: | 2022A3PS1298H |     |     |     |
| Track |         | Research |            |               |     |     |     |
Topic area Search & Problem Solving, combined with Applications of Deep Learning
GitHub repository https://github.com/DevanshSharma867/learned-heuristics-attack-graphs
Short project description. This project investigates whether a neural network trained to estimate
cost-to-goal can guide A* search over vulnerability-derived attack graphs better than classical A*
heuristics. Attackgraphsarebuiltfromsyntheticenterprisenetworktopologies, withrealCVE/CVSS
attributes providing exploit-cost features. The learned heuristic is trained on one set of topologies and
then evaluated across the full range of test conditions: held-out graphs from the training distribution,
pluslargernetworks, structurallydifferentnetworks, andnetworkswithdifferentvulnerabilityprofiles.
Graphs used for training or tuning are never used to support a claim. It is compared head-to-head
against classical baselines (A* with standard hand-crafted heuristics, i.e. “normal A*”, and uniform-
cost search) on search effort (nodes expanded, run time) and solution quality (plan cost relative to
the optimum).
1

| 1   | Problem |     | Statement |     | and | Motivation |     |     |     |
| --- | ------- | --- | --------- | --- | --- | ---------- | --- | --- | --- |
Attack-graph analysis is a defensive technique: given a network and its known vulnerabilities, it
finds the exploit sequences an attacker could use to reach a critical asset, so that defenders can fix the
weakestroutesfirst. Findingtheexploitsequenceofminimumcostunderadefinedattack-effortmodel
is a search problem and is the core computation behind simulated penetration testing [4]. On small
networks an exact solver suffices; on large networks the state space grows combinatorially, and the
heuristic guiding A* [1] largely determines whether the search finishes. Faster analysis lets defenders
| re-run | it  | more | often as | networks | and | patches change. |     |     |     |
| ------ | --- | ---- | -------- | -------- | --- | --------------- | --- | --- | --- |
Hand-crafted heuristics, derived from relaxed versions of the problem, are domain-agnostic and often
weakly informed. In other search domains, a network trained to estimate cost-to-goal has been used
to guide A*-style search [6, 7]. This project focuses on whether such a learned heuristic generalizes
across unseen attack-graph topologies; how much this specific question has already been studied in
attack-graph planning will be established by the initial literature review (Week 1).
Research question. Compared with normal A* using classical heuristics, can a neural cost-to-go
estimator trained on some attack graphs reduce search effort on attack graphs from unseen network
| topologies, |     | and | how much | solution | quality | does it | cost? |     |     |
| ----------- | --- | --- | -------- | -------- | ------- | ------- | ----- | --- | --- |
Hypotheses.
• H1 (efficiency): on unseen test graphs from the training distribution, A* with the learned
heuristic expands fewer nodes than A* with the hand-crafted baselines.
• H2 (efficiency–quality trade-off): the learned heuristic reduces search effort at the cost of
measurable suboptimality relative to admissible classical heuristics, which return optimal plans.
•
H3 (generalization): the learned heuristic’s efficiency advantage decreases under distribution
shifts in graph size, topology structure, and vulnerability features; the experiments measure the
|     | magnitude |     | of each | effect | separately. |     |     |     |     |
| --- | --------- | --- | ------- | ------ | ----------- | --- | --- | --- | --- |
Scope. Core: GNN heuristic, A* with classical baselines, and the generalization study. Secondary:
MLP ablation. Optional: weighted A*, asymmetric-loss comparison, MulVAL validation. If the
| schedule |        | slips, | the core | alone | is a complete | result.    |     |     |     |
| -------- | ------ | ------ | -------- | ----- | ------------- | ---------- | --- | --- | --- |
| 2        | Course |        | Concepts |       | and           | Techniques |     |     |     |
•
A* search (f = g+h), admissibility and consistency; uniform-cost search/Dijkstra (h ≡ 0)
|     | as  | the uninformed |     | baseline. |     |     |     |     |     |
| --- | --- | -------------- | --- | --------- | --- | --- | --- | --- | --- |
• Heuristics from relaxed problems: delete-relaxation heuristics h (admissible) and h
max add
|     | (informative, |     | inadmissible), |     | and | a shortest-path | relaxation | h . |     |
| --- | ------------- | --- | -------------- | --- | --- | --------------- | ---------- | --- | --- |
sp
•
Deep learning for regression: a message-passing graph neural network (GNN), trained with
supervised learning to predict optimal cost-to-go; an MLP on hand-built features as ablation.
• Weighted A* (f = g+w·h), as a secondary empirical tool only.
| 3   | Proposed |     | Approach |     | and | Methodology |     |     |     |
| --- | -------- | --- | -------- | --- | --- | ----------- | --- | --- | --- |
3.1 Pipeline
|     |     |     | Synthetic | Service/CVE |     | MulVAL              |           | Fact–action  | Search-state |
| --- | --- | --- | --------- | ----------- | --- | ------------------- | --------- | ------------ | ------------ |
|     |     |     | network   | assignment  |     | (ornativegenerator) |           | attackgraph  | generator    |
|     |     |     |           |             |     | ClassicalA*         |           | GNN-guidedA* | Evaluationon |
|     |     |     |           |             |     | (h0,hmax,h          | add ,hsp) | (h θ )       | unseengraphs |
2

3.2 Data: synthetic topologies with CVE-derived vulnerability features
Topologies (hosts, services, reachability/firewall rules, trust relationships) are generated synthetically
at varying sizes from several generator families (e.g. flat, tiered/segmented, hub-and-spoke). Each
service is assigned a service family, and CVEs are sampled from NVD [8] records matching that family
(by product/CPE); their CVSS attributes [9] become the vulnerability features. This gives enough
graphs of controlled size and structure for clean train/test splits and a reproducible pipeline, with
vulnerability features grounded in real CVSS exploitability attributes. Attack graphs are produced
with MulVAL [3], a Datalog-based generator that derives them from a network configuration and
vulnerability data. If MulVAL is not operational by the end of Week 2, I will use a native generator
that implements the same fact–action representation directly, and MulVAL becomes optional external
validation.
Cost model. CVSS does not give a calibrated probability of exploit success, so exploit cost is a
synthetic attack-effort proxy built from CVSS exploitability attributes: higher exploitability means
lower cost (e.g. c(a) = 1+9(1−x ), with x ∈ [0,1] the normalized CVSS exploitability sub-score).
a a
It is not a calibrated probability. The mapping is fixed and documented before the main experiments,
and all “optimal” results are optimal under this model.
3.3 Search formulation
Becauseanexploitmayrequireseveralprerequisiteprivilegesatonce, theattackgraphisafact–action
graph with conjunctive action preconditions, so search runs over the induced state space and not over
individual graph edges. A state is the set of privileges the attacker holds; an action is an exploit
whose preconditions hold in the state and which adds privileges; the goal is a target privilege. Under
this abstraction privileges are monotonic and never removed, giving a delete-free planning problem,
so delete-relaxation heuristics apply; optimal delete-free planning is nonetheless NP-hard in general.
Evaluation instances have a reachable target by construction; any unexpectedly unreachable instance
is logged separately as a generation or solver failure.
3.4 Heuristics compared
(1) h : uniform-cost search. (2) h : admissible. (3) h : inadmissible reference. (4) h : cost-
0 max add sp
weighted shortest-path relaxation. (5) h : the learned heuristic. Methods (2)–(4) are the classical A*
θ
baselines (“normal A*”); h is the uniform-cost baseline.
0
3.5 Learned heuristic
GNN.Privilegenodescarrywhethertheprivilegeisheldinthecurrentstateandwhetheritisthegoal;
exploitnodescarrynormalizedcostandCVSSattributes. Messagepassingoverthefact–actiongraph,
followedbypooling, yieldsascalarestimateofremainingcost-to-goh (s). MLP ablation. TheMLP
θ
sees graph-level hand-built features (e.g. numbers of privileges and exploits, privileges currently held,
h (s), aggregate CVSS cost statistics), which tests whether the relational GNN representation adds
sp
value over non-relational features.
Labels and verification. Training targets are exact optimal costs-to-go from an exact solver on
small graphs. On small instances they are cross-checked against an independent uniform-cost search
implementation (and exhaustive enumeration on the smallest), providing an independent check that
the generated labels match optimal costs on small instances.
Loss and admissibility. I will compare MSE with an asymmetric loss that penalizes overestimation
more, to test whether it reduces admissibility violations; it does not guarantee admissibility. I report
the overestimation rate |{s : h (s) > h∗(s)}|/|evaluated states|, plus mean and maximum violation.
θ
Weighted A* is used only as an additional empirical study of the efficiency–quality trade-off; no
suboptimality bound is claimed for an inadmissible heuristic.
3

| 3.6 Evaluation |     | protocol |     |     |     |     |     |     |     |
| -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Comparison with normal A*. All methods run on the same instances, so comparisons are paired
per instance and reported as ratios (nodes expanded relative to normal A*; plan cost relative to
optimal), with one summary table per test split and plots against graph size.
Splits. Topology-level train/validation/test splits are created first, from disjoint seeds; states and
optimal trajectories are then sampled only from the corresponding split, which prevents state-level
leakage. Test graphs are never used for training, early stopping, or tuning (validation only). Results
on training graphs are diagnostic only and support no claim. Each generalization test changes one
| factor and      | keeps | the others | within  |        | the training |     | range: |             |                |
| --------------- | ----- | ---------- | ------- | ------ | ------------ | --- | ------ | ----------- | -------------- |
| Test            |       | What       | changes |        |              |     |        | Held within | training range |
| In-distribution |       | fresh      | unseen  | graphs |              |     |        | everything  |                |
Size shift number of hosts (larger) topology family, vulnerability distribution
Structure shift topology family (held out) size range, vulnerability distribution
Vulnerability shift CVE feature distribution (held-out CVE size range, topology family
|     |     | groups               | with | a deliberately |         | shifted | CVSS-     |     |     |
| --- | --- | -------------------- | ---- | -------------- | ------- | ------- | --------- | --- | --- |
|     |     | attribute            |      | distribution,  |         | e.g.    | different |     |     |
|     |     | exploitability-score |      |                | ranges) |         |           |     |     |
Metrics and reporting. Nodes expanded; plan cost relative to optimal; wall-clock time; fraction
solved within a fixed expansion budget; overestimation statistics. Results report mean ± standard
deviation across random seeds, alongside the per-instance paired comparisons. All timings use the
same hardware configuration, and GNN inference overhead is included in end-to-end run time. Graph
| sizes and  | budgets | are fixed | after        | a   | pilot  | in Weeks | 3–4.      |              |      |
| ---------- | ------- | --------- | ------------ | --- | ------ | -------- | --------- | ------------ | ---- |
| 4 Current  |         | Work      | in           | the | Area   |          |           |              |      |
| The papers | below   | are       | the starting |     | point; | Week     | 1 extends | the survey.  |      |
| Work       |         | What      | it did       |     |        |          |           | Gap relevant | here |
Sheyner et al. [2] Automatedattack-graphgenerationbysymbolic Generationandanalysis;nolearnedsearchguid-
|     |     | model    | checking,      | plus | analyses | of      | which attacks | ance |     |
| --- | --- | -------- | -------------- | ---- | -------- | ------- | ------------- | ---- | --- |
|     |     | are most | cost-effective |      | to guard | against |               |      |     |
MulVAL [3] Datalog-based multihost, multistage vulnerabil- Graph generation; no learned heuristics
|     |     | ity analysis |     | that ingests | vulnerability-database |     |     |     |     |
| --- | --- | ------------ | --- | ------------ | ---------------------- | --- | --- | --- | --- |
data
Hoffmann [4]; Systematize simulated pentesting from Dijkstra Broader or partially observable models; this
Shmaryahu et on explicit graphs to POMDPs; pentesting as project is classical and fully observable
| al. [5] |     | contingent | planning |     |     |     |     |     |     |
| ------- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- |
Agostinelli et Learned cost-to-go with weighted A* on combi- Puzzle domains, not attack graphs
| al. [6] |     | natorial | puzzles; | solutions |     | not always | optimal |     |     |
| ------- | --- | -------- | -------- | --------- | --- | ---------- | ------- | --- | --- |
Shen et al. [7] Learned heuristics over hypergraphs of delete- General planning, not attack-graph topology
|     |     | relaxedproblems;generalizeacrosssizesandun- |         |     |     |     |     | shift |     |
| --- | --- | ------------------------------------------- | ------- | --- | --- | --- | --- | ----- | --- |
|     |     | seen                                        | domains |     |     |     |     |       |     |
This project GNN heuristic for A* on attack graphs Tests unseen size, structure and vulnerability
|                |     |          |     |     |     |       |     | shifts against | normal A* |
| -------------- | --- | -------- | --- | --- | --- | ----- | --- | -------------- | --------- |
| 5 Feasibility, |     | Timeline |     |     | and | Roles |     |                |           |
Solo project: I hold all roles. The plan assumes about ten weeks from the week of 5 October and will
be adjusted once the final date is announced. Weekly commits provide the progress trail.
4

| Week | Milestone  |         |             |     |        |              | Tier |
| ---- | ---------- | ------- | ----------- | --- | ------ | ------------ | ---- |
| 1    | Literature | survey; | repository; |     | MulVAL | install test | Core |
2 Fixformulationandcostmodel; converter; MulVALgo/no-go(elsenativegenerator) Core
3 Topology generators, CVE assignment; pilot for sizes and budgets Core
4 Exact solver, label cross-check, classical A* baselines Core
| 5   | Training-data | generation;         |         | MLP        | ablation |     | Secondary |
| --- | ------------- | ------------------- | ------- | ---------- | -------- | --- | --------- |
| 6   | GNN           | heuristic           | and GPU | training   | pipeline |     | Core      |
| 7   | h in          | A*; in-distribution |         | evaluation | (H1,     | H2) | Core      |
θ
8 Size, structure and vulnerability shift experiments (H3) Core
9 Asymmetric loss, weighted A*, analysis, plots, reproducibility scripts Optional/Core
10 Final report, AI-usage disclosure, demo and viva preparation Core
Risks and limitations. Topologies are synthetic, so generalization to generated topologies does not
guarantee generalization to real enterprise networks. The cost model is a modelling choice, not a
calibrated measurement. Exact labels limit training graphs to sizes the exact solver can handle, which
is why size generalization is a central test. Partial observability is out of scope.
References
[1] P. E. Hart, N. J. Nilsson, B. Raphael. A formal basis for the heuristic determination of minimum cost paths. IEEE
| Trans. | Syst. | Sci. Cybern., | 4(2):100–107, |     | 1968. |     |     |
| ------ | ----- | ------------- | ------------- | --- | ----- | --- | --- |
[2] O.Sheyner,J.Haines,S.Jha,R.Lippmann,J.M.Wing.Automatedgenerationandanalysisofattackgraphs.IEEE
Symp. Security and Privacy, pp. 254–265, 2002. https://doi.org/10.1109/SECPRI.2002.1004377
[3] X. Ou, S. Govindavajhala, A. W. Appel. MulVAL: A logic-based network security analyzer. USENIX
Security, pp. 113–128, 2005. https://www.usenix.org/conference/14th-usenix-security-symposium/
mulval-logic-based-network-security-analyzer
[4] J. Hoffmann. Simulated penetration testing: From “Dijkstra” to “Turing Test++”. ICAPS, 2015. https://doi.
org/10.1609/icaps.v25i1.13684
[5] D.Shmaryahu,G.Shani,J.Hoffmann,M.Steinmetz.Simulatedpenetrationtestingascontingentplanning.ICAPS,
| pp. 241–249, |     | 2018. |     |     |     |     |     |
| ------------ | --- | ----- | --- | --- | --- | --- | --- |
[6] F. Agostinelli, S. McAleer, A. Shmakov, P. Baldi. Solving the Rubik’s cube with deep reinforcement learning and
search. Nature Machine Intelligence, 1:356–363, 2019. https://doi.org/10.1038/s42256-019-0070-z
[7] W. Shen, F. Trevizan, S. Thi´ebaux. Learning domain-independent planning heuristics with hypergraph networks.
ICAPS, 30(1):574–584, 2020. https://ojs.aaai.org/index.php/ICAPS/article/view/6754
| [8] NIST. | National | Vulnerability |     | Database. | https://nvd.nist.gov/ |     |     |
| --------- | -------- | ------------- | --- | --------- | --------------------- | --- | --- |
[9] FIRST. Common Vulnerability Scoring System. https://www.first.org/cvss/
5