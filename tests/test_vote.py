def test_vote_on_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json = {"post_id":test_posts[1].id,"dir":1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote/",json = {"post_id":test_posts[3].id,"dir":1})
    assert res.status_code == 409


def test_delete_post(authorized_client,test_posts,test_vote):
        res = authorized_client.post("/vote/",json = {"post_id":test_posts[3].id,"dir":0})

        assert res.status_code == 201


def test_delete_non_exisit_vote(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json = {"post_id":test_posts[3].id,"dir":0})

    assert res.status_code == 404


def test_vote_post_non_exisit(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json = {"post_id":"8000","dir":1})

    assert res.status_code == 404


def test_unauthrized_user_vote(client,test_posts):
    res = client.post("/vote/",json = {"post_id":test_posts[3].id,"dir":1})

    assert res.status_code == 401
