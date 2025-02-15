# Run in a loop and produce custom otel metric
import time
import random
from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
import os

OTEL_COLLECTOR_ENDPOINT = os.environ.get("OTEL_COLLECTOR_ENDPOINT")

# Initialize the OTLP exporter
otlp_exporter = OTLPMetricExporter(
    endpoint=OTEL_COLLECTOR_ENDPOINT,
    insecure=True
)

# Initialize metric reader with manual submission


# Initialize the metric reader with the OTLP exporter
metric_reader = PeriodicExportingMetricReader(
    otlp_exporter, 
    export_interval_millis=1000
)

# assume you have machines with temperature sensors, produce metrics which will immitate these machines
machine_ids = [f"machine_{i}" for i in range(5)]
# Initialize the meter provider with the metric reader
meter = MeterProvider(metric_readers=[metric_reader]).get_meter("sensor-mock")

# Create gauge metric for machine temperature
temperature_metric = meter.create_gauge("temperature", unit="celsius", description="Temperature of the machine")

# Produce sample temeratures in a loop, take into account previous temperature to not overload it
previous_temperatures = {machine_id: random.uniform(70, 80) for machine_id in machine_ids}
while True:
    for machine_id in machine_ids:
        temperature = previous_temperatures[machine_id] + random.uniform(-2, 2)
        if temperature < 50:
            temperature = 50
        if temperature > 99:
            temperature = 99

        # Update the previous temperature for the next iteration
        previous_temperatures[machine_id] = temperature
        
        # Record the temperature metric
        temperature_metric.set(temperature, {"machine_id": machine_id})

    print("Recorded values successfully!")
    time.sleep(1)