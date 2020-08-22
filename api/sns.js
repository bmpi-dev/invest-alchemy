'use strict';

const AWS = require('aws-sdk');
const sns = new AWS.SNS({region: 'us-east-1'});

function validateEmail(email) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

module.exports.subscribe_sns = (event, context, callback) => {
  const email = event.body.email;

  if (!validateEmail(email)) {
    console.log('validate email fail: ' + email);
    const data = {
      statusCode: 200,
      body: JSON.stringify(
        {
          code: -1,
          message: 'Input a valid email.',
          email: email,
        },
        null,
        2
      ),
    };
    callback(null, JSON.stringify(data));
  }

  let params = {
    Protocol: 'EMAIL',
    TopicArn: process.env.snsTopicArn,
    Endpoint: email
  };

  sns.subscribe(params, (err, data) => {
    if (err) {
      console.log("SNS subscribe error: " + err);
      const data = {
        statusCode: 200,
        body: JSON.stringify(
          {
            code: -1,
            message: 'SNS subscribe error! Maybe try again later.',
            email: email,
          },
          null,
          2
        ),
      };
      callback(null, JSON.stringify(data));
    } else {
      console.log('subscribe success!');
      const data = {
        statusCode: 200,
        body: JSON.stringify(
          {
            code: 0,
            message: 'Subscribe success! Pending confirmation, need confirm email.',
            email: email,
          },
          null,
          2
        ),
      };
      callback(null, JSON.stringify(data));
    }
  });
};
