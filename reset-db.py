import json
import boto3
import json
import decimal


 
db = boto3.resource('dynamodb')
# Helper class to convert a DynamoDB item to JSON.
locationTable = db.Table("locations")
roomTable = db.Table("rooms")

locations_list = ['queens','merchant ventures','hawthorns','senate house']  

def reset_bookings():
    try:
        for i in range(0,len(locations_list)):
            locationResponse = locationTable.get_item(
                    Key={"location":locations_list[i]}
                )
            location_item = locationResponse['Item']
            roomNumbers = location_item['roomNumbers']
            print(roomNumbers)
            for i in range(len(roomNumbers)):
                roomResponse = roomTable.get_item(
                    Key={"roomID":roomNumbers[i]}
                )
                roomTable.update_item(
                Key={'roomID': roomNumbers[i]},
                UpdateExpression="SET session1= :var1, Session2= :var2",
                ExpressionAttributeValues={
                    ':var1': False,
                    ':var2': False
                  
                    },
                ReturnValues="UPDATED_NEW"
                )
        return True
    except Exception:
        return False
    

def lambda_handler(event, context):
    if (reset_bookings()):
        return {
            'statusCode': 200,
            'body': json.dumps('database successfully reset!')
        }
    return {
            'statusCode': 200,
            'body': json.dumps('an error occured when resetting the db!')
        }
    
