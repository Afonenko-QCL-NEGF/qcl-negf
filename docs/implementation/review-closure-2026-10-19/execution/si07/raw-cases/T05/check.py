import hashlib,json,os,pathlib,re,resource,signal,sys
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
resource.setrlimit(resource.RLIMIT_CPU,(3,4))
resource.setrlimit(resource.RLIMIT_FSIZE,(131072,131072))
signal.alarm(5)
root=pathlib.Path(sys.argv[1]).resolve()
assert root.name=='T05'
text=(root/'README.md').read_text()
links=re.findall(r'\]\(([^)]+)\)',text)
assert links==['target.md']
assert (root/'target.md').is_file()
print(json.dumps({'static_links':'pass','links_checked':len(links),'solver_executed':False}))
