# -*- coding:utf-8 -*-

import itchat
import csv

itchat.auto_login()   # 可设置hotReload = True 登录

# itchat.send('Hello', toUserName='filehelper')

friends = itchat.get_friends(update=True)
# for friend in friends:
#     print friend.Signature   # 个性签名
#     print friend.NickName    # 昵称
#     print friend.RemarkName  # 我的备注
#     print friend.UserName    # 唯一标识，类似于微信号


with open('/Users/admin/Desktop/WeChatFriend.csv', 'w') as csvfile:
    fieldnames = ['RemarkName', 'NickName', 'Signature', 'UserName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for friend in friends:
        writer.writerow(
            {
                'RemarkName': friend.RemarkName.encode('utf-8'),
                'NickName': friend.NickName.encode('utf-8'),
                'Signature': friend.Signature.encode('utf-8'),
                'UserName': friend.UserName
            }
        )
