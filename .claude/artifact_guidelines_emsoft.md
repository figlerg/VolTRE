Call for Artifacts – EMSOFT

As software researchers, we produce a lot of software artifacts to assess our research. The objective of the artifact review is to ensure the quality and reusability of these artifacts. This will foster research reproducibility and new research that builds on top of previous discoveries.

Authors of papers accepted at the EMSOFT 2026 technical track will be invited to submit an artifact associated to their paper as candidate for the

    Available
    Reviewed
    Reproducible

These badges are considered independent and any one, two, or all three can be applied to any given paper. The authors can apply for any combination of the three. If the artifact is accepted, it will receive the awarded badges on the front page of the authors’ paper and in the proceedings.
Submission

Submission Link
Important Dates (AoE)

    17 July: EMSOFT 2026 paper notification and authors invitation to
    submit an artifact.
    24 July: Artifact submission deadline.
    24 August: Artifact decision notification.

Artifacts

Artifacts consist of reusable products that other researchers can use to bootstrap their own research. Experience shows that such papers earn increased citations and greater prestige in the research community. Artifacts of interest include (but are not limited to) the following.

    Software, which are implementations of systems or algorithms potentially useful in other studies.
    Data repositories, which are data (e.g., logging data, system traces, survey raw data) that can be used for multiple software engineering approaches.
    Frameworks, which are tools and services illustrating new approaches to embedded software engineering that could be used by other researchers in different contexts.

This list is not exhaustive, so the authors are asked to email the chair before submitting if their proposed artifact is not on this list.

There is no need to anonymize the artifact nor the submission. The review process will be single-blind.
Badges
Badge Name 	Description 	Figure
- Available: 	The code and/or datasets, including any associated data and documentation, provided by the authors is reasonable and complete and can potentially be used to support reproducibility of the published results. 	
- Reviewed: 	The code and/or datasets, including any associated data and documentation, provided by the authors is reasonable and complete, runs to produce the outputs described, and can support reproducibility of the published results.
- Reproducible: 	This badge signals that an additional step was taken or facilitated to certify that an independent party has regenerated computational results using the author-created research objects, methods, code, and conditions of analysis. Reproducible assumes that the research objects were also reviewed. 	
Submission Instructions

Submissions are made on the HotCRP submission website. In the submission form, authors must include:

    - A link to access the archival repository of the artifact (possibly the DOI if the authors are applying for the Available badge).
    - The technical skills and environments expected to review the artifact. For example, if the artifact runs only on a specific OS, or given (possibly licensed) software is required (e.g., Matlab), or if given hardware is required (e.g., a GPU).
    - Include the paper (the accepted version) as pdf in the submission.
    - Specify which badges the authors are applying for.

Please note the deadline:

    Submission deadline: 24 July.

CONCERNING HARDWARE REQUIREMENTS Note that it is the authors’ duty to clearly state hardware and software constraints in the submission form. Failing to do so might prevent the reviewers from being able to evaluate the artifact, (potentially) leading to rejection of the badges awarding.

It is also up to the authors to assess whether the hardware requirements are compatible with the software evaluation process. For example, if the experiments require a specific microcontroller, then it is almost impossible that a reviewer would be able to execute the artifact. In such case, it is recommended that the authors apply only for the available badge, as the evaluation for the other badges would be impossible within the constraints of the artifact evaluation process.
Preparing the artifact

Making the Artifact Available. The authors must make the artifact available through a persistent repository, with an assigned DOI. We encourage all authors to generate a DOI that points to the specific version with which the results of the paper can be reproduced, and provide the DOI in their abstract submission (e.g., in Zenodo: do not use the “always latest” DOI). The authors are welcome to include in the artifact’s documentation links to open-source repositories or websites where the development of the artifact will continue or new releases will be made available. However, such resources do not replace the requirement for a doi-indexed persistent copy.

Note, it is technically possible to have the other badges such as Functional and Reusable without the Available one (i.e., artifact access needs to be given only to the reviewers). However, due to Open Science Policies, this is strongly discouraged (exceptions can be made in well documented, special cases). In such cases a private link can be used to make the artifact available to the reviewers (e.g., the private links in figshare).

Installation Package. If the artifact consists of a tool or software system, then the authors need to prepare an installation package so that the tool can be installed and run in the reviewer’s environment. Provide enough associated instruction, code, and data such that some CS person with a reasonable knowledge of scripting, build tools, etc. could install, build, and run the code. If the artifact contains or requires the use of a special tool or any other non-trivial piece of software the authors must provide a VirtualBox VM image or a Docker container image with a working environment containing the artifact and all the necessary tools.

We expect the artifacts to be vetted on a clean machine before submission.

Documenting the Artifact. The artifact should contain the following documentation files:

    - A README main file describing what the artifact does. There should be a clear description of how to use the artifact and specifically how to repeat/replicate/reproduce the results presented in the paper. Artifacts that focus on data should, in principle, cover aspects relevant to understanding the context, data provenance, ethical and legal statements (as long as relevant), and storage requirements. Artifacts that focus on software should, in principle, cover aspects relevant to how to install and use it (and be accompanied by a small example).
    - A REQUIREMENTS file for artifacts that focus on software. This file should, in principle, cover aspects of hardware environment requirements (e.g., performance, storage or non-commodity peripherals) and software environments (e.g., Docker, VM, and operating system) but also, if relevant, a requirements.txt with explicit versioning information (e.g. for Python-only environments). Any deviation from standard environments needs to be reasonably justified.
    - A STATUS file stating what kind of badge(s) the authors are applying for, including the reasons why the authors believe that the artifact deserves each badge.
    - A LICENSE file describing the distribution rights. Note that to score “available,” then that license needs to be some form of open-source license.
    An INSTALL file with installation instructions. These instructions should include notes illustrating a very basic usage example or a method to test the installation. This could be, for instance, on what output to expect that confirms that the code is installed and working; and the code is doing something interesting and useful.
    - A copy of the accepted paper in PDF format.

