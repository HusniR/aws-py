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
def cli():
    """Shooty manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,help="only snapshots for Project(tag Project:<name>)")
def list_snapshots(project):
    "List EC2 snapshots"
    instances = filter_instances(project)
    for i in instances:

        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                    )))

    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@cli.group('instances')
def instances():
    """Commands for instances"""

@volumes.command('list')
@click.option('--project', default=None,help="only volumes for Project(tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)

    for i in instances:   
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
           )))
    return

@instances.command('snapshot', help = "Create snapshots for all volumes")
@click.option('--project', default=None,help="only instances for Project(tag Project:<name>)")
def create_snapshots(project):
    "Create Snapshot"
    instances = filter_instances(project)
    for i in instances:
        print ("Stopping {0}...".format(i.id))
        i.stop()
        i.wait_until_stopped()


        for v in i.volumes.all():
            print("creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by the boss")

            print ("Starting {0}...".format(i.id))
            i.start()
            i.wait_until_running()
    print ("Job Done...")

    return

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
    cli()














    #s3 = boto3.resource('s3)
    #s3 = boto3.resource('s3')
    #for bucket in s3.buckets.all():
    #    print(bucket.name)

    
    #instances = ec2.instances.filter(
    #    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    #for instance in instances:
    #   print(instance.id, instance.instance_type)


