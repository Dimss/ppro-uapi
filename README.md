## User API - UAPI REST Service for CURD operations.

### Technology stack
- Python 3.7
- MongoDB
- Falcon REST framework
- Pipenv

### CI 
CI is done by GitLab CI public service and includes two stages (see `.gitlab-ci.yml`)
- test - run unit tests 
- build - create docker image. To build your own image, you'll have to define following GitLab CI environment variables
    - `DOCKER_REGISTRY_USER` username for your docker registry 
    - `DOCKER_REGISTRY_PASSWORD` password for your docker registry 
    - `DOCKER_REPOSITORY` the name of the docker repository to where to push the image
    - `APP_NAME` the application name which will be used as a docker image name
    
    Example 
     - `DOCKER_REPOSITORY=docker.io/dimssss`
     - `APP_NAME=uapi`
     
     Docker image will be `docker.io/dimssss/uapi:latest` and `docker.io/dimssss/uapi:git_sha_short_commit`
     
     If you don't want to build your own image you may use existing images
     - ui - `docker.io/dimssss/uapiui:latest`
     - api - `docker.io/dimssss/uapi:latest`

           
### CD 
Two modes of CD are available
- Standalone deployment with raw K8S yaml file deploy following objects
    - K8S deployment for MongoDB
    - K8S service for MongoDB
    - K8S secret for API service 
    - K8S deployment for API service 
    - K8S `NodePort 30081` service for API service

    Deploy standalone instance of API service with `kubectl create -f https://gitlab.com/dimss/ppro-uapi/raw/master/deploy/k8s.yaml`
    
    Cleanup `kubectl delete -f https://gitlab.com/dimss/ppro-uapi/raw/master/deploy/k8s.yaml`

- Deployment with UAPI Operator
    
    MongoDB: 
    - K8S deployment for MongoDB
    - K8S service for MongoDB
    
    [API Service](https://gitlab.com/dimss/ppro-uapi)
    - K8S secret for API service 
    - K8S deployment for API service 
    - K8S `NodePort 30081` service for API service

    [UI Service](https://gitlab.com/dimss/ppro-ui)
    - K8S deployment for UI service 
    - K8S `NodePort 30080` service for API service       
    
    ### Deploying the app with uapi [operator](https://gitlab.com/dimss/ppro-uapiui-operator)
    
    - Deploy the Operator `kubectl create -f https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/all-in-one.yaml`
    - Make sure the Operator container is up and running `kubectl get pods | grep uapi-operator`
    - Deploy UAPI-UI CR (replace the `K8S_EXTERNAL_NODE_IP` placeholder with actual `minikube ip` ) 
    `export NODE_IP=$(minikube ip) && curl -qs https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/crds/uiapi_v1alpha1_uapi_cr.yaml  | sed "s~K8S_EXTERNAL_NODE_IP~${NODE_IP}~g" | kubectl create -f -`
    - Wait for all resources become `Running`
    - Get minikube ip and open the url in the browser `echo http://$(minikube ip):30080`
    
    Cleanup
    - `kubectl delete -f https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/crds/uiapi_v1alpha1_uapi_cr.yaml`
    - `kubectl delete -f https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/all-in-one.yaml`



