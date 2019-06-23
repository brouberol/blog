Title: Managing my infra like it's 2019
Date: 2019-07-22
Category: Programming
Status: draft


I recently realized that I was routinely managing thousands of servers and petabytes of data in my daily job, but was still managing my own personal infrastructure like I was living in 1999.

![my-infra](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/managing-infra/infra.png)

---

With the advent of configuration management tools such as [Ansible](https://docs.ansible.com/), [Chef](https://www.chef.io/), and the like, it became easier to configure instances in a reproducible manner by defining said configuration as code. [Terraform](http://terraform.io/) made it easier to codify and provision cloud resources: instances, but also security groups, permissions, storage, load balancers, etc.

It's easy to simply think of a cloud infrastructure as a pool of compute resource. It is however often so much more than that. When executed right, The Cloud is a set of meshed services, interacting and communicating with each other (possibly with compute resources sitting in the middle). That applies for vast and complex infrastructures such as the one I work on at [Datadog](https://datadoghq.com), but it also applies to my ridiculously tiny personal one. Realizing this got me thinking. Why wasn't I using the same tools and techniques to manage my small infrastructure than the ones I'm using daily?


## My infrastructure

My personal infrastructure consists of (drumrolls...) 3 servers:

- a VPS running at Scaleway, hosting my personal services (personal website, blog, git repositories, [CalDAV server](https://radicale.org/documentation/), [traffic analytics](https://usefathom.com/), [IRC client](https://thelounge.chat/), [Read-it-later service](https://www.wallabag.org/en), etc)
- a VPS running at OVH, hosting my mother's website
- a Raspberry Pi, running in my living room, hosting private services ([Kresus](https://kresus.org/en/index.html))

Until now, each of these servers were managed in an _ad-hoc_ fashion, sometimes with scripts, sometimes without. All the cloud resources on which my services (S3 buckets, DNS zones, etc) were managed manually, using the cloud provider web console.

I manage my DNS zones with OVH, I use the AWS S3 bucket free tier for the blog images, and Datadog for monitoring.

![ssl-expiry-monitoring](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/managing-infra/datadog-monitors.png)


## Improving the setup

I had several objectives in mind to improve the current setup:

- define all instances configuration and state in [ansible playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
- re-use and share instances configuration by leveraging [ansible roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- define and manage all cloud resources using [terraform](https://terraform.io) to never have to log into a cloud web console again
- secure all web-services with an automatically renewed SSL certificate provided by Let's Encrypt
- run all services behind a reverse-proxy, using a docker container or a [userland systemd service](https://www.brendanlong.com/systemd-user-services-are-amazing.html) with minimal permissions and privileges
- monitor the hosts and services using [Datadog](https://datadoghq.com) (free for 5 hosts or less) , with monitors define in terraform
- secure the SSH connections of the internet-facing hosts via [Duo](https://duo.com/) (free for 10 users or less)
- be able to SSH into all hosts from my personal and work laptop, as well as from my [phone](https://play.google.com/store/apps/details?id=org.connectbot&hl=en_US)
- monitor my daily backups


## Show me the code

You can have a look at the code [here](https://github.com/brouberol/infrastructure). I've purposefully omitted the `terraform/global_vars/main.tf` file, credentials are obviously encrypted, API keys are defined in my home directory, but everything else is readable openly. My hope is that that readers might either learn something or point out where I'm doing something silly or insecure.


## What now?

I'm now confident that I can open some of these services to friends, if they need to. I measure and monitor my own SLIs, the expiry of the SSL certificates, and can intervene from anywhere if something breaks.

![ssl-expiry-monitoring](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/managing-infra/ssl-expiry-monitoring.png)

My infrastructure is now more secure, and has been audited by fellow peers [^review]. I'm now confident I can restore the services in the face of an instance loss (which is very important for my mother, as her website has a fair amount of traffic and brings her regular new customers).

I'm also dogfooding Datadog features, which got to me suggest a couple of improvements to the Datadog [terraform provider](https://www.terraform.io/docs/providers/datadog/index.html) which will be worked on next quarter.


[^review]: Thanks to Mehdi and Thomas for the thorough playbook review. Any remaining mistake or silliness is my own.