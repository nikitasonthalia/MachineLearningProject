
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
object sparkweek3 {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("week3"));
  val textFile = sc.textFile("/Users/vikashkamdar/Desktop/MLProject/train_week3.csv")
  val counts = textFile.map(line => {
    val token = line.split(",");
     val key = token(4);
      val value = token(5) +"#"+ token(10);
      (key,value)}).groupByKey;
  
  counts.coalesce(1).saveAsObjectFile("/Users/vikashkamdar/Desktop/MLProject/week3output")
}
  }