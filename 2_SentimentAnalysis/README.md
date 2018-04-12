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
	![Inline policies screenshot](images/inline-policies.png)

1. Select **Choose a service**.

1. Begin typing `Comprehend` into the search box labeled **Find a service** and select **Comprehend** when it appears. 
	![Select policy service](images/select-policy-service.png)
	
1. Choose **Select actions**.

1.	Begin typing `DetectSentiment` into the search box labeled **Filter actions** and check the box next to **DetectSentiment** when it appears.

1. Choose **Review Policy**.

1. Enter `ComprehendDetectSentiment` for the policy name and choose **Create policy**.
    ![Review Policy](images/review-policy.png)
	
</p></details>

### 2. Create a Lambda Function 

#### Background

AWS Lambda will run your code in response to events in this case from API Gateway (which we will cover in the next section). In this step you'll build the core function that will process API requests (via API Gateway) from the web application to detect a sentiment of a feedback text. In the next section you'll use Amazon API Gateway to create a RESTful API that will expose an HTTP endpoint that can be invoked from your users' browsers. You'll then connect the Lambda function you create in this step to that API in order to create a fully functional backend for your web application.

#### High-Level Instructions

Use the AWS Lambda console to create a new Lambda function called `DetectSentiment` that will process the requests. 

Make sure to configure your function to use the `NLPWLambda` IAM role you created in the previous section.

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary><p>

1. Choose on **Services** then select **Lambda** in the Compute section.

1. Click **Create function**.

1. Keep the default **Author from scratch** card selected.

1. Enter `DetectSentiment` in the **Name** field.

1. Select **Python 3.6** for the **Runtime**.

1. Ensure `Choose an existing role` is selected from the **Role** dropdown.

1. Select `NLPWLambda` from the **Existing Role** dropdown.
    ![Create Lambda function screenshot](images/create-lambda-function.png)

1. Click on **Create function**.

1. Scroll down to the **Function code** section and replace the exiting code in the **lambda_function.py** code editor with the contents of [DetectSentiment.py](DetectSentiment.py).
    ![Create Lambda function screenshot](images/create-lambda-function-code.png)

1. Click **"Save"** in the upper right corner of the page.

</p></details>

## Implementation Validation

For this section you will test the function that you built using the AWS Lambda console. In the next section you will add a REST API with API Gateway so you can invoke your function from the browser-based application that you deployed in the first module.

1. From the main edit screen for your function, select **Configure test event** from the the **Select a test event...** dropdown.
    ![Configure test event](images/configure-test-event.png)
	
1. Keep **Create new test event** selected.

1. Enter `TestRequestEvent` in the **Event name** field

1. Copy and paste the following test event into the editor:

	```JSON
    {
        "path": "/ride",
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Authorization": "eyJraWQiOiJLTzRVMWZs",
            "content-type": "application/json; charset=UTF-8"
        },
        "queryStringParameters": null,
        "pathParameters": null,
        "requestContext": {
            "authorizer": {
                "claims": {
                    "cognito:username": "the_username"
                }
            }
        },
        "body": "{\"PickupLocation\":{\"Latitude\":47.6174755835663,\"Longitude\":-122.28837066650185}}"
    }
    ```

    ![Configure test event](images/configure-test-event-2.png)
	
1. Click **Create**.

1. On the main function edit screen click **Test** with `TestRequestEvent` selected in the dropdown.   

1. Scroll to the top of the page and expand the **Details** section of the **Execution result** section.

1. Verify that the execution succeeded and that the function result looks like the following:

```JSON
{
    "statusCode": 201,
    "body": "{\"RideId\":\"SvLnijIAtg6inAFUBRT+Fg==\",\"Unicorn\":{\"Name\":\"Rocinante\",\"Color\":\"Yellow\",\"Gender\":\"Female\"},\"Eta\":\"30 seconds\"}",
    "headers": {
        "Access-Control-Allow-Origin": "*"
    }
}
```

After you have successfully tested your new function using the Lambda console, you can move on to the next section.

### 3. Add a Resource and Method to the existing REST API

API Gateway calls the Lambda function we created at the previous step. Create a GET method that invokes the Lambda function and passes the IDs of each user feedback as an event. 

Create a new resource called `/detectsentiment` within your API. Then create a GET method for that resource and configure it to use a Lambda proxy integration backed by the `DetectSentiment` function you created in the previous section.

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary><p>

1. In the left nav, click on **Resources** under your VOCApp API.

1. From the **Actions** dropdown select **Create Resource**.

1. Enter `detectsentiment` as the **Resource Name**.

1. Ensure the **Resource Path** is set to `detectsentiment`.

1. Select **Enable API Gateway CORS** for the resource.

1. Click **Create Resource**.

    ![Create resource screenshot](images/create-resource.png)

1. With the newly created `/detectsentiment` resource selected, from the **Action** dropdown select **Create Method**.

1. Select `GET` from the new dropdown that appears, then **click the checkmark**.

    ![Create method screenshot](images/create-method.png)

1. Select **Lambda Function** for the integration type.

1. Check the box for **Use Lambda Proxy integration**.

1. Select the Region you are using for **Lambda Region**.

1. Enter the name of the function you created in the previous module, `DetectSentiment`, for **Lambda Function**.

1. Choose **Save**. Please note, if you get an error that you function does not exist, check that the region you selected matches the one you used in the previous module.

    ![API method integration screenshot](images/api-integration-setup.png)

1. When prompted to give Amazon API Gateway permission to invoke your function, choose **OK**.

1. Choose on the **Method Request** card.

1. Open the **URL Query String Parameters**, and click on **Add query string** link. Enter Name as `Id` and then **click the checkmark**.

	![API method request 1 screenshot](images/api-query_string-setup.png)

1.	Go back to the previous screen and choose **Integration Request** card.

1.	Scroll down to see Body Mapping Templates and open the section by clicking on the arrow on the left side. 

1.	Click on **Add mapping template** link and type `application/json` in the textbox.

	![API method request 2 screenshot](images/api-body_mapping--template-setup.png)

1.	When you save it by clicking on the checkmark, it will bring up a text area. Type `{ "ID": "$input.params('Id')" }` into it and press the save button. 

	![API method request 3 screenshot](images/api-body_mapping-template.png)

</p></details>

### 4. Deploy Your API