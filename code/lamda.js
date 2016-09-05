
console.log('Loading event');
exports.handler = function(event, context) {{
  var AWS = require('aws-sdk');
  var sns = new AWS.SNS();
  var ml = new AWS.MachineLearning();
  var endpointUrl = '';
  var mlModelId = '';
  var snsTopicArn = '';
  var numMessagesProcessed = 0;
  

  var updateSns = function(Data) {{
    var params = {};
    params['TopicArn'] = snsTopicArn;
    params['Subject']  = Data.toString();
    params['Message']  = Data.toString();
    console.log('Calling Amazon SNS to publish.');
    sns.publish(
      params,
      function(err, data) {{
        if (err) {{
          console.log(err, err.stack); // an error occurred
          context.done(null, 'Failed when publishing to SNS');
        }}
        else {{
          context.done(null, 'Published to SNS');
        }}
      }}
      );
  }}

  var callPredict = function(tweetData){{
    console.log('calling predict');
    ml.predict(
      {
        Record : tweetData,
        PredictEndpoint : endpointUrl,
        MLModelId: mlModelId
      },
      function(err, data) {{
        if (err) {{
          console.log(err);
          context.done(null, 'Call to predict service failed.');
        }}
        else {{
          console.log('Predict call succeeded');
          updateSns(data.Prediction.predictedValue);
        
        }}
      }}
      );
  }}

  var processRecords = function(){{
    for(i = 0; i < numMessagesToBeProcessed; ++i) {{
      encodedPayload = event.Records[i].kinesis.data;
      payload = new Buffer(encodedPayload, 'base64').toString('utf-8');
      console.log("payload:"+payload);
      try {{
        parsedPayload = JSON.parse(payload);
        callPredict(parsedPayload);
      }}
      catch (err) {{
        console.log(err, err.stack);
        context.done(null, "failed payload"+payload);
      }}
    }}
  }}

  var checkRealtimeEndpoint = function(err, data){{
    updateSns('real');
    if (err){{
      updateSns('fail in fetch');
      console.log(err);
      context.done(null, 'Failed to fetch endpoint status and url.');
    }}
    else {{
      var endpointInfo = data.EndpointInfo;
      updateSns('check');

      if (endpointInfo.EndpointStatus === 'READY') {{
        endpointUrl = endpointInfo.EndpointUrl;
        console.log('Fetched endpoint url :'+endpointUrl);
        processRecords();
        updateSns('Ready');
      }} else {{
        console.log('Endpoint status : ' + endpointInfo.EndpointStatus);
        context.done(null, 'End point is not Ready.');
        updateSns('Fail');
      }}
    }}
  }}
  
  ml.getMLModel({MLModelId:mlModelId}, checkRealtimeEndpoint);
  
}};