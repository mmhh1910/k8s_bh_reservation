# bh_reservation_containerized

Build with: 

docker build -t bhreservationcontainerized:latest .
docker build --platform linux/arm/v7 -t bhreservationcontainerized:latest .
docker build --platform linux/amd64 -t bhreservationcontainerized:latest .
docker build --platform linux/amd64,linux/arm/v7 -t bhreservationcontainerized:latest .


Run with: 

docker run --env-file=.env bhreservationcontainerized
docker run --platform linux/arm/v7 --env-file=.env bhreservationcontainerized