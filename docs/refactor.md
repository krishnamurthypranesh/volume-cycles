# Objects
So, let's start off by listing the first class citizens of this script:
1. The first is the programme itself. This is the ultimate first class citizen for this entire programme. This can be serialized in multiple formats: JSON, CSV, and sometime in the future, in a database. So, each of the formats itself has to be considered as aprt of the structure itself.
2. Internally, the programme has three main objects:
	1. Exercise: Each exercise has a bunch of details
	2. Session: A session can consist of multiple exercises