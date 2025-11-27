# Terraform AWS Infrastructure Setup

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Terraform installed (v1.0+)
- GitHub repository with Actions enabled

## Step-by-Step Setup Procedure

### Step 1: Create AWS Backend Infrastructure

Before running Terraform, you need to create the S3 bucket and DynamoDB table for state management.

#### 1.1 Create S3 Bucket for Terraform State

```bash
aws s3api create-bucket \
  --bucket terraform-bucket-state-aws \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1
```

Enable versioning on the bucket:

```bash
aws s3api put-bucket-versioning \
  --bucket terraform-bucket-state-aws \
  --versioning-configuration Status=Enabled \
  --region ap-south-1
```

Enable encryption:

```bash
aws s3api put-bucket-encryption \
  --bucket terraform-bucket-state-aws \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }' \
  --region ap-south-1
```

#### 1.2 Create DynamoDB Table for State Locking

```bash
aws dynamodb create-table \
  --table-name terraform-lock-table \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1
```

#### 1.3 Verify Resources Created

Check S3 bucket:
```bash
aws s3 ls | grep terraform-bucket-state-aws
```

Check DynamoDB table:
```bash
aws dynamodb describe-table --table-name terraform-lock-table --region ap-south-1
```

### Step 2: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID | `AKIAIOSFODNN7EXYY675TR7888AMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key | `555wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_REGION` | AWS Region for your resources | `ap-south-1` |

### Step 3: Initialize Terraform Locally (Optional)

If you want to test locally before pushing to GitHub:

```bash
# Initialize Terraform
terraform init

# Format code
terraform fmt

# Validate configuration
terraform validate

# Create execution plan
terraform plan

# Apply changes (if plan looks good)
terraform apply
```

### Step 4: Push to GitHub

Once you push your code to GitHub, the workflows will automatically trigger:

- **Pull Requests**: Runs `terraform plan` to show what changes will be made
- **Push to main branch**: Runs `terraform apply` to apply the changes

```bash
git add .
git commit -m "Setup Terraform infrastructure"
git push origin main
```

### Step 5: Monitor GitHub Actions

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Monitor the workflow execution
4. Check for any errors in the logs

## Troubleshooting

### Error: "Requested resource not found" (DynamoDB)

**Problem**: DynamoDB table doesn't exist.

**Solution**: Run Step 1.2 to create the DynamoDB table.

### Error: "NoSuchBucket" (S3)

**Problem**: S3 bucket doesn't exist.

**Solution**: Run Step 1.1 to create the S3 bucket.

### Error: "Input required and not supplied: aws-region"

**Problem**: GitHub secret `AWS_REGION` is not configured.

**Solution**: Follow Step 2 to add the missing secret.

### Error: "Access Denied"

**Problem**: AWS credentials don't have sufficient permissions.

**Solution**: Ensure your IAM user/role has permissions for:
- S3 (read/write to state bucket)
- DynamoDB (read/write to lock table)
- Any resources Terraform will create

## Workflow Files

This repository includes three GitHub Actions workflows:

1. **terraform.yml** - Full CI/CD pipeline (plan on PR, apply on main)
2. **terraform-plan.yml** - Only runs plan on pull requests
3. **terraform-apply.yml** - Only runs apply on main branch pushes

## Backend Configuration

The Terraform backend is configured in `provider.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-bucket-state-aws"
    key            = "project1/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}
```

## Security Best Practices

- ✅ State file encryption enabled
- ✅ S3 bucket versioning enabled
- ✅ DynamoDB state locking enabled
- ✅ AWS credentials stored as GitHub secrets
- ⚠️ Consider using OIDC instead of long-lived AWS credentials
- ⚠️ Enable S3 bucket public access blocking
- ⚠️ Add bucket policies to restrict access

## Next Steps

1. Add your Terraform resources to `main.tf`
2. Define variables in `variables.tf`
3. Define outputs in `outputs.tf`
4. Test locally with `terraform plan`
5. Create a pull request to see the plan
6. Merge to main to apply changes

## Cleanup

To destroy all resources created by Terraform:

```bash
terraform destroy
```

To remove the backend infrastructure (S3 bucket and DynamoDB table):

```bash
# Delete DynamoDB table
aws dynamodb delete-table --table-name terraform-lock-table --region ap-south-1

# Empty and delete S3 bucket
aws s3 rm s3://terraform-bucket-state-aws --recursive
aws s3api delete-bucket --bucket terraform-bucket-state-aws --region ap-south-1
```
