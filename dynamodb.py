import boto3


class dynamodb_controller:

    def __init__(self):
        self.REGION = "ap-northeast-1"
        self.table_name = "plan"
        self.credential = "Ask Harry Lau"
        self.pw = "Ask Harry Lau"
        self.client = boto3.client('dynamodb', aws_access_key_id=self.credential, aws_secret_access_key=self.pw,
                                   region_name=self.REGION)
        self.resource = boto3.resource('dynamodb', aws_access_key_id=self.credential, aws_secret_access_key=self.pw,
                                       region_name=self.REGION)
        self.table = self.resource.Table(self.table_name)

    def save_plan(self, uid, name, description, progress, dueDate):

        item = {
            'id': {'S': str(uid)},
            'name': {'S': str(name)},
            'description': {'S': str(description)},
            'progress': {'S': str(progress)},
            'dueDate': {'S': str(dueDate)}
        }
        response = self.client.put_item(TableName=self.table_name, Item=item)
        print("Item inserted:", response)

    def scan_table(self):
        return self.table.scan()['Items']

    def edit_plan(self, uid, name, description, progress, dueDate):
        item = {
            'id': {'S': str(uid)},
            'name': {'S': str(name)},
            'description': {'S': str(description)},
            'progress': {'S': str(progress)},
            'dueDate': {'S': str(dueDate)}
        }
        try:
            response = self.client.update_item(TableName=self.table_name, Key={'id': {'S': uid}},
                                               AttributeUpdates={
                                                   'name': {'Value': item['name'], 'Action': 'PUT'},
                                                   'description': {'Value': item['description'], 'Action': 'PUT'},
                                                   'progress': {'Value': item['progress'], 'Action': 'PUT'},
                                                   'dueDate': {'Value': item['dueDate'], 'Action': 'PUT'},
                                               })
            print("Edit Successful：", response)
        except Exception as e:
            print("Edit Exception：", e)

    def delete_plan(self, uid):
        try:
            response = self.client.delete_item(
                TableName=self.table_name,
                Key={
                    'id': {'S': uid}
                }
            )
            print("Delete Successful：", response)
        except Exception as e:
            print("Delete Exception：", e)
