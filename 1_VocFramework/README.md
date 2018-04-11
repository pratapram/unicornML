# Unicorn NLP Workshop

In this workshop you'll deploy a simple web application that enables users to submit product feedback . The application will present users with an HTML based user interface where they can submit feedback, predict sentiment about submitted feedbacks and identify gender for the user submitting feedback.

The application architecture uses [AWS Lambda](https://aws.amazon.com/lambda/), [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [Amazon S3](https://aws.amazon.com/s3/), [Amazon DynamoDB](https://aws.amazon.com/dynamodb/), [Amazon Comprehend](https://aws.amazon.com/comprehend/), [Amazon ECR](https://aws.amazon.com/ecr/), and [Amazon SageMaker](https://aws.amazon.com/sagemaker/). S3 hosts static web resources including HTML, CSS, JavaScript, and image files which are loaded in the user's browser. JavaScript executed in the browser sends and receives data from a public backend API built using Lambda and API Gateway. DynamoDB provides a  persistence layer where data can be stored by the API's Lambda function. Comprehend provides NAtural Language Processing service needed to predict the sentiment from the feedback entered by users. SageMaker is used to orchestrate the machine learning process needed to predict gender of the user from name. ECR is used to host the machine learning training code. Finally, Python binding for Keras - machine learning framework is used to create the model needed for gender prediction.

See the diagram below for a depiction of the complete architecture.

![Unicorn ML Application Architecture](images/unicornml-complete-architecture.png)

# Module 1: VOC Web Application Framework with Amazon S3

In this module you'll configure Amazon Simple Storage Service (S3) to host the static resources for your web application. In subsequent modules you'll add dynamic functionality to these pages using JavaScript to call remote RESTful APIs built with AWS Lambda and Amazon API Gateway.

If you're already comfortable working with Amazon S3, or you just want to skip ahead to working with Lambda and API Gateway, you can launch one of these AWS CloudFormation templates in the Region of your choice to build the necessary resources automatically.

Region| Launch
------|-----
US East (N. Virginia) | [![Launch Module 1 in us-east-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
US East (Ohio) | [![Launch Module 1 in us-east-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
US West (Oregon) | [![Launch Module 1 in us-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
EU (Frankfurt) | [![Launch Module 1 in eu-central-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
EU (Ireland) | [![Launch Module 1 in eu-west-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
EU (London) | [![Launch Module 1 in eu-west-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
Asia Pacific (Tokyo) | [![Launch Module 1 in ap-northeast-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
Asia Pacific (Seoul) | [![Launch Module 1 in ap-northeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
Asia Pacific (Sydney) | [![Launch Module 1 in ap-southeast-2](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)
Asia Pacific (Mumbai) | [![Launch Module 1 in ap-south-1](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/images/cloudformation-launch-stack-button.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=nlp-workshop-voc-webapp&templateURL=https://s3.amazonaws.com/nlp-workshop/templates/voc-webapp.json)


<details>
<summary><strong>CloudFormation Launch Instructions (expand for details)</strong></summary><p>

1. Click the **Launch Stack** link above for the region of your choice.

1. Click **Next** on the Select Template page.

1. Provide a globally unique name for the **Website Bucket Name** such as `nlp-yourname` and click **Next**.
    ![Speficy Details Screenshot](images/module1-cfn-specify-details.png)

1. On the Options page, leave all the defaults and click **Next**.

1. On the Review page, check the box to acknowledge that CloudFormation will create IAM resources and click **Create**.
    ![Acknowledge IAM Screenshot](images/cfn-ack-iam.png)

    This template uses a custom resource to copy the static website assets from a central S3 bucket into your own dedicated bucket. In order for the custom resource to write to the new bucket in your account, it must create an IAM role it can assume with those permissions.

1. Wait for the `nlp-workshop-voc-webapp` stack to reach a status of `CREATE_COMPLETE`.

1. With the `nlp-workshop-voc-webapp` stack selected, click on the **Outputs** tab and click on the WebsiteURL link.

1. Verify the VOC application home page is loading properly and move on to the next module, [Sentiment Analysis](../2_SentimentAnalysis).

</p></details>