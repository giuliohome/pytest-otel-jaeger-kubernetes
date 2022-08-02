# OpenTelemetry Collectori
# docker run -it --rm -p 4317:4317 -p 4318:4318 -p 12345:12345 -v $(pwd):/cfg:ro otel/opentelemetry-collector:0.56.0 --config=/cfg/otel-config.yaml

# Grafana Agent
docker run -it --rm -p 4317:4317 -p 4318:4318 -p 12345:12345 -v $(pwd):/cfg:ro grafana/agent:main -config.file=/cfg/config.yaml
