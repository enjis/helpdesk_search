# helpdesk_search

[![Continuous Integration](https://github.com/enjis/helpdesk_search/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/enjis/helpdesk_search/actions/workflows/ci.yml)

Help desk search engine to gain insights from your customers feedback

1. To insert dummy fake data in the database

```
python utils/fake_data.py --number 1000
```

2. To run the application

For WINDOWS :

```
set DB_URI=< MONGO URI OF YOUR DATABASE >
set SECRET_KEY=abxyz
python src/app.py
```

For LINUX :

```
export DB_URI=< MONGO URI OF YOUR DATABASE >
export SECRET_KEY="abxyz"
python src/app.py
```

3. To build and run docker container

```
docker build . -t helpdesk --build-arg db_var=< MONGO URI OF YOUR DATABASE >
docker run -d -p 5000:5000 helpdesk
```

4. To run kubernetes deployment of the server in cluster with a load balancer

```
kubectl apply -f k8s_manifest.yaml
```

5. Check deployment status with

```
kubectl get po
kubectl get service
```

If you are using minikube or similar single cluster setup on your local machine,
You may have to run one additional command to tunnel the service,
So that you can use it outside of the Kubernetes virtual network.

```
minikube service helpdesk-server
```

Deliverables:

1. Only admin allowed to add documents ---------> done
2. Relevant search for given query ---------> done
3. UI
4. Generate fake document ---------> done
5. REST api ---------> done
6. Unit tests/ Integration tests ---------> done
7. logs ---------> done
8. docker ---------> done
9. kubernetes manifest ---------> done
