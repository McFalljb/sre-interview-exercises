# Discussion questions

We'll talk through these five questions together, about 6 minutes each. They're
written down here so you can read them on your own. There are no right answers
to memorise: tell us how you'd approach each one, what you'd want to know first
and what trade-offs you see. Asking clarifying questions is welcome.

## 1. Scaling Terraform

We have a single deployment directory full of Terraform files that deploys our
whole cloud setup. How would you make it easier to work with and more scalable?

## 2. Postgres WAL load, read replicas and blue/green

We have a large Postgres instance shared by several microservices. It's gotten
to the point that we can't run a read replica because of the WAL load. The goal
is to have read replicas and to do blue/green upgrades. How would you get there?

## 3. Networking RDS and EKS

What are some of the ways to do networking in the cloud? Say I have a database
in RDS and my services run in EKS. How can you network them together? How would
that solution scale?

## 4. API pods went down during an EKS upgrade

You're upgrading a large EKS cluster with many nodes. During the upgrade, our
API service went down, even though it runs multiple replicas. What would you
change so this doesn't happen again?

## 5. p99 latency doubled

You get paged: p99 latency on one of our main services doubled about an hour
ago. Error rate looks normal. Walk me through what you do.
