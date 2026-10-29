# Related work and novelty check

Checked 2026-10-29 with web search.

**Opened** means the paper's abstract page or PDF was opened in this session and the
one-line summary comes from it. Papers marked **not opened** are listed for
completeness only and must not be cited until opened. Overlap is judged against
our two claims:

- **C1 (characterisation):** classical admissible heuristics (h_max, LM-cut) are
  near-exact on CVE-grounded attack graphs, including deeper and coupled variants
  (D15/D16, `findings.md` §7). Random-walk state sampling under-represents where
  they err.
- **C2 (learning):** a learned cost-to-go heuristic for A\* on attack graphs, and
  how it generalises to unseen topologies, sizes and CVE distributions.

## Verdict

**No paper found makes C2.** We found none that learns a cost-to-go heuristic for
A\* over attack graphs and tests it under topology, size and vulnerability
shift.

- *The nearest learned work on attack graphs* is RL policies (Hu et al. 2020;
  Terranova et al. 2024) and GNN path scorers (SPGNN-API). None is a heuristic
  inside optimal search.
- *The nearest learned-heuristic work* is domain-independent and evaluated on
  IPC benchmarks (STRIPS-HGN, GOOSE, WL-GOOSE).

**C1 is not new as a mechanism. It is new only as a measurement on attack
graphs, and must be framed that way.**

- *The mechanism is published.* Attack graphs with monotonic privileges are
  delete-free tasks, so h\* equals the optimal delete-relaxation value h+.
  Helmert & Domshlak (2009) show that LM-cut "gives excellent approximations
  to h+". So near-exactness of LM-cut on delete-free attack graphs is largely
  predicted by known results.
- *Optimal delete-free planning has dedicated exact methods* (Haslum et al.
  2012; Pommerening & Helmert 2012; Imai & Fukunaga 2015). A reviewer will ask
  why A\* is used at all.
- *What is new:*
  - the pre-registered measurement on CVE-grounded attack graphs, including
    under deliberate depth and coupling;
  - that A\* expansions stay at about plan length;
  - the per-instance sampling-bias result;
  - the inference-cost break-even: on these graphs a learned heuristic cannot
    beat compiled classical A\* on time (`results/feasibility/fd_crosscheck/`).

  None of these was found in the literature searched.
- *The search was not exhaustive:* about 15 literature searches and 20 papers opened. A
  dedicated query on "LM-cut accuracy on delete-free / attack-graph tasks" may
  still find a direct precedent: **[VERIFY before submission]**.

## Learned heuristics for classical and delete-free planning

| Paper | Opened | What it did | Overlap |
|---|---|---|---|
| Shen, Trevizan, Thiébaux. *Learning Domain-Independent Planning Heuristics with Hypergraph Networks* (STRIPS-HGN). ICAPS 2020. https://ojs.aaai.org/index.php/ICAPS/article/view/6754 | yes (abstract page) | Hypergraph network over the delete-relaxation hypergraph, trained on state/value pairs from optimal plans. Competitive with LM-cut; generalises across problems and domains. | **Closest method to C2.** Same label type (optimal cost-to-go) and a delete-relaxation graph input, but domain-independent, on IPC domains, not attack graphs; no topology, CVE or size-shift study. C2 must cite it and position as a domain-specific application plus a generalisation study. |
| Chen, Thiébaux, Trevizan. *Learning Domain-Independent Heuristics for Grounded and Lifted Planning* (GOOSE). AAAI 2024; arXiv:2312.11143. https://arxiv.org/abs/2312.11143 | yes (arXiv abstract) | Three graph representations of planning tasks for GNN heuristics, including lifted; generalises to much larger problems than training; beats STRIPS-HGN. | Size generalisation of a GNN heuristic is shown there, on IPC domains. Our H3 size shift is therefore not new in kind; its novelty is the attack-graph domain and the separate structure and CVE shifts. |
| Chen, Trevizan, Thiébaux. *Return to Tradition: Learning Reliable Heuristics with Classical Machine Learning* (WL-GOOSE). ICAPS 2024; arXiv:2403.16508. https://arxiv.org/abs/2403.16508 | yes (arXiv abstract) | WL features plus classical ML; far fewer parameters, faster training; beats h_FF in a fair setting. | Implies a **cheap non-deep baseline** that C2 should include: WL features plus linear or GP regression. A reviewer will ask why a GNN and not this. |
| Ståhlberg, Bonet, Geffner. *Learning General Optimal Policies with Graph Neural Networks: Expressive Power, Transparency, and Limits*. ICAPS 2022; arXiv:2109.10129. https://arxiv.org/abs/2109.10129 | yes (arXiv abstract) | Supervised GNN approximating V\* on small instances; the limits follow C2-logic expressiveness. | Same supervision idea (V\* from small instances); generalised planning, not attack graphs. Cite for the expressiveness limits of our GNN. |
| Chrestien, Edelkamp, Komenda, Pevný. *Optimize Planning Heuristics to Rank, not to Estimate Cost-to-Goal*. NeurIPS 2023; arXiv:2310.19463. https://proceedings.neurips.cc/paper_files/paper/2023/hash/50ea4dbd1cff6bd3daef939eff10c092-Abstract-Conference.html | yes (arXiv abstract and NeurIPS page) | Ranking losses tailored to A\*/GBFS; argues that cost-to-go regression is unnecessarily hard. | Directly relevant to the loss choice (CLAUDE.md §5 optional ranking loss). No attack-graph overlap. |
| Agostinelli, McAleer, Shmakov, Baldi. *Solving the Rubik's cube with deep reinforcement learning and search* (DeepCubeA). Nat. Mach. Intell. 2019. https://doi.org/10.1038/s42256-019-0070-z | **not opened this session** (blocked by redirect and bot protection; verified in the proposal) | Learned cost-to-go plus batched weighted A\*. | Background for batched evaluation; no overlap. |

