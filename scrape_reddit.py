#! python3
"""Created: Tue May 19 16:06:52 2020 @author: Rajat Verma"""

import praw
import csv
from datetime import datetime as time

# create the praw Reddit object
red = praw.Reddit(client_id = 'wejqi7u3P_dE4A',
                  client_secret = '21iuFXgESnIg4BaUMzSSt6yinAA',
                  user_agent = 'uber_drivers_reddit',
                  username = 'emphasent',
                  password = 'Wje3Rj!ShVZ9dPg')
# get the Uber drivers' subreddit
sub = red.subreddit('uberdrivers')

def log(msg, file='data_read_errors.log'):
    with open(file, 'a') as f:
        f.write('%s: %s\n' % (time.now().isoformat(), msg))

def get_obj_info(obj, fields):
    '''Get only relevant fields of an PRAW object'''
    res = {}
    for field in fields:
        if obj is not None:
            res[field] = getattr(obj, field)
        else:
            res[field] = None
    return res

# define the fields the details
fields = {
    'thd': ['id','created','num_comments',
          'permalink','score','title','upvote_ratio'],
    'msg': ['id','link_id','created_utc','is_submitter',
            'parent_id','score','body'],
    'auth': ['id','name','comment_karma','created_utc',
             'fullname','is_mod','is_gold','link_karma']
}

files = {
    'thd': 'data/threads.csv',
    'msg': 'data/messages.csv',
    'auth': 'data/authors.csv'
}

#def read_submissions(top, save=False):
#    thds = []
#    msgs = []
#    auths = {}
#    for post in sub.top(limit = top):
#        # get the thread details
#        thd = get_obj_info(post, fields['thd'])
#        if post.author is not None:
#            thd['auth_id'] = post.author.id
#            auths[post.author.id] = get_obj_info(post.author, fields['auth'])
#        else:
#            thd['auth_id'] = ''
#        thds.append(thd)
#        # get the author details
#        
#        # get the messages/comments
#        for com in post.comments:
#            try:
#                msg = get_obj_info(com, fields['msg'])
#                # get the author details
#                if com.author is not None:
#                    msg['auth_id'] = com.author.id
#                    auth = get_obj_info(com.author, fields['auth'])
#                    auths[com.author.id] = auth
#                else:
#                    msg['auth_id'] = ''
#                msgs.append(msg)
#            except TypeError as e:
#                # logging.debug('msg[{}]:{}'.format(com.id, e))
#                log('msg[{}]:{}'.format(com.id, e))
#                # pass
#            except AttributeError as e:
#                # logging.debug('msg[{}]:{}'.format(com.id, e))
#                log('msg[{}]:{}'.format(com.id, e))
#                # pass
#    
#    thds = pd.DataFrame(thds).set_index('id')
#    msgs = pd.DataFrame(msgs).set_index('id')
#    auths = pd.DataFrame(list(auths.values())).set_index('id')
#    
#    if save:
#        thds.to_csv(files['thd'], index=False)
#        msgs.to_csv(files['msg'], index=False)
#        auths.to_csv(files['auth'], index=False)
#    
#    return thds, msgs, auths

def read_write_submissions(subreddit, top):
    # open the files
    f_thd = open(files['thd'], 'w', newline='', encoding='utf-8')
    f_msg = open(files['msg'], 'w', newline='', encoding='utf-8')
    f_auth = open(files['auth'], 'w', newline='', encoding='utf-8')
    
    # create the writer objects & write the header row
    w_thd = csv.writer(f_thd)
    w_msg = csv.writer(f_msg)
    w_auth = csv.writer(f_auth)
    w_thd.writerow(fields['thd'])
    w_msg.writerow(fields['msg'])
    w_auth.writerow(fields['auth'])
    
    # iterate over the submissions
    post_num = 0
    for post in subreddit.top(limit=top):
        post_num += 1
        if post_num < 1000:
            continue
        print('Post#%d' % post_num)
        try:
            # get the thread details
            thd = get_obj_info(post, fields['thd'])
            if post.author is not None:
                thd['auth_id'] = post.author.id
                auth = get_obj_info(post.author, fields['auth'])
                w_auth.writerow(auth.values())
            else:
                thd['auth_id'] = ''
            w_thd.writerow(thd.values())
            
            # get the messages/comments
            for com in post.comments:
                try:
                    msg = get_obj_info(com, fields['msg'])
                    # get the author details
                    if com.author is not None:
                        msg['auth_id'] = com.author.id
                        auth = get_obj_info(com.author, fields['auth'])
                        w_auth.writerow(auth.values())
                    else:
                        msg['auth_id'] = ''
                    w_msg.writerow(msg.values())
                except TypeError as e:
                    log('msg[{}]:{}'.format(com.id, e))
                except AttributeError as e:
                    log('msg[{}]:{}'.format(com.id, e))
        except Exception as e:
            log('post[{}]:unexpected error:{}'.format(post_num, e))
    
    # close the files
    f_thd.close()
    f_msg.close()
    f_auth.close()

#%% Main
t = time.now()
read_write_submissions(sub, top=10000)
print('Time elapsed: %.3fs' % (time.now() - t).total_seconds())
# time taken for top 1000 submissions: 20,604.5 s = 5.72 h