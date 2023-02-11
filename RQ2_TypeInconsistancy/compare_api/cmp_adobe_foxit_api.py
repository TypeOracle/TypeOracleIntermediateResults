adobe_api = []
foxit_api = []
foxit_special = []
share_api = []


f = open("adobe_doc.txt", "r")
tmp = f.readlines()
f.close()

for line in tmp:
    adobe_api.append(line.strip())

f = open("adobe_undoc.txt", "r")
tmp = f.readlines()
f.close()

for line in tmp:
    adobe_api.append(line.strip())


f = open("foxit\\funclst.txt", "r")
tmp = f.readlines()
f.close()

for line in tmp:
    foxit_api.append(line.strip())

f = open("foxit\\setterlst.txt", "r")
tmp = f.readlines()
f.close()

for line in tmp:
    foxit_api.append(line.strip())

for api in foxit_api:
    if api in adobe_api:
        share_api.append(api)
    else:
        foxit_special.append(api)


f = open("share_api.txt", "w")
for api in share_api:
    f.write("{}\n".format(api))
f.close()

f = open("foxit_specific_api.txt", "w")
for api in foxit_special:
    f.write("{}\n".format(api))
f.close()