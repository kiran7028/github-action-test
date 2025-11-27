
How This CI/CD Pipeline Works (Simple Words)

When you create a Pull Request:
	•	GitHub Action runs
	•	Checks formatting
	•	Validates Terraform syntax
	•	Runs Terraform Plan
	•	Shows any changes

When code is merged to main:
	•	GitHub Action runs
	•	Terraform Apply executes
	•	AWS resources are created/updated/deleted

⸻

🧪 Local Workflow (Before Pushing Code)
	1.	terraform fmt
	2.	terraform init
	3.	terraform validate
	4.	terraform plan
	5.	Commit & push

⸻

🛡️ Security Best Practices

✔ Never store AWS keys in .tf files
✔ Always use GitHub Secrets
✔ Protect main branch
✔ Review Terraform plans before applying
✔ Use S3 backend for state




Create the DynamoDB table manually

Run this AWS CLI command to create the table:
Secret Name
Description
AWS_ACCESS_KEY_ID
IAM Access Key
AWS_SECRET_ACCESS_KEY
IAM Secret Key
AWS_REGION
(e.g., ap-south-1)
TF_VAR_instance_type
Optional Terraform variable
TF_BACKEND_BUCKET
Optional (if using S3 backend)



aws dynamodb create-table \
  --table-name terraform-lock-table \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1


Create the DynamoDB table manually

Run this AWS CLI command to create the table:

aws dynamodb create-table \
  --table-name terraform-lock-table \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1