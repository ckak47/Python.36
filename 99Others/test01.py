import os
import datetime
import arrow

# a = arrow.now()  # 当前本地时间
# print(a.timestamp)
# print(a.year)
# print(a.month)
# print(a.format("W"))
# print(a.date())
# print(a.time())
# b = a.shift(weeks=-4).format("W")[0:8]
# c = a.shift(weeks=-3).format("W")[0:8]
#
# print(a.shift(weeks=-2).format("W")[0:8])
# print(a.shift(weeks=-1).format("W")[0:8])
# print(a.shift(weeks=0).format("W")[0:8])
# print(a.shift(weeks=+1).format("W")[0:8])
# print(a.shift(weeks=+2).format("W"))
# print(a.shift(weeks=+3).format("W"))
# print(a.shift(weeks=+4).format("W"))

backup_time = arrow.now().format("W")[0:8]

destroy_backup_time = arrow.now().shift(weeks=-4).format("W")[0:8]

print(backup_time)
print(destroy_backup_time)
