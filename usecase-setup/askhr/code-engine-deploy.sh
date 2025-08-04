#!/bin/bash
#
# Check for required inputs
: "${API_KEY:?Error: API_KEY is not set}"
: "${RESOURCE_GROUP:?Error: RESOURCE_GROUP is not set}"

# ---- Set variables ----
DOCKERFILE_PATH=usecase-setup/askhr/HCM_APP    # Path to Dockerfile in the repo
APP_NAME=hr-skills-app                          # Code Engine Application name
PORT=8000
REGION=us-south                                # region where Code Engine and watsonx reside
GHE_REPO_URL=git@github.ibm.com:skol/agentic-ai-client-bootcamp-instructors.git  
BRANCH_NAME=${1:-main}  
IMAGE_REGISTRY=us.icr.io                       # Can change to your preferred container registry region
IMAGE_NAMESPACE=$(ibmcloud cr namespaces --output json | jq -r '.[] | select(.name | startswith("cr-itz")) | .name')  # e.g., your-container-namespace
PRIVATE_KEY_PATH=${PRIVATE_KEY_PATH:-~/.ssh/id_rsa}  
CE_PROJECT_NAME=ce-$RESOURCE_GROUP

# ---- Login and target ----
ibmcloud config --check-version=false
ibmcloud login --apikey "$API_KEY" -r "$REGION" -g "$RESOURCE_GROUP" 
ibmcloud plugin install code-engine -f 
ibmcloud ce project select --name "$CE_PROJECT_NAME" 

echo "Using branch: $BRANCH_NAME"  

# ---- Create secrets ----
echo "Creating secrets..."
# Check if secret exists
if ibmcloud ce registry get --name cr-secret > /dev/null 2>&1; then
  echo "Secret cr-secret exists. Deleting..."
  ibmcloud ce registry delete --name cr-secret --force
fi

ibmcloud ce registry create \
  --name cr-secret \
  --server us.icr.io \
  --username iamapikey \
  --password "$API_KEY"

if ibmcloud ce secret get --name ghe-ssh-secret > /dev/null 2>&1; then
  echo "Secret cr-secret exists. Deleting..."
  ibmcloud ce secret delete --name ghe-ssh-secret --force
fi
ibmcloud ce secret create \
  --name ghe-ssh-secret \
  --format ssh \
  --key-path $PRIVATE_KEY_PATH
  
# ---- Create build from GHE repo ----
BUILD_NAME="${APP_NAME}-build"
IMAGE_TAG="${IMAGE_REGISTRY}/${IMAGE_NAMESPACE}/${APP_NAME}:latest"

echo "Create build from GHE repo..."
if ! ibmcloud ce build get --name $BUILD_NAME &> /dev/null; then
  ibmcloud ce build create --name "$BUILD_NAME" \
    --source "$GHE_REPO_URL" \
    --commit "$BRANCH_NAME" \
    --context-dir "$DOCKERFILE_PATH" \
    --strategy "dockerfile" \
    --image "$IMAGE_TAG" \
    --registry-secret cr-secret \
    --git-repo-secret ghe-ssh-secret \
    --timeout 900 \
    --size xlarge
else
  ibmcloud ce build update --name "$BUILD_NAME" \
    --source "$GHE_REPO_URL" \
    --commit "$BRANCH_NAME" \
    --context-dir "$DOCKERFILE_PATH" \
    --strategy "dockerfile" \
    --image "$IMAGE_TAG" \
    --registry-secret cr-secret \
    --git-repo-secret ghe-ssh-secret \
    --timeout 900 \
    --size xlarge
fi

# ---- Wait for the build to finish ----
echo "Submitting build..."
if ibmcloud ce buildrun submit \
  --build "$BUILD_NAME" \
  --wait; then

  echo "Build succeeded. Proceeding to deploy..."

  # Workaround for IBM Cloud Shell. The build takes a while, and Cloud Shell reinitializes, losing the resource group information
  ibmcloud target -g $RESOURCE_GROUP > /dev/null

  # ---- Deploy the app ----
  if ibmcloud ce application get --name "$APP_NAME" > /dev/null 2>&1; then
    echo "Application exists. Updating..."
    ibmcloud ce application update --name "$APP_NAME" \
      --image "$IMAGE_TAG" \
      --min-scale 1 --max-scale 1 \
      --registry-secret cr-secret \
      --port "$PORT" \
      --wait
  else
    echo "Application does not exist. Creating..."
    ibmcloud ce application create --name "$APP_NAME" \
      --image "$IMAGE_TAG" \
      --min-scale 1 --max-scale 1 \
      --registry-secret cr-secret \
      --port "$PORT" \
      --wait
  fi
else
  echo "❌ Build failed. Aborting deployment. See buildrun logs for details"
  exit 1
fi

# ---- Output app URL ----
ibmcloud target -g $RESOURCE_GROUP > /dev/null
APP_URL=$(ibmcloud ce application get --name "$APP_NAME" --output json | jq -r '.status.url')
echo "✅ App deployed at: $APP_URL"

