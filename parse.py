a_file = open("Soiree.m3u8", "r")
lines = a_file.readlines()
a_file.close()
with open("new.txt", "w") as f:
    for line in lines:
        if not line.startswith("#"):
            f.write(line.replace("primary/", "This PC/Pixel 6/Internal shared storage/"))
