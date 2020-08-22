resource "aws_sns_topic" "trade_signal" {
  name = "trade-signal-topic"
  delivery_policy = <<EOF
{
"http": {
    "defaultHealthyRetryPolicy": {
    "minDelayTarget": 20,
    "maxDelayTarget": 20,
    "numRetries": 3,
    "numMaxDelayRetries": 0,
    "numNoDelayRetries": 0,
    "numMinDelayRetries": 0,
    "backoffFunction": "linear"
    },
    "disableSubscriptionOverrides": false,
    "defaultThrottlePolicy": {
    "maxReceivesPerSecond": 1
    }
}
}
EOF

}