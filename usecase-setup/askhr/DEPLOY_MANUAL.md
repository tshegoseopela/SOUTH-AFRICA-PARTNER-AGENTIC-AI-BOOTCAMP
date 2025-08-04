# Deploy the AskHR Backend Application Manually

These instructions will walk you thru the process to deploy the askhr [backend application](./HCM_APP) manually within **IBM Cloud Serverless Containers (Code Engine)**. 

1. Navigate to [IBM Cloud](cloud.ibm.com).

   <img width="1000" alt="image" src="./app_deployment_images/image0.1.png">

1. Click on the hamburger menu in the top left and then select **Resource List**.

   <img width="1000" alt="image" src="./app_deployment_images/image0.2.png">

1. This will show you a list of available resources in your instance. Select **Containers**, which will give you a list of products. Choose the **Code Engine** product.

   <img width="1000" alt="image" src="./app_deployment_images/image0.3.png">

1. This is **Code Engine** project homepage.
   <img width="1000" alt="image" src="./app_deployment_images/image1.png">

1. Create Registry and SSH secrets. For those steps go [here](../../environment-setup/common/Readme.md)

1. Create the Application. From menu, click on "Applications", then click on "Create".
   <img width="1000" alt="image" src="./app_deployment_images/image2.png">

1. Give your application a name, i.e. `hr-skills-app`. Select "Build container image from source code" under Code section. Paste `git@github.ibm.com:skol/agentic-ai-client-bootcamp-instructors.git` in "Code repo URL" field.
Then click on "Specify build details"
   <img width="1000" alt="image" src="./app_deployment_images/image3.png">

1. In "SSH secret" field, you have to select your ssh secret that you created in Step 5 to access the Github repository. In "Branch name" field, type `main` or whatever branch you want to deploy from. In "Context directory" field, put `usecase-setup/askhr/HCM_APP`. Finally click on "Next".
   <img width="1000" alt="image" src="./app_deployment_images/image4.png">

1. In next step, select Strategy `Dockerfile`, keep Timeout `40m`. In "Build resources", select `M(1 vCPU / 4 GB)` from dropdown. Then click on "Next"
   <img width="1000" alt="image" src="./app_deployment_images/image5.png">

1. Select available registry server from dropdown in "Registry Server" field, In "Registry secret" field, select your registry secret that you created in Step 5. "Namespace" field will be automatically filled, otherwise you can select one from dropdown. 
Give your Repository (image) a name, in "Tag" section, type `latest`. Finally click on "Done".
   <img width="1000" alt="image" src="./app_deployment_images/image6.png">

1. Scroll down a bit. Increase "Min number of instances" to 1. 
   <img width="1000" alt="image" src="./app_deployment_images/image7.png">

1. Select "Public" in Domain mappings.
   <img width="1000" alt="image" src="./app_deployment_images/image8.png">

1. In "Image start options", under "Listening port", edit the value from `8080` to `8000`.
   <img width="1000" alt="image" src="./app_deployment_images/image11.png">

1. Click on "Create" in right.
   <img width="1000" alt="image" src="./app_deployment_images/image12.png">   

1. Wait for the status to change to "Ready". Once its ready, click on the application.
   <img width="1000" alt="image" src="./app_deployment_images/image13.png">

1. Click on "Test application".
 <img width="1000" alt="image" src="./app_deployment_images/image14.png">

1. Click on "Application URL". You'll be directed to a website. Take note of this URL, you will need it in the final setup steps [here](./README.md#3-update-api-spec-file-with-deployment-url)
   <img width="1000" alt="image" src="./app_deployment_images/image15.png">   
