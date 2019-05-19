# UAPI-UI Architecture

![schema](https://gitlab.com/dimss/ppro-uapi/raw/master/arch.png)

## Components overview

### Frontend UI
Stateless ReactJS application which provides an interfaces between end user 
and backend Python REST API service.

### API backend  
Stateless Python REST backend provides an interface between MongoDB and HTTP REST requests.
The user identity state provided by JWT tokens. 

### MongoDB 
NoSQL databased stores application state.

### UAPI-UI Operator
Manage deployment logic for all components    
  

## Scalability
Scalability could be easily achieved by increasing 
number of replicas of Backend service because this service is **stateless**.  

The Frontend service is stateless is as well, however most of the 
logic of Frontend service executed on the client machine, 
thus there is no really good reason to increase replicas of UI service 
until it will have extremely high load traffic on UI static server.

The MongoDB is a **stateful** component, which makes scalability
not such easy as other services. 
Scale MongoDB instance could be done by creating a sharded cluster, 
which will allow creating multiple replicas of the DB.
Yet, such solution will suffer from a lack of elasticity since there is no 
easy way to add or remove new shards to the sharded cluster.


## Deployment 
The deployment logic is managed by K8S Operator, 
which provides a powerful solution to manage deployment operations.
In UAPI-UI operator developer may define any custom logic required 
for deploying the application, add new components to the UAPI-UI 
and hide complex logic and configuration of deployment behind a scene.

To increase development and deployment speed, the UAPI-UI Operator 
could be bounded to the Git hook, which will trigger new deployment when 
either new commit or tag is pushed to the Git repo.  


