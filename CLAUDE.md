# VolTRE

## Overview
A tool for sampling uniformly timed words from a Timed Regular Expression, with guaranteed uniform distribution. 

In the simplest terms, define a TRE and then you can run one of the sampling methods to create samples. Depending on the TRE (some are easier than others, i.e. unambiguous expressions) sampling can be more or less hard.

## Repo outline
The full accepted paper tex is visible in paper_source. Check whether file .claude/repository.md and .claude/method.md is present. If it is, that's where you keep your context about where things are and what the method is in the paper. If it isn't there yet, read the repo and paper to populate these files.

Also, keep a file .claude/PLAN.md where you keep TODOs, steps that we discussed, things that we save for later, and things that we have completed. 

The paper experiments are in experiments/paper_experiments. The tool can be called on a .tre file, the syntax is in parse (together with the parsing logic). Some experiments are also in experiments/thesis_experiments of my MSc thesis that built some of the base method of this tool.

In gitignored wordgen, you can find a functioning installation of wordgen, a different tool that we compare against. Keep in mind that this is not shipped to origin, so we can't refer to it except if we list it as prerequisite and point to installation instructions. 

## Tasks

### Building an artifact for EMSOFT
The paper is accepted at EMSOFT. We need to provide an artifact to get our reusability stamps. The exact instructions are in .claude/artifact_guidelines_emsoft.md. Make sure that .claude/PLAN.md is always updated with these tasks and updated when we make progress. This TODO list should also include a list of all the replicable figures that are listed in the paper source (be careful not all figures made it into the final version). We should make an effort to make a clearly documented, easy to install and use, sufficiently clean artifact that is frozen for the future. We have to have an evaluation loop that I can easily run in a fresh environment/docker so the reviewers have a clearly working artifact. 


## Environment

- WSL Ubuntu, Python venv at .venv. Activate before running anything: `source .venv/bin/activate`
- Install: `pip install -e .` (setup.py). requirements.txt also exists. Both are maybe untested for fresh environments, verifying them is part of the artifact task. PyPI publication is planned, not strictly necessary for the artifact but would be cool to have.
- Python version: Python 3.12.13
- The tool is invoked on a .tre file: Invocation examples are in README.md. Treat them as unverified, testing them literally is part of the artifact task (see Verification).
- Development happens in the venv. Docker is a build target for the artifact only, not the dev environment.
- wordgen lives in gitignored wordgen/ as a local installation. It is a comparison baseline, not part of the artifact. Never assume it exists in a fresh environment. In artifact docs, list it as an optional prerequisite with a pointer to its installation instructions.

## Workflow rules

- Plan before acting for any change touching more than one file. Present the plan and wait for approval.
- Work in small increments, one logical step at a time.
- Never commit without asking. Propose a commit message, wait for explicit confirmation.
- Never push, force-push, hard-reset or rewrite history. Propose the exact command and let me run it. Also enforced via permission deny rules in .claude/settings.json.
- Update .claude/PLAN.md at the end of every work block: progress on artifact tasks, decisions, open questions.
- If .claude/repository.md or .claude/method.md are missing, populate them from the repo and paper_source, then have me review and correct them before relying on their content. Do not treat unreviewed generated notes as ground truth.
- Don't sign off with these things like "Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>". 
- In prose, don't use em dashes and semicolons. 

## Verification

- Definition of done for the artifact: the evaluation loop runs end to end in a fresh environment (Docker) and reproduces every replicable paper figure listed in .claude/PLAN.md, with no manual steps beyond what the artifact README documents.
- For code changes during artifact preparation: run the affected experiment or a smoke-test subset and confirm it completes without errors before considering the change done.
- Anything the reviewer must type is part of the artifact and must be tested literally as written in the README.

## Git state

- Current branch is experimental: new work and bug fixes, 31 commits ahead of main. Never force-push it.
- The artifact branch will be cut from experimental. Once cut and submitted, it is frozen: no content changes without my explicit instruction.
- Merging experimental into main is deferred, not part of the current task.
- Never push any branch. Propose the exact command, I run it.

