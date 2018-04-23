# Serverless NLP Workshop

In this workshop you'll deploy a voice-of-the-customer application that enables users to submit feedback about your product. The application will present users with an HTML based user interface for providing feeback and will interface on the backend with a RESTful web service to submit the request. The internal facing application will help the business owners to analyze the feedback provided using Natural Language Processing (NLP) techniques.

The application architecture uses [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [Amazon S3](https://aws.amazon.com/s3/), [Amazon DynamoDB](https://aws.amazon.com/dynamodb/), [Amazon Comprehend](https://aws.amazon.com/comprehend/), [Amazon ECR](https://aws.amazon.com/ecr/), and [Amazon SageMaker](https://aws.amazon.com/sagemaker/). S3 hosts static web resources including HTML, CSS, JavaScript, and image files which are loaded in the user's browser. JavaScript executed in the browser sends and receives data from a public backend API built using Lambda and API Gateway. DynamoDB provides a  persistence layer where data can be stored by the API's Lambda function. Comprehend provides NAtural Language Processing service needed to predict the sentiment from the feedback entered by users. SageMaker is used to orchestrate the machine learning process needed to predict gender of the user from name. ECR is used to host the machine learning training code. Finally, Python binding for Keras - machine learning framework is used to create the model needed for gender prediction.

See the diagram below for a depiction of the complete architecture.

![Unicorn ML Application Architecture](images/unicornml-complete-architecture.png)

If you'd like to jump in and get started please visit the [VoC Framework](1_VocFramework) module page to begin the workshop.

## Prerequisites

### AWS Account

In order to complete this workshop you'll need an AWS Account with access to create AWS IAM, S3, DynamoDB, Lambda, API Gateway, Comprehend, and Sagemaker. The code and instructions in this workshop assume only one student is using a given AWS account at a time. If you try sharing an account with another student, you'll run into naming conflicts for certain resources. You can work around these by appending a unique suffix to the resources that fail to create due to conflicts, but the instructions do not provide details on the changes required to make this work.

All of the resources you will launch as part of this workshop are eligible for the AWS free tier if your account is less than 12 months old. See the [AWS Free Tier page](https://aws.amazon.com/free/) for more details.

### Browser

We recommend you use the latest version of Chrome to complete this workshop.

### Text Editor

You will need a local text editor for making minor updates to configuration files.

## Modules

This workshop is broken up into multiple modules. You must complete each module before proceeding to the next, however, modules 1 and 2 have AWS CloudFormation templates available that you can use to launch the necessary resources without manually creating them yourself if you'd like to skip ahead.

1. [Creating a VOC application framework](1_VocFramework)
2. [Adding sentiment analysis](2_SentimentAnalysis)
3. [Create your own NLP classifier](3_NLPClassifier)
4. [Named entity recognition](Coming soon)
5. [Topic modelling of the feedback](Coming soon)

After you have completed the workshop you can delete all of the resources that were created by following the [cleanup guide](9_CleanUp).

## Cleanup
Please delete the following resources in this given order. 
1. Delete Cloudformation stack created in Step #3
2. Delete Cloudformation stack created in Step #2
3. Delete Cloudformation stack created in Step #1
4. Delete the Sagemaker deployment instance
5. Delete the Sagemaker notebook instance
