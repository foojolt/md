
### demo code

import org.apache.spark._
import org.apache.spark.streaming._

//val conf = new SparkConf().setAppName(appName).setMaster(master)
val conf = sc
val ssc = new StreamingContext(conf, Seconds(1))

val lines = ssc.socketTextStream("localhost", 9999)
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.reduceByKey(_ + _)
wordCounts.print()

ssc.start() 
ssc.awaitTermination() 

### netcat
nc -lk 9999




