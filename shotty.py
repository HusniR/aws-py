import boto3
import click


session = boto3.Session(profile_name='boto3')
ec2 = boto3.resource('ec2')

@click.command()
def list_instances():
	"List EC2 instances"
	for i in ec2.instances.all():
	    print (', '.join((
	    	i.id,
	    	i.instance_type,
	    	i.placement['AvailabilityZone'],
	    	i.state['Name'],
	    	i.public_dns_name)))
	return

if __name__ == '__main__' :
	list_instances()














	#s3 = boto3.resource('s3)
	#s3 = boto3.resource('s3')
	#for bucket in s3.buckets.all():
	#    print(bucket.name)

	
	#instances = ec2.instances.filter(
	#    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	#for instance in instances:
	#   print(instance.id, instance.instance_type)


