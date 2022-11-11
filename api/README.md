# Invest Alchemy API Service

## Library

```bash
npm install -g serverless
```

## How to start

- deploy serverless lambda

```bash
sls deploy
```

## API

- subscribe SNS topic by email

```bash
curl -H 'Content-Type: application/json' -d '{"email": "me@i365.tech"}' https://fey17sm0g7.execute-api.us-east-1.amazonaws.com/dev/subscribe
```
