import mimetypes

print(mimetypes.guess_type("archive.tar.gz"))
# ('application/x-tar', 'gzip')

print(mimetypes.guess_type("song.png.gz"))
# ('audio/mpeg', None)

print(mimetypes.guess_type("data.csv"))
# ('text/csv', None)