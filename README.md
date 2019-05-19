## User API - UAPI REST Service for CURD operations.

### Technology stack
- Python 3.7
- MongoDB
- Falcon REST framework
- Pipenv

### CI 
CI is done by GitLab CI public service and includes two stages (see `.gitlab-ci.yml`)
- test - run unit tests 
- build - create docker image

### CD 
Two modes of CD are available
- Standalone deployment with raw K8S yaml file deploy following objects
    - K8S deployment for MongoDB
    - K8S service for MongoDB
    - K8S secret for API service 
    - K8S deployment for API service 
    - K8S `NodePort 30081` service for API service

    Deploy standalone instance of API service with `kubectl apply -f deploy/k8s.yaml`

- Deployment with UAPI Operator
    
    MongoDB: 
    - K8S deployment for MongoDB
    - K8S service for MongoDB
    
    API Service: 
    - K8S secret for API service 
    - K8S deployment for API service 
    - K8S `NodePort 30081` service for API service

    UI Service:  
    - K8S deployment for UI service 
    - K8S `NodePort 30080` service for API service       
    
    [Deploying the app with uapi operator](https://gitlab.com/dimss/ppro-uapiui-operator)
    
    - Deploy the Operator `kubectl create -f https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/all-in-one.yaml`
    - Make sure the Operator container is up and running `kubectl get pods | grep uapi-operator`
    - Create new Custom Resource `kubectl create -f https://gitlab.com/dimss/ppro-uapiui-operator/raw/master/deploy/crds/uiapi_v1alpha1_uapi_cr.yaml`



