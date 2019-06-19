import random
import asyncio
import graphene


class Author(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class Post(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    author = graphene.Field(Author)


class Query(graphene.ObjectType):
    posts = graphene.List(Post)

    def resolve_posts(root, info):
        return [
            Post(id=1, title="one", author=Author(id=1, name="Hamdy")),
            Post(id=2, title="two", author=Author(id=2, name="Aly")),
        ]


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


class Subscription(graphene.ObjectType):
    count_seconds = graphene.Float(up_to=graphene.Int())
    random_int = graphene.Field(RandomType)

    async def resolve_count_seconds(root, info, up_to=500):
        for i in range(up_to):
            print("YIELD SECOND", i)
            yield i
            await asyncio.sleep(1.)
        yield up_to

    async def resolve_random_int(root, info):
        i = 0
        while True:
            yield RandomType(seconds=i, random_int=random.randint(0, 500))
            await asyncio.sleep(1.)
            i += 1


schema = graphene.Schema(query=Query, subscription=Subscription)
