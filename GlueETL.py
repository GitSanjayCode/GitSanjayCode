import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())

participantheader = glueContext.create_dynamic_frame.from_catalog(database="myfirstglue", table_name="participantheader")
participantdetail = glueContext.create_dynamic_frame.from_catalog(database="myfirstglue", table_name="participantdetail")
transaction = glueContext.create_dynamic_frame.from_catalog(database="myfirstglue", table_name="transaction")
participantdetailflexfield = glueContext.create_dynamic_frame.from_catalog(database="myfirstglue", table_name="participantdetailflexfield")


print("Count: " + str(participantheader.count()))
participantheader.printSchema()

print("Count: " + str(participantdetail.count()))
participantdetail.printSchema()

print("Count: " + str(transaction.count()))
transaction.printSchema()

print("Count: " + str(participantdetailflexfield.count()))
participantdetailflexfield.printSchema()

participantheader = participantheader.drop_fields(['col4'])
participantheader.toDF().show()

participantdetail.toDF().show()

transaction.toDF().show()

participantdetailflexfield = participantdetailflexfield.drop_fields(['columnumber'])

participantdetailflexfield.toDF().show()

for row in participantdetailflexfield.toDF().rdd.collect():
    print(row.actualcolumnname+' '+row.flexfielddescription)
    participantdetail = participantdetail.rename_field(row.actualcolumnname,row.flexfielddescription)
    
participantdetail.toDF().show()


detail = Join.apply(transaction,
                       Join.apply(participantheader, participantdetail, 'participant id', 'participant id'),
                       'participant detail id', 'participant detail id').drop_fields(['participant id', 'participant detail id'])

print(detail.count())

detail.printSchema()

detail.toDF().show()

BUCKET_NAME = 'myglue-sample-target'
PREFIX = 'output-dir/detail'

glueContext.write_dynamic_frame.from_options(frame = detail,
              connection_type = "s3",
              connection_options = {"path": "s3://"+BUCKET_NAME+"/"+PREFIX},
              format = "csv")

detailoutput = detail.toDF()
detailoutput.write.csv("s3://"+BUCKET_NAME+"/"+PREFIX)

import boto3
client = boto3.client('s3')

response = client.list_objects(
    Bucket=BUCKET_NAME,
    Prefix=PREFIX,
)
name = response["Contents"][0]["Key"]

print('BUCKET_NAME: '+BUCKET_NAME)
print('PREFIX: '+PREFIX)
print('name: '+name)

client.copy_object(Bucket=BUCKET_NAME, CopySource=BUCKET_NAME+'/'+name, Key=PREFIX+"DetailView.csv")
#client.delete_object(Bucket=BUCKET_NAME, Key='/'+name)

