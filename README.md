# k8s_bh_reservation
```


Build with: 

docker build --push --platform linux/arm64 -t eu-frankfurt-1.ocir.io/frs4lzee0jfi/bh_reservation:latest .


k apply -f k8s/bh_reserve_pvc.yaml

k apply -f k8s/bh_reserve_configmaps.yaml
k apply -f k8s/bh_reserve_secrets.yaml

k delete -f k8s/bh_reserve_cronjobs.yaml
k apply -f k8s/bh_reserve_cronjobs.yaml


Run with: 

docker run --env-file=.env eu-frankfurt-1.ocir.io/frs4lzee0jfi/bh_reservation:latest

docker run --env-file=.env bhreservationcontainerized
docker run --platform linux/arm/v7 --env-file=.env bhreservationcontainerized

```
