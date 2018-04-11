# Module 2: Sentiment Analysis using Comprehend

In this module you'll use [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/lambda/) and [Amazon Comprehend](https://aws.amazon.com/comprehend/) to analyze the feedback that users enter through the web page. The browser application that you deployed in the first module allows users to enter their name and feedback. The JavaScript running in the browser invokes an API Gateway and then Lambda to persist the information entered in a DynamoDB table.
 
Now in order to activate “Predict Sentiment” functionality, you will implement an API Gateway and a Lambda function that 

## Architecture Overview

The architecture for this module is composed of AWS Lambda function that leverage the sentiment analysis capabilities of Amazon Comprehend. Feedback entered by the user through the web page is persisted in a DynamoDB table. Upon the request from the web page, API Gateway invokes the Lambda function, which sends an API call to Comprehend to do the sentiment analysis. The result is saved to the DynamoDB table and the web page gets refreshed to show the result of the analysis, both through the Lambda function and API Gateway.  

![Sentiment Analysis Architecture](images/sentiment-analysis-architecture.jpg)

## Implementation Instructions

Each of the following sections provide an implementation overview and detailed, step-by-step instructions. The overview should provide enough context for you to complete the implementation if you're already familiar with the AWS Management Console or you want to explore the services yourself without following a walkthrough.

If you're using the latest version of the Chrome, Firefox, or Safari web browsers the step-by-step instructions won't be visible until you expand the section.

### 1. Create an IAM Role for your Lambda function 

#### Background

Every Lambda function has an IAM role associated with it. This role defines what other AWS services the function is allowed to interact with. For the purposes of this workshop, you'll need to create an IAM role that grants your Lambda function permission to write logs to Amazon CloudWatch Logs and detect sentiment by Comprehend.

#### High-Level Instructions

Use the IAM console to create a new role. Name it `NLPWLambda` and select AWS Lambda for the role type. You'll need to attach policies that grant your function permissions to write to Amazon CloudWatch Logs and detect sentiment by Comprehend.
Attach the managed policy called `AWSLambdaBasicExecutionRole` to this role to grant the necessary CloudWatch Logs permissions. Also, create a custom inline policy for your role that allows the `comprehend:DetectSentiment` action

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary><p>

1.	From the AWS Management Console, click on **Services** and then select **IAM** in the Security, Identity & Compliance section.
1.	Select **Roles** in the left navigation bar and then choose **Create new role**.
1.	Select **Lambda** for the role type from the **AWS service** group, then click **Next: Permissions**

    **Note:** Selecting a role type automatically creates a trust policy for your role that allows AWS services to assume this role on your behalf. If you were creating this role using the CLI, AWS CloudFormation or another mechanism, you would specify a trust policy directly.

1.	Begin typing `AWSLambdaBasicExecutionRole` in the Filter text box and check the box next to that role.	
1.	Click **Next: Review**.
1.	Enter `NLPWLambda` for the **Role name**.
1.	Choose **Create role**.
1.	Type `NLPWLambda` into the filter box on the Roles page and choose the role you just created.
1.	On the Permissions tab, choose the **Add inline policy** link in the lower right corner to create a new inline policy. 
	![Inline policies screenshot](../images/inline-policies.png)