# Cloud Resume - Backend

The backend consists of AWS Lambda, API Gateway and a DynamoDB table. The serverless architecuture is deployed with AWS SAM through the GitHub Actions CD pipeline. The pipeline also consists of a Pytest module, where the Lambda function is tested against a mock dynamoDB table instantiated with the python moto package. 
