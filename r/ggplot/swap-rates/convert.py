f = open("skew_5x10_20180807.csv")

w = open("skew_5x10_20180807_modified.csv", 'w')
w.write("strike,volatility\n")
lines = f.readlines()

for a, b in zip(lines[0].strip().split(","), lines[1].strip().split(",")):
    w.write(a.replace("bps", "").replace('ATM', "0") + "," + b + "\n")

w.close()
f.close()