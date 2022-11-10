# Awesome CI/CD Security [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

List of awesome resources about CI/CD security included books, blogs, videos, tools and cases.

## Table of Contents

  - [Book](#book)
  - [Blogs](#blogs)
  - [Videos](#videos)
  - [Repositories](#repositories)
  - [Playground](#playground)
  - [Cases](#cases)

## Book

- [Advanced Infrastructure Penetration Testing](https://www.packtpub.com/product/advanced-infrastructure-penetration-testing/9781788624480)

## Blogs

### General

- [Top 10 CI/CD Security Risks](https://github.com/nathanawmk/top-10-cicd-security-risks)
- [Continuous Delivery 3.0 Maturity Model (CD3M)](https://nisi.nl/continuousdelivery/articles/maturity-model)
- [Visualizing CI/CD from an attacker’s perspective](https://medium.com/cider-sec/visualizing-ci-cd-from-an-attackers-perspective-22dfa38c9d09)
- [The Anatomy of an Attack Against a Cloud Supply Pipeline](https://www.paloaltonetworks.com/blog/2021/10/anatomy-ci-cd-pipeline-attack/)
- [When Supply-Chain Attacks Meet CI/CD Infrastructures](https://blogs.vmware.com/networkvirtualization/2021/12/29260.html/)
- [CI/CD Supply Chain Attacks for Data Exfiltration or Cloud Account Takeover](https://www.praetorian.com/blog/ci-cd-supply-chain-attacks-for-data-exfiltration-or-cloud-account-takeover/)
- [Detecting Malicious Activity in CI/CD Pipeline with Tracee](https://blog.aquasec.com/cicd-pipeline-security-tool-tracee)
- [Let’s Hack a Pipeline: Argument Injection](https://devblogs.microsoft.com/devops/pipeline-argument-injection/)
- [Let’s Hack a Pipeline: Stealing Another Repo](https://devblogs.microsoft.com/devops/pipeline-stealing-another-repo/)
- [Let’s Hack a Pipeline: Shared Infrastructure](https://devblogs.microsoft.com/devops/pipeline-shared-infrastructure/)
- [Poorly Configured CI/CD Systems Can Be A Backdoor Into Your Infrastructure](https://thenewstack.io/poorly-configured-ci-cd-systems-can-be-a-backdoor-into-your-infrastructure/)
- [Assess Vulnerabilities and Misconfigurations in CICD Pipelines: Part 1](https://success.qualys.com/discussions/s/article/000005841)
- [Assess Vulnerabilities and Misconfigurations in CICD Pipelines: Part 2](https://success.qualys.com/discussions/s/article/000005842)
- [Defending software build pipelines from malicious attack](https://www.ncsc.gov.uk/blog-post/defending-software-build-pipelines-from-malicious-attack)
- [Cloud Native Best Practices: Security Policies in CI/CD Pipelines](https://blog.aquasec.com/cloud-native-security-best-practices-devops-security)

### GitLab

- [Abusing GitLab Runners](https://frichetten.com/blog/abusing-gitlab-runners/)
- [Securing GitLab CI pipelines with Sysbox](https://blog.nestybox.com/2020/10/21/gitlab-dind.html)
- [GitLab - Security for self-managed runners](https://docs.gitlab.com/runner/security/)
- [Critical GitLab vulnerability could allow attackers to steal runner registration tokens](https://portswigger.net/daily-swig/critical-gitlab-vulnerability-could-allow-attackers-to-steal-runner-registration-tokens)

### GitHub Actions

- [Self-hosted runner security](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners#self-hosted-runner-security)
- [GitHub Action Runners Analyzing the Environment and Security in Action](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/github-action-runners-analyzing-the-environment-and-security-in-action)
- [Github Actions Security Best Practices](https://engineering.salesforce.com/github-actions-security-best-practices-b8f9df5c75f5)
- [Automatically Secure Your CI/CD Pipelines Using Tracee GitHub Action](https://blog.aquasec.com/ci-cd-pipeline-security-tracee-github-action)

### Jenkins

- [Attacking Jenkins](https://msgpeek.net/blog/2020/02/attacking-jenkins/)
- [Reflections on trusting plugins: Backdooring Jenkins builds](https://www.synopsys.com/blogs/software-security/backdooring-jenkins-builds-and-security-measures/)
- [Securing Jenkins](https://www.jenkins.io/doc/book/security/securing-jenkins/)
- [How to Secure Jenkins Pipelines without the hassle](https://www.contrastsecurity.com/security-influencers/how-to-secure-jenkins-pipelines-without-the-hassle#:~:text=Navigate%20to%20your%20Jenkins%20UI,available%20to%20your%20Jenkins%20instance.)

### ArgoCD

- [Security Considerations](https://argo-cd.readthedocs.io/en/stable/security_considerations/)

## Videos

- [Challenges to Securing CI/CD Pipelines](https://www.youtube.com/watch?v=Pd6akunYaZc)
- [Attacking Development Pipelines For Actual Profit](https://www.youtube.com/watch?v=AQCvfzwcGso)
- [Exploiting Continuous Integration (CI) and Automated Build systems](https://www.youtube.com/watch?v=mpUDqo7tIk8)
- [Continuous Intrusion: Why CI Tools Are An Attacker's Best Friends](https://www.youtube.com/watch?v=0H6jd5yG7_A)
- [How to Build a Compromise Resilient CI/CD](https://www.youtube.com/watch?v=ArS31CxneUA)
- [Argo CD Security Practices](https://www.youtube.com/watch?v=3IoLH1j6cm0)

## Repositories

- [Threat Matrix for CI/CD Pipeline](https://github.com/rung/threat-matrix-cicd)
- [Jenkins Attack Framework](https://github.com/Accenture/jenkins-attack-framework)
- [pwn_jenkins](https://github.com/gquere/pwn_jenkins)

## Playground

- [CI/CDon't](https://hackingthe.cloud/aws/capture_the_flag/cicdont)
- [CI/CD Goat](https://github.com/cider-security-research/cicd-goat)

## Cases

- [10 real-world stories of how we’ve compromised CI/CD pipelines](https://research.nccgroup.com/2022/01/13/10-real-world-stories-of-how-weve-compromised-ci-cd-pipelines/)
- [CI/CD pipeline attacks: A growing threat to enterprise security](https://limacharlie.io/blog/cicd-pipeline-attacks)
- [Poisoned pipelines: Security researcher explores attack methods in CI environments](https://portswigger.net/daily-swig/poisoned-pipelines-security-researcher-explores-attack-methods-in-ci-environments)
- [Travis CI Flaw Exposes Secrets of Thousands of Open Source Projects](https://thehackernews.com/2021/09/travis-ci-flaw-exposes-secrets-of.html)
- [GitHub Actions being actively abused to mine cryptocurrency on GitHub servers](https://www.bleepingcomputer.com/news/security/github-actions-being-actively-abused-to-mine-cryptocurrency-on-github-servers/)
- [Report: Software supply chain attacks increased 300% in 2021](https://venturebeat.com/2022/01/27/report-software-supply-chain-attacks-increased-300-in-2021/)
- [Critical vulnerability discovered in popular CI/CD framework](https://www.itpro.co.uk/security/cyber-security/361400/critical-vulnerability-discovered-in-popular-cicd-framework)
- [Malicious Kubernetes Helm Charts can be used to steal sensitive information from Argo CD deployments](https://apiiro.com/blog/malicious-kubernetes-helm-charts-can-be-used-to-steal-sensitive-information-from-argo-cd-deployments/)
- [New Attacks on Kubernetes via Misconfigured Argo Workflows](https://www.intezer.com/blog/container-security/new-attacks-on-kubernetes-via-misconfigured-argo-workflows/)
- [Argo CD Security Bug Opens Kubernetes Cloud Apps to Attackers](https://threatpost.com/argo-cd-security-bug-kubernetes-cloud-apps/178239/)
- [Ransomware attacks on GitHub, Bitbucket, and GitLab – what you should know](https://gitprotect.io/blog/ransomware-attacks-on-github-bitbucket-and-gitlab-what-you-should-know/)
- [Compromising CI/CD Pipelines with Leaked Credentials](https://blog.gitguardian.com/security-zines-2-compromising-ci-cd-pipelines/)

## [Contributing](contributing.md)

Your contributions are always welcome.

## License

[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
