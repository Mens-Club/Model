from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import os

def report_training_metrics(loss_value, training_time):
    registry = CollectorRegistry()

    # 훈련 손실(loss)
    g_loss = Gauge('training_loss', 'Loss during training', registry=registry)
    g_loss.set(loss_value)

    # 훈련 시간(seconds)
    g_time = Gauge('training_duration_seconds', 'Training time in seconds', registry=registry)
    g_time.set(training_time)

    # Push to Pushgateway
    push_to_gateway(
        gateway=os.getenv("PUSH_GATEWAY_URL"),
        job="serverless_training",
        registry=registry
    )
