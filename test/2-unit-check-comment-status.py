import json
import re
import requests


def get(url: str):
    """
    https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id=652985ab0000000023019186&cursor=&top_comment_id=
    :param url:
    :return:
    """
    cookies = "abRequestId=b3a24d97-e349-553f-866c-7fba9239ccaa; a1=18b287fe0af9atg98uvl7aoprycn0jsa7sc9ov2z750000374905; webId=037a83ee1baebf147894c93a32bf9802; gid=yYDJYWifdKWdyYDJYWid8MhJ0ij09kjY7h1WSuW0lUFvSj28I8VM0l888qW4j8280q00WSKf; xsecappid=xhs-pc-web; unread={%22ub%22:%226518f2d7000000001e02c4df%22%2C%22ue%22:%22650e6a0800000000130284f1%22%2C%22uc%22:23}; web_session=040069b030ce5a584c31f2c31e374bd7cbd784; webBuild=2.11.10; acw_tc=0b0a1754c5ada7b56e78dad92fed0bfb1a0145d9e77278026a74f1cff2b5381b; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=53f8ff8e-35db-4452-9d85-eeac2c67e529"
    headers = {
        'Cookie': cookies
    }
    response = requests.get(url, headers=headers)
    return response


def get_comment_status(url: str, comment: str):
    note_id = re.search(r'/explore/(\w{24})', url).group(1)
    response_data = json.loads(
        get(f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={note_id}").text)
    user_id = response_data["data"]["user_id"]
    for other_comment in response_data['data']['comments']:
        if other_comment['user_info']['user_id'] == user_id and other_comment['content'] == comment:
            return other_comment['status']
    return 0


if __name__ == '__main__':
    url1 = "https://www.xiaohongshu.com/explore/652967cd000000001c017307"
    comment1 = "真是太棒了！"
    if get_comment_status(url=url1, comment=comment1) == -1:
        print("已经被屏蔽")
    else:
        print("还没有被屏蔽")