## Optimal delete-free planning and heuristic accuracy (bears on C1)

| Paper | Opened | What it did | Overlap |
|---|---|---|---|
| Helmert, Domshlak. *Landmarks, Critical Paths and Abstractions: What's the Difference Anyway?* ICAPS 2009. https://ojs.aaai.org/index.php/ICAPS/article/view/13370 | yes (PDF) | Introduces LM-cut and shows experimentally that it "gives excellent approximations to h+". | **Largely predicts C1.** On delete-free tasks h+ = h\*, so LM-cut near-exactness is expected. C1 must cite this and claim only the attack-graph measurement and its consequences. |
| Pommerening, Helmert. *Optimal Planning for Delete-Free Tasks with Incremental LM-Cut*. ICAPS 2012. https://ojs.aaai.org/index.php/ICAPS/article/view/13532 | yes (abstract page) | Branch-and-bound and IDA\* in a delete-free search space with incremental LM-cut; beats A\*+LM-cut in Fast Downward. | A stronger exact baseline for delete-free tasks than our A\*. The "why search" question applies. |
| Haslum, Slaney, Thiébaux. *Minimal Landmarks for Optimal Delete-Free Planning*. ICAPS 2012. https://ojs.aaai.org/index.php/ICAPS/article/view/13534 | yes (abstract page) | Exact h+ by minimum-cost hitting sets over minimal disjunctive action landmarks. | Same as above. It resolves the `status_report.md` §6 `[VERIFY]` on hitting-set methods. |
| Imai, Fukunaga. *On a Practical, Integer-Linear Programming Model for Delete-Free Tasks and its Use as a Heuristic for Cost-Optimal Planning*. JAIR 54, 2015. https://jair.org/index.php/jair/article/view/10972 | yes (abstract page) | IP model solving delete-free tasks directly; its LP relaxation often approximates the optimal delete-free cost closely. | Same; it resolves the MIP part of that `[VERIFY]`. |
| Helmert, Röger. *How Good Is Almost Perfect?* AAAI 2008. https://mlanthology.org/aaai/2008/helmert2008aaai-good | yes (abstract page) | A\* can need exponentially many expansions even with heuristics off by a small additive constant, on common IPC domains. | Contrast for C1: on our attack graphs, near-exact heuristics do give about plan-length expansions. Worth discussing why: few symmetric alternatives, and short plans. |

## Penetration testing and attack graphs as planning

