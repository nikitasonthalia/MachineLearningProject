import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
object Cooccurrence {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("matrix3")
    .setMaster("local[7]") 
     .set("spark.executor.memory", "4g")
     .set("spark.driver.memory","5g"));
    val valuefile =  sc.objectFile[(Char, Seq[(String)])]("/Users/vikashkamdar/Desktop/week7Pobjectoutput/part-00000");
    val output= valuefile.persist(StorageLevel.MEMORY_AND_DISK_SER).flatMap( {
      case (userid, values) =>
      {
        var productIds = values.map(value=>value.split("#")(0));
        var demand = values.map(value=>value.split("#")(1));
        productIds.combinations(2).map(
          pairs => {
             {(pairs.mkString("#"), 1)}
          })
    }}).reduceByKey(_ + _);

  output.coalesce(1).saveAsTextFile("/Users/vikashkamdar/Desktop/MLprojectOutput/week7ProductMatrix")
 
}
  }