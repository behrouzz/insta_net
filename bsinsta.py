from InstagramAPI import InstagramAPI
import pickle
import os

def log(username, password):
    api = InstagramAPI(username, password)
    api.login()
    return api

def save_me(api, adr=''):
    '''Save and return my network (list of followers & followings)'''
    
    ers = api.getTotalSelfFollowers()
    ing = api.getTotalSelfFollowings()

    followers = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in ers]
    followings = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in ing]
    my_data = [followers, followings]
    
    with open(adr+'me.pickle','wb') as f:
        pickle.dump(my_data, f)
    print('My network saved.')
    return my_data
    
def save_friend(api, username, user_id, adr=''):
    '''Save and return a friend's network (list of followers & followings)'''

    ers = api.getTotalFollowers(user_id)
    ing = api.getTotalFollowings(user_id)
    
    followers = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in ers]
    followings = [(i['pk'], i['username'], i['full_name'], i['is_private']) for i in ing]
    friend_data = [followers, followings]

    with open(adr+username+'.pickle','wb') as f:
        pickle.dump(friend_data, f)
    print(username + ' saved.')
    return friend_data


def get_insta(adr, my_username, my_password, fav_list):
    '''Return my (list) and my friends' (dic) networks'''
    api_loaded = False

    if not os.path.isdir(adr):
        os.makedirs(adr)

    # Read my network
    # ===============
    if os.path.isfile(adr+'me.pickle'):
        with open(adr+'me.pickle', 'rb') as f:
            my_data = pickle.load(f)
    else:
        api = log(my_username, my_password)
        api_loaded = True
        my_data = save_me(api, adr)

    my_net = list(set(my_data[0]+my_data[1]))
    all_ids = [i[0] for i in my_net]
    all_users = [i[1] for i in my_net]
    user2id = {u:v for (u,v) in zip(all_users,all_ids)}

    # Read friends's networks
    # =======================
    fs_data = []
    for i in fav_list:
        if os.path.isfile(adr+i+'.pickle'):
            with open(adr+i+'.pickle', 'rb') as f:
                fs_data.append(pickle.load(f))
        else:
            if not api_loaded:
                api = log(my_username, my_password)
                api_loaded = True
            fs_data.append(save_friend(api, i, user2id[i], adr=adr))

    fs_net_dc = {}
    for i in range(len(fs_data)):
        net = list(set(fs_data[i][0]+fs_data[i][1]))
        #net.append(me)
        fs_net_dc[fav_list[i]] = net

    return my_net, fs_net_dc

