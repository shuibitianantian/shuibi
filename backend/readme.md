# Architecture of backend
There are so many way to accomplish this project. For simplicity, I decided to use serverless services to host the project.

AWS services: `S3`, `Lambda Function`, `API Gateway`

1. All data will be stored in `AWS S3`
2. Data query logics are implemented in 2 `AWS Lambda Function`s. In fact, I can directly use S3 select feature in the frontend so I can remove this layer. I did not implemented in that way, because I do not think that is good (maybe I am wrong).
3. The requests are redirected to `AWS Lambda Function` via `AWS API Gateway`


# Steps of preparing data
1. Get s&p 500 listed company information via wiki (I only need the stock code, but I saved some other informations)
2. Get maximum daily historical data of each stock, and keep it updated everyday
3. Generate traning dataset
4. Build model and save it locally
5. Predict and upload prediction to `S3`

Currently, I am processing data locally and upload it to S3. In fact, I can host everything by `Lambda Function` or use `EC2`. Because the steps are fixed, I can use `EventBridge` to trigger the data process routine after the trading period. I did do it because I want to save my time to play __`Dota2`__.
