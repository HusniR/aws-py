import boto3

if __name__ == '__main__' :
	session = boto3.Session(profile_name='boto3')
	#s3 = boto3.resource('s3)
	#s3 = boto3.resource('s3')
	#for bucket in s3.buckets.all():
	#    print(bucket.name)

	ec2 = boto3.resource('ec2')
	#instances = ec2.instances.filter(
	#    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	#for instance in instances:
	#   print(instance.id, instance.instance_type)

	for i in ec2.instances.all():
	    print (i)
