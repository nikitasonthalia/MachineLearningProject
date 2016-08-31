
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
object DataFormat {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("week"));
  for( a <- 3 to 10){
    val textFile = sc.textFile("/home/zhang/Kaggle-Bimbo/MLprojectOutput/train_week"+a+".csv")
    val counts = textFile
//   	  val counts = textFile.map(line => {
//      val token = line.split(",");
//      val key = token(4);
//    (key,(token(1),token(2),token(5),token(6),token(7),token(8),token(9),token(10)))}).groupByKey;
    counts.coalesce(1).saveAsTextFile("/home/zhang/Kaggle-Bimbo/MLprojectOutput/week"+a+"objectoutput")
   }
  }
}
