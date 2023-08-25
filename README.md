# k8s_bh_reservation
```

Status: Not working (on arm64). chromedriver chrashes. 


Build with: 

docker build --push --platform linux/arm64 -t eu-frankfurt-1.ocir.io/frs4lzee0jfi/bh_reservation:latest .




Run with: 

docker run --env-file=.env eu-frankfurt-1.ocir.io/frs4lzee0jfi/bh_reservation:latest

docker run --env-file=.env bhreservationcontainerized
docker run --platform linux/arm/v7 --env-file=.env bhreservationcontainerized

```
