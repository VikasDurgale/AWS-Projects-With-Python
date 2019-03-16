import click


@click.group()
def cli():
    pass


@cli.command('test', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True
))
@click.argument('id')
@click.pass_context
def test(ctx, id):
    data = dict()
    tags=dict()
    tag_list = list()
    for item in ctx.args:
        print(item)
        data.update([item.split('=')])
    #print(data)
    for items in data.items():
        #print(items[0] +": "+ items[1])
        tags['Key'] = items[0]
        tags['Value'] = items[1]
        tag_list.append(tags)

    print(tag_list)
    print(id)

if __name__ == '__main__':
    cli()
