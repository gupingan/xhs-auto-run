import random

rare_words = "敳屮屰屲峫峭峮嵂掴掵掶掸掹掺掻掼掽掾掿拣揁揂揃嵄嵙嵚嵛嵜庋庌庍庎庑庖庘庛庝庞庠庡庢嵴嵵嵶嵷嶊嶋嶌嶍嶎嶏嶪嶫嶬嶭巗巘巙巚暀暁暂暃暄暅暆暇晕晖暊暋暌暍暎暏暐暑暒暓暔暕暖暗旸暙暚暛暜暝暞暟暠暡暣暤暥暦暧暨暩暪"

for _ in range(20):
    print(random.choice(rare_words))


print(''.join(random.choices(rare_words, k=0)))
print(random.choices(rare_words, k=3))
print(len(['https://www.xiaohongshu.com/explore/652d1f73000000001e03ea10', 'https://www.xiaohongshu.com/explore/652d1f03000000001f03c327', 'https://www.xiaohongshu.com/explore/652d1e7d0000000023018dc6', 'https://www.xiaohongshu.com/explore/652d1e74000000001a015802', 'https://www.xiaohongshu.com/explore/652d1d1200000000220290f2', 'https://www.xiaohongshu.com/explore/652cb225000000001d014cb3', 'https://www.xiaohongshu.com/explore/652d1cd7000000001e02a73f', 'https://www.xiaohongshu.com/explore/652d1c18000000001a014afd', 'https://www.xiaohongshu.com/explore/652d1bfc000000001f034441', 'https://www.xiaohongshu.com/explore/652d1b4d000000002101f2f7', 'https://www.xiaohongshu.com/explore/652d1f3d000000001f005bee', 'https://www.xiaohongshu.com/explore/652d1dca000000001a0153ca', 'https://www.xiaohongshu.com/explore/652d1d65000000002101fbe3', 'https://www.xiaohongshu.com/explore/652d1c19000000001f0344f5', 'https://www.xiaohongshu.com/explore/652d1bb5000000002301b48d', 'https://www.xiaohongshu.com/explore/652d198d000000002101e917', 'https://www.xiaohongshu.com/explore/652d1973000000001d03a247', 'https://www.xiaohongshu.com/explore/652cdd4d000000001f004962', 'https://www.xiaohongshu.com/explore/652d180f000000001e00c78c', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac']
))

print(len(set(['https://www.xiaohongshu.com/explore/652d2102000000001d03b97a', 'https://www.xiaohongshu.com/explore/652d1fa4000000001a01612a', 'https://www.xiaohongshu.com/explore/652d1f74000000001a022325', 'https://www.xiaohongshu.com/explore/652d1f3d000000001f005bee', 'https://www.xiaohongshu.com/explore/652d1ebb000000001c016d40', 'https://www.xiaohongshu.com/explore/652d1ea9000000001f0058c0', 'https://www.xiaohongshu.com/explore/652d1dca000000001a0153ca', 'https://www.xiaohongshu.com/explore/652d1d65000000002101fbe3', 'https://www.xiaohongshu.com/explore/652d1c84000000002301b9fc', 'https://www.xiaohongshu.com/explore/652d1c19000000001f0344f5', 'https://www.xiaohongshu.com/explore/652d1bb5000000002301b48d', 'https://www.xiaohongshu.com/explore/652d198d000000002101e917', 'https://www.xiaohongshu.com/explore/652d1973000000001d03a247', 'https://www.xiaohongshu.com/explore/652cdd4d000000001f004962', 'https://www.xiaohongshu.com/explore/652d180f000000001e00c78c', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1c84000000002301b9fc', 'https://www.xiaohongshu.com/explore/652d1c19000000001f0344f5', 'https://www.xiaohongshu.com/explore/652d1bb5000000002301b48d', 'https://www.xiaohongshu.com/explore/652d198d000000002101e917', 'https://www.xiaohongshu.com/explore/652d1973000000001d03a247', 'https://www.xiaohongshu.com/explore/652cdd4d000000001f004962', 'https://www.xiaohongshu.com/explore/652d180f000000001e00c78c', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1765000000001e02f81f', 'https://www.xiaohongshu.com/explore/652d1765000000001a0162c1', 'https://www.xiaohongshu.com/explore/652d15c6000000001f03e11f', 'https://www.xiaohongshu.com/explore/652d155a000000001e02e7cf', 'https://www.xiaohongshu.com/explore/652d1520000000002101c3b9', 'https://www.xiaohongshu.com/explore/652d140a000000002101f8d9', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1765000000001e02f81f', 'https://www.xiaohongshu.com/explore/652d1765000000001a0162c1', 'https://www.xiaohongshu.com/explore/652d15c6000000001f03e11f', 'https://www.xiaohongshu.com/explore/652d155a000000001e02e7cf', 'https://www.xiaohongshu.com/explore/652d1520000000002101c3b9', 'https://www.xiaohongshu.com/explore/652d140a000000002101f8d9', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d129d000000001e00f7c0', 'https://www.xiaohongshu.com/explore/652d125b000000001a02242d', 'https://www.xiaohongshu.com/explore/652d115a000000001e02dc51', 'https://www.xiaohongshu.com/explore/652d10fd000000001f034e16', 'https://www.xiaohongshu.com/explore/652d0dea000000001c017534', 'https://www.xiaohongshu.com/explore/652d0d78000000002202b15d', 'https://www.xiaohongshu.com/explore/652d0cba000000001f037a68', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d129d000000001e00f7c0', 'https://www.xiaohongshu.com/explore/652d125b000000001a02242d', 'https://www.xiaohongshu.com/explore/652d115a000000001e02dc51', 'https://www.xiaohongshu.com/explore/652d10fd000000001f034e16', 'https://www.xiaohongshu.com/explore/652d0dea000000001c017534', 'https://www.xiaohongshu.com/explore/652d0d78000000002202b15d', 'https://www.xiaohongshu.com/explore/652d0cba000000001f037a68', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d0af0000000001f037230', 'https://www.xiaohongshu.com/explore/652d0a5d000000001e022f11', 'https://www.xiaohongshu.com/explore/652cf08d000000001e033892', 'https://www.xiaohongshu.com/explore/652d0920000000001d017978', 'https://www.xiaohongshu.com/explore/652d0693000000002101d3e2', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d0af0000000001f037230', 'https://www.xiaohongshu.com/explore/652d0a5d000000001e022f11', 'https://www.xiaohongshu.com/explore/652cf08d000000001e033892', 'https://www.xiaohongshu.com/explore/652d0920000000001d017978', 'https://www.xiaohongshu.com/explore/652d0693000000002101d3e2', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0423000000001f0349f3', 'https://www.xiaohongshu.com/explore/652cee4000000000200038f5', 'https://www.xiaohongshu.com/explore/652d018c000000001f03fa04', 'https://www.xiaohongshu.com/explore/652d00ff000000001c0157fb', 'https://www.xiaohongshu.com/explore/652cfe75000000001e02097b', 'https://www.xiaohongshu.com/explore/652cfd04000000001d016eba', 'https://www.xiaohongshu.com/explore/652cd020000000001e03041a', 'https://www.xiaohongshu.com/explore/652cfabb000000001e03e760', 'https://www.xiaohongshu.com/explore/652cf990000000001f0340a4', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0423000000001f0349f3', 'https://www.xiaohongshu.com/explore/652cee4000000000200038f5', 'https://www.xiaohongshu.com/explore/652d018c000000001f03fa04', 'https://www.xiaohongshu.com/explore/652d00ff000000001c0157fb', 'https://www.xiaohongshu.com/explore/652cfe75000000001e02097b', 'https://www.xiaohongshu.com/explore/652cfd04000000001d016eba', 'https://www.xiaohongshu.com/explore/652cd020000000001e03041a', 'https://www.xiaohongshu.com/explore/652cfabb000000001e03e760', 'https://www.xiaohongshu.com/explore/652cf990000000001f0340a4', 'https://www.xiaohongshu.com/explore/652cf4d5000000001d03ab26', 'https://www.xiaohongshu.com/explore/652cf3e6000000002101e6d0', 'https://www.xiaohongshu.com/explore/652cf2f9000000001a02321b'])))
print(len(['https://www.xiaohongshu.com/explore/652d2102000000001d03b97a', 'https://www.xiaohongshu.com/explore/652d1fa4000000001a01612a', 'https://www.xiaohongshu.com/explore/652d1f74000000001a022325', 'https://www.xiaohongshu.com/explore/652d1f3d000000001f005bee', 'https://www.xiaohongshu.com/explore/652d1ebb000000001c016d40', 'https://www.xiaohongshu.com/explore/652d1ea9000000001f0058c0', 'https://www.xiaohongshu.com/explore/652d1dca000000001a0153ca', 'https://www.xiaohongshu.com/explore/652d1d65000000002101fbe3', 'https://www.xiaohongshu.com/explore/652d1c84000000002301b9fc', 'https://www.xiaohongshu.com/explore/652d1c19000000001f0344f5', 'https://www.xiaohongshu.com/explore/652d1bb5000000002301b48d', 'https://www.xiaohongshu.com/explore/652d198d000000002101e917', 'https://www.xiaohongshu.com/explore/652d1973000000001d03a247', 'https://www.xiaohongshu.com/explore/652cdd4d000000001f004962', 'https://www.xiaohongshu.com/explore/652d180f000000001e00c78c', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1c84000000002301b9fc', 'https://www.xiaohongshu.com/explore/652d1c19000000001f0344f5', 'https://www.xiaohongshu.com/explore/652d1bb5000000002301b48d', 'https://www.xiaohongshu.com/explore/652d198d000000002101e917', 'https://www.xiaohongshu.com/explore/652d1973000000001d03a247', 'https://www.xiaohongshu.com/explore/652cdd4d000000001f004962', 'https://www.xiaohongshu.com/explore/652d180f000000001e00c78c', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1765000000001e02f81f', 'https://www.xiaohongshu.com/explore/652d1765000000001a0162c1', 'https://www.xiaohongshu.com/explore/652d15c6000000001f03e11f', 'https://www.xiaohongshu.com/explore/652d155a000000001e02e7cf', 'https://www.xiaohongshu.com/explore/652d1520000000002101c3b9', 'https://www.xiaohongshu.com/explore/652d140a000000002101f8d9', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d17fe000000001c017fac', 'https://www.xiaohongshu.com/explore/652cf57f000000001f0366ef', 'https://www.xiaohongshu.com/explore/652d1765000000001e02f81f', 'https://www.xiaohongshu.com/explore/652d1765000000001a0162c1', 'https://www.xiaohongshu.com/explore/652d15c6000000001f03e11f', 'https://www.xiaohongshu.com/explore/652d155a000000001e02e7cf', 'https://www.xiaohongshu.com/explore/652d1520000000002101c3b9', 'https://www.xiaohongshu.com/explore/652d140a000000002101f8d9', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d129d000000001e00f7c0', 'https://www.xiaohongshu.com/explore/652d125b000000001a02242d', 'https://www.xiaohongshu.com/explore/652d115a000000001e02dc51', 'https://www.xiaohongshu.com/explore/652d10fd000000001f034e16', 'https://www.xiaohongshu.com/explore/652d0dea000000001c017534', 'https://www.xiaohongshu.com/explore/652d0d78000000002202b15d', 'https://www.xiaohongshu.com/explore/652d0cba000000001f037a68', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d13df000000001f0077ba', 'https://www.xiaohongshu.com/explore/652d12ae00000000200011c1', 'https://www.xiaohongshu.com/explore/652d129d000000001e00f7c0', 'https://www.xiaohongshu.com/explore/652d125b000000001a02242d', 'https://www.xiaohongshu.com/explore/652d115a000000001e02dc51', 'https://www.xiaohongshu.com/explore/652d10fd000000001f034e16', 'https://www.xiaohongshu.com/explore/652d0dea000000001c017534', 'https://www.xiaohongshu.com/explore/652d0d78000000002202b15d', 'https://www.xiaohongshu.com/explore/652d0cba000000001f037a68', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d0af0000000001f037230', 'https://www.xiaohongshu.com/explore/652d0a5d000000001e022f11', 'https://www.xiaohongshu.com/explore/652cf08d000000001e033892', 'https://www.xiaohongshu.com/explore/652d0920000000001d017978', 'https://www.xiaohongshu.com/explore/652d0693000000002101d3e2', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0b430000000020003169', 'https://www.xiaohongshu.com/explore/652d0af0000000001f037230', 'https://www.xiaohongshu.com/explore/652d0a5d000000001e022f11', 'https://www.xiaohongshu.com/explore/652cf08d000000001e033892', 'https://www.xiaohongshu.com/explore/652d0920000000001d017978', 'https://www.xiaohongshu.com/explore/652d0693000000002101d3e2', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0423000000001f0349f3', 'https://www.xiaohongshu.com/explore/652cee4000000000200038f5', 'https://www.xiaohongshu.com/explore/652d018c000000001f03fa04', 'https://www.xiaohongshu.com/explore/652d00ff000000001c0157fb', 'https://www.xiaohongshu.com/explore/652cfe75000000001e02097b', 'https://www.xiaohongshu.com/explore/652cfd04000000001d016eba', 'https://www.xiaohongshu.com/explore/652cd020000000001e03041a', 'https://www.xiaohongshu.com/explore/652cfabb000000001e03e760', 'https://www.xiaohongshu.com/explore/652cf990000000001f0340a4', 'https://www.xiaohongshu.com/explore/652d0566000000001e03c8c3', 'https://www.xiaohongshu.com/explore/652d053f000000001f034e91', 'https://www.xiaohongshu.com/explore/652d0423000000001f0349f3', 'https://www.xiaohongshu.com/explore/652cee4000000000200038f5', 'https://www.xiaohongshu.com/explore/652d018c000000001f03fa04', 'https://www.xiaohongshu.com/explore/652d00ff000000001c0157fb', 'https://www.xiaohongshu.com/explore/652cfe75000000001e02097b', 'https://www.xiaohongshu.com/explore/652cfd04000000001d016eba', 'https://www.xiaohongshu.com/explore/652cd020000000001e03041a', 'https://www.xiaohongshu.com/explore/652cfabb000000001e03e760', 'https://www.xiaohongshu.com/explore/652cf990000000001f0340a4', 'https://www.xiaohongshu.com/explore/652cf4d5000000001d03ab26', 'https://www.xiaohongshu.com/explore/652cf3e6000000002101e6d0', 'https://www.xiaohongshu.com/explore/652cf2f9000000001a02321b']
))