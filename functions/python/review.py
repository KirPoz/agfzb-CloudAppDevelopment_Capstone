#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
from cloudant.result import Result
from cloudant.query import Query
import re


def main(dict):
    databaseName = "reviews"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        #print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    
    my_database = client[databaseName]
    
    try:
        dealershipId = dict["DEALERID"]
        dealershipId = re.sub('[^A-Za-z0-9]+', '', dealershipId)
        query = Query(my_database, selector = {"dealership": {'$eq': int(dealershipId)}}, 
                    fields= ['id','name','dealership','review','purchase','purchase_date',
                                'car_make','car_model','car_year'])
        return {"listRew": query.result[:]}   
    except:
        return {
            "statusCode": 404,
            "message":"dealerId does not exist"
            
        }
        
