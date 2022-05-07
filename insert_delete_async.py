import sys, os, django,random, asyncio

############ DESKTOP ENV ###########################
sys.path.extend(["tweets"])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assignment.settings")
django.setup()

from django.contrib.auth.models import User
from tweets.models import Tweets

from asgiref.sync import sync_to_async

LINE = 'the quick brown fox jumps over the little lazy dog'.split()
tweets = [" ".join([random.choice(LINE) for y in range(random.randint(5,10))]) for x in range(10)]
usernames = list(User.objects.values_list('username',flat=True))

def insert_into_db(tweet):

    user = User.objects.get(username=random.choice(usernames))
    val = Tweets.objects.create(user=user,tweet=tweet)
    print('created ', tweet)
    return val

async def main():
    inserted = [await sync_to_async(insert_into_db)(tweet) for tweet in tweets]
    print(inserted)

if __name__ == "__main__":
    asyncio.run(main())
    print('DONE')
