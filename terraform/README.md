# Terraform: onboard a new team

This stack gives every product team its own storage bucket in `prod`. It is
already applied: `terraform.tfstate` holds the live state, and the bucket names
are referenced by other systems, so existing buckets must never be renamed or
recreated.

To keep the exercise offline, buckets are modelled with the `random` provider
and the built-in `terraform_data` resource. No cloud account or credentials are
needed; `terraform init` downloads one small provider.

## Requirements

- Terraform >= 1.5
- Internet access for `terraform init`

## Task

The **payments** team needs a bucket. Add `payments` to the team list in
`terraform.tfvars`, keeping the list alphabetical (between `identity` and
`search`), and make whatever other changes are needed so the change is safe to
apply to production.

## Goal

Your change is ready when `terraform plan`:

- creates the bucket for `payments` (its `random_id` suffix and its
  `terraform_data` bucket), and nothing else;
- leaves every existing bucket untouched (nothing destroyed, replaced or
  modified).

Treat this like a change going to production: review the plan, but **do not
run `terraform apply`**. Change any Terraform files you need to. Tell us when
you think you're done, and be ready to explain what you changed and why.

## Commands

```sh
cd terraform
terraform init                      # once
terraform plan                      # on a fresh checkout: "No changes"
git checkout -- terraform.tfstate   # restore the original state if it gets changed
git checkout -- .                   # start over: undo edits to existing files
terraform workspace select default  # if you created another workspace
```

## If you finish early

We also want a `dev` environment with its own, shorter list of teams. How would
you add it without copying the Terraform code and without disturbing the `prod`
state?