| Paper | Opened | What it did | Overlap |
|---|---|---|---|
| Lucángeli Obes, Sarraute, Richarte. *Attack Planning in the Real World*. SecArt @ AAAI 2010; arXiv:1306.4044. https://arxiv.org/abs/1306.4044 | yes (arXiv abstract) | PDDL attack model integrated into a pentest tool (Core Security); planners generate and validate attack paths on medium-sized networks. | Classical planning for attack paths; no learning. Motivates the formulation. |
| Sarraute, Buffet, Hoffmann. *POMDPs Make Better Hackers: Accounting for Uncertainty in Penetration Testing*. AAAI 2012. https://ojs.aaai.org/index.php/AAAI/article/view/8363 | yes (abstract page) | POMDP attack planning with per-machine decomposition. | Partial observability, which we exclude (threat to validity). No overlap. |
| Hoffmann. *Simulated Penetration Testing: From "Dijkstra" to "Turing Test++"*. ICAPS 2015 (invited). https://ojs.aaai.org/index.php/ICAPS/article/view/13684 | yes (abstract page) | Systematises the sequential-decision models for simulated pentesting. | Positioning; our model is the classical-planning end of that space. |
| Shmaryahu, Shani, Hoffmann, Steinmetz. *Simulated Penetration Testing as Contingent Planning*. ICAPS 2018. https://ojs.aaai.org/index.php/ICAPS/article/view/13902 | yes (abstract page) | Contingent planning as a middle ground between POMDP and classical models; scales on real network scans. | No overlap. |
| Ou, Govindavajhala, Appel. *MulVAL: A Logic-based Network Security Analyzer*. USENIX Security 2005. https://www.usenix.org/conference/14th-usenix-security-symposium/mulval-logic-based-network-security-analyzer | yes (abstract page) | Datalog attack-graph generation from vulnerability and configuration data. | The generator family we follow; no overlap. |
| Sheyner et al. *Automated generation and analysis of attack graphs*. IEEE S&P 2002. https://doi.org/10.1109/SECPRI.2002.1004377 | **not opened this session** (IEEE page empty; verified in the proposal) | Attack-graph generation by model checking. | Background. |

## Learning on attack graphs and in automated pentesting

| Paper | Opened | What it did | Overlap |
|---|---|---|---|
| Hu, Beuran, Tan. *Automated Penetration Testing Using Deep Reinforcement Learning*. EuroS&PW 2020. DOI 10.1109/EuroS&PW51379.2020.00009 (PDF: https://www.jaist.ac.jp/~razvan/publications/automated_penetration_testing_reinforcement_learning.pdf) | yes (PDF, first pages) | Shodan-based topologies, MulVAL attack trees and a DQN to pick the easiest attack path. | Learning over MulVAL attack graphs, but as an RL policy with no optimality guarantee and no A\*. Cite as the RL alternative. |
| Terranova, Lahmadi, Chrisment. *Leveraging Deep Reinforcement Learning for Cyber-Attack Paths Prediction: Formulation, Generalization, and Evaluation*. RAID 2024. https://doi.org/10.1145/3678890.3678902 (PDF: https://raid2024.github.io/papers/raid2024-12.pdf) | yes (PDF, first pages) | DRL attack-path agent with a local-view formulation, trained over diverse topologies, sizes and vulnerabilities; tested on unseen networks (CyberBattleSim). | **Closest generalisation study to our H3**, for RL policies, not search heuristics, with no optimal-cost evaluation. C2's H3 novelty must be stated relative to this. |
| Schwartz, Kurniawati. *Autonomous Penetration Testing using Reinforcement Learning*. arXiv:1905.05965, 2019. https://arxiv.org/abs/1905.05965 | yes (arXiv abstract) | Fast pentest simulator (the NASim line) and tabular and neural Q-learning; finds optimal attack paths on small networks. | RL baseline family; no learned heuristic. |
| Microsoft Defender Research. *CyberBattleSim*. GitHub, 2021. https://github.com/microsoft/CyberBattleSim | yes (repository) | Gym environment for RL agents doing lateral movement in a simulated network. | Environment only; no overlap. |
| Jmal et al. *SPGNN-API: A Transferable Graph Neural Network for Attack Paths Identification and Autonomous Mitigation*. arXiv:2305.19487 (page lists IEEE TIFS). https://arxiv.org/abs/2305.19487 | yes (arXiv abstract) | Transferable GNN for shortest-path identification toward critical assets, plus policy tuning. | A learned path or distance estimate on networks, but not a heuristic inside optimal A\*, and no CVE-shift study. Cite and contrast. |

## `[VERIFY]` items resolved by this check

- **The proposal (`docs/proposal.md`) contains no `[VERIFY]` marker.** Its
  references 1–8 were checked when it was written. This session reopened
  ref 3 (MulVAL), ref 4 (Hoffmann 2015), ref 5 (Shmaryahu et al. 2018) and
  ref 7 (STRIPS-HGN).
- **`docs/status_report.md` §8, exact delete-free methods (hitting-set and
  MIP):** resolved. The methods are Haslum et al. 2012 (hitting sets),
  Imai & Fukunaga 2015 (IP/LP) and Pommerening & Helmert 2012 (incremental
  LM-cut branch and bound).
- **D17 "related work on how accurate delete-relaxation heuristics are":**
  resolved by Helmert & Domshlak 2009. LM-cut approximates h+ closely, and
  h+ = h\* on delete-free tasks.
- **Not in scope here, still open:** the D9 NVD rounding rule, the D11 cve.org
  terms of use, and the D12 MulVAL rule-name correspondence. These are data
  and licence checks, not related work.
