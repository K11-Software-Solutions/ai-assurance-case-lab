# 01. Why Test Results Are Not an Assurance Case

> **Series:** AI Assurance Case Lab · [Index](../README.md#articles) · Next: [02. Claims, Arguments and Evidence](02-claims-arguments-and-evidence.md)

This is the capstone of a series of ten labs for quality engineers moving into AI. Each lab produced evidence about one part of an AI system: its answers, its model, its agents, its production behaviour, its performance and cost, its evaluators, its data, its security and its tool supply chain. This lab asks the question every one of them leads to: **can we sign this system off, on what evidence, and what risk are we accepting?**

## A pile of green builds is not an argument

At the end of a release cycle a team typically has dozens of reports: eval scores, red-team results, load tests, monitoring dashboards. Each says something true. None of them, alone or together, says "this system is fit to release". Something has to connect them:

- **Which claim does each result support?** A groundedness score of 1.0 supports "answers are grounded". It says nothing about whether the agent sends emails to the right people.
- **Is the evidence about this system?** A security report from the last version, or from a test environment with different defences, is evidence about something else.
- **How strong is it?** "0 of 30 attacks succeeded" and "0 of 1,440 succeeded" are both green, and support very different claims (see the [AI Security Testing Lab](https://github.com/K11-Software-Solutions/ai-security-testing-lab)).
- **What does the evidence say against us?** Every lab in this series found something that did not work. A release decision that does not mention those findings is not honest, and an auditor will find them.
- **Who accepted what remains?** Some known problems ship. Someone has to own that, and the acceptance has to end at some point.

An **assurance case** is the structure that answers those questions: a set of claims about the system, the argument for each, the evidence behind each, the evidence against, and the residual risks accepted. The idea comes from safety-critical engineering (aviation, rail, medical devices, nuclear), where nobody accepts "the tests passed" as a reason to ship.

## What this lab builds

- **An assurance case** for a fictional *Orbitly Support Assistant 2.3.0*, written as data ([`case/assurance_case.json`](../case/assurance_case.json)): 12 claims, 25 evidence items, 6 defeaters (evidence against) and 6 residual risks.
- **Evidence from the ten labs, pinned**: every item quotes, word for word, a result file from a lab's v1.0.0 release, at the exact commit Zenodo archived, with a hash (article 03).
- **Nine checks on the case itself** (article 07), and thirteen broken versions of the case that must fail them.
- **A release decision** ([`docs/release-decision.md`](../docs/release-decision.md)): GO, GO WITH ACCEPTED RISKS, or NO-GO, with the whole argument a reviewer needs.
- **Mappings** to the NIST AI Risk Management Framework, ISO/IEC 42001 and the EU AI Act's requirements for high-risk systems (article 06).

## A worked template, not an assurance

The evidence comes from teaching labs, most with simulated components. The case is therefore a **template**: it shows how to structure an argument, how to make evidence trustworthy and how to test the argument. It does not assure any real system, and the case says so in its own context statements. To use it for a real system, replace the evidence with evidence about that system (article 08).
