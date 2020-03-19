import jpype
from jpype import *
import os
jvmPath = jpype.getDefaultJVMPath()
dependency = os.path.join(os.path.abspath('.'), '/home/appops/fmvec/hash-util')
#jvmPath = u'C:\Program Files\Java\jdk1.8.0_73\jre\bin\server\jvm.dll'
jpype.startJVM(jvmPath, "-Djava.ext.dirs=%s" %dependency)
jpype.java.lang.System.out.println("hello world!")
hashObj=JClass("com.netease.rec.news.engine.util.HashUtil")

devid = "F18A0295-607D-4225-979A-B70BA2A272E8"
print(hashObj.getToutiaoBucket(devid))

jpype.shutdownJVM()
