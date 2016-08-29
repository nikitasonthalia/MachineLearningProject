
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
object sparkweek3 {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("week"));
  val textFile = sc.textFile("/Users/vikashkamdar/Desktop/MLprojectOutput/train_week{0}.csv")
  val counts = textFile.map(line => {
    val token = line.split(",");
     val key = token(4);
   // val value = token(1) +"#"+ token(10);

     // val value = token(5) +"#"+ token(10);
      (key,(token(1),token(2),token(5),token(6),token(7),token(8),token(9),token(10)))}).groupByKey;
    //(key,value)}).groupByKey;


  counts.coalesce(1).saveAsTextFile("/Users/vikashkamdar/Desktop/MLprojectOutput/week{0}objectoutput")
}
  }