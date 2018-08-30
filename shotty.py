import boto3
import click


session = boto3.Session(profile_name='boto3')
ec2 = boto3.resource('ec2')

def filter_instances(project):
	if project:
		instances = ec2.instances.filter(
	    Filters=[{'Name': 'tag:Project', 'Values': [project]}])
	else:
	 	instances = ec2.instances.all()

	return instances

@click.group()
def instances():
	"''Commands for instances"""


@instances.command('list')
@click.option('--project', default=None,help="only instances for Project(tag Project:<name>)")
def list_instances(project):
	"List EC2 instances"
	instances = filter_instances(project)

	for i in instances:
		tags = {t['Key']:t['Value'] for t in i.tags or []}
		print(', '.join((
	    	i.id,
	    	i.instance_type,
	    	i.placement['AvailabilityZone'],
	    	i.state['Name'],
	    	i.public_dns_name, 
	    	tags.get('Project','<no project>')
	    	)))

	return


@instances.command('stop')
@click.option('--project',default=None, help='Only Instances for project')
def stop_instances(project):
	"Stop EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()
	return

@instances.command('start')
@click.option('--project',default=None, help='Only Instances for project')
def start_instances(project):
	"Start EC2 instances"

	instances = filter_instances(project)

	for i in instances:
		print("Starting {0}...".format(i.id))
		i.start()
	return

if __name__ == '__main__' :
	instances()














	#s3 = boto3.resource('s3)
	#s3 = boto3.resource('s3')
	#for bucket in s3.buckets.all():
	#    print(bucket.name)

	
	#instances = ec2.instances.filter(
	#    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	#for instance in instances:
	#   print(instance.id, instance.instance_type)


