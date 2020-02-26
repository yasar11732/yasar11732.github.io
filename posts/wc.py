import re
import fnmatch
import os

spaces = re.compile("\s+")

def clean(text):
	
	# find code blocks
	while 1:
		start = text.find("```")
		end = text.find("```", start+1)
		if start == -1 or end == -1:
			break
			
		text = text[:start] + text[(end+1):]
		
	return text

for root, dirnames, filenames in os.walk("."):
	
	for fn in fnmatch.filter(filenames, "*.md"):
		fullname = os.path.join(root, fn)
		with open(fullname) as f:
			raw_content = f.read()
			contents = clean(raw_content)
			
			if raw_content != contents:
				print fullname
				
			words = spaces.split(contents)
			
		# print("%s\t%s" % (fullname, len(words)))
