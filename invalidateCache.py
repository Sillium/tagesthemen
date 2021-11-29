import os
import datetime
import logging
import boto3
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('apigateway')

api_gateway_id = os.environ['API_GATEWAY_ID']
stage = os.environ['STAGE']

def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    logger.info(f"Stage: {stage}, API Gateway Id: {api_gateway_id}")

    response = client.flush_stage_cache(
        restApiId=api_gateway_id,
        stageName=stage
    )

    logger.info(f"Response: {json.dumps(response, indent=2)}")
